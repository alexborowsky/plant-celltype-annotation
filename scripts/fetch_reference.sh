#!/usr/bin/env bash
# fetch_reference.sh: download and build a reference-species proteome whose gene IDs match
# the skill's marker tables (references/markers/), for the homology step (SKILL.md Step 5).
#
# Usage:
#   bash scripts/fetch_reference.sh list                  # show the hubs in references/proteomes.tsv
#   bash scripts/fetch_reference.sh <key> [outdir]        # build one hub (e.g. arabidopsis, rice_msu7)
#   bash scripts/fetch_reference.sh all [outdir]          # build every hub that is reachable
#   bash scripts/fetch_reference.sh <key> [outdir] --check-only   # only re-measure the table match
#
# outdir defaults to $PROTEOME_DIR, else ./reference_proteomes.
# Build the hubs once into an outdir and point the DIAMOND commands at it.
#
# For each hub <key> it writes, in outdir:
#   <key>.pep.fa             longest protein isoform per gene; header ">GENE_ID symbol=..; description"
#                            (GENE_ID is the ID system of the marker tables; DIAMOND/BLAST keep only
#                            the first word, so hits come out as gene IDs and need no strip regex)
#   <key>_annotation.tsv     gene_id<TAB>symbol<TAB>description (header line), for
#                            map_markers.py --ref-annotation
#   <key>.dmnd               DIAMOND database (only if `diamond` is on PATH)
#   <key>_table_match.tsv    fraction of each matching marker table's IDs found in the proteome
#   raw/<file>               the downloaded source file (kept; delete to force a re-download)
#
# Behaviour:
#   - Reads the hub definitions (url, header format, id_strip_regex, id_rewrite) from
#     references/proteomes.tsv next to this script.
#   - Idempotent: skips the download if raw/<file> exists and the build if <key>.pep.fa is not older
#     than it. FORCE=1 rebuilds.
#   - Hubs that need a login (Phytozome) are built from `local_path` when that file exists (on
#     an Lmod cluster), or from LOCAL_SRC=/path/to/file for a single key; otherwise they are skipped with
#     instructions.
#   - DIAMOND: on an Lmod cluster `module load biology && module load diamond/2.1.23` first. Without it
#     the FASTA and annotation are still written and the makedb command is printed.
#   - Needs only bash, curl, gzip and python3 (standard library). No installs, no sudo.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
MANIFEST="${MANIFEST:-$SKILL_DIR/references/proteomes.tsv}"
MARKERS="$SKILL_DIR/references/markers"

usage() { sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'; }

[ $# -ge 1 ] || { usage; exit 1; }
case "$1" in -h|--help) usage; exit 0;; esac
KEY="$1"; shift
OUTDIR="${PROTEOME_DIR:-$PWD/reference_proteomes}"
CHECK_ONLY=0
for a in "$@"; do
    case "$a" in
        --check-only) CHECK_ONLY=1;;
        -*) echo "unknown option $a" >&2; exit 1;;
        *) OUTDIR="$a";;
    esac
done
[ -f "$MANIFEST" ] || { echo "manifest not found: $MANIFEST" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 not on PATH" >&2; exit 1; }

# manifest -> tab-separated fields for one key (by column name, so column order can change)
field() {  # field <key> <column>
    python3 - "$MANIFEST" "$1" "$2" <<'PY'
import csv, sys
path, key, col = sys.argv[1:4]
with open(path) as fh:
    rows = [r for r in csv.DictReader((l for l in fh if not l.startswith('#')), delimiter='\t')]
for r in rows:
    if r['key'] == key:
        print((r.get(col) or '').strip())
        sys.exit(0)
sys.exit(3)
PY
}

keys() {
    python3 - "$MANIFEST" <<'PY'
import csv, sys
with open(sys.argv[1]) as fh:
    for r in csv.DictReader((l for l in fh if not l.startswith('#')), delimiter='\t'):
        print(r['key'])
PY
}

if [ "$KEY" = "list" ]; then
    python3 - "$MANIFEST" <<'PY'
import csv, sys
with open(sys.argv[1]) as fh:
    for r in csv.DictReader((l for l in fh if not l.startswith('#')), delimiter='\t'):
        print('%-16s %-14s %-34s %s' % (r['key'], r['species'], r['id_system'][:34], r['access']))
PY
    exit 0
fi

have_diamond() { command -v diamond >/dev/null 2>&1; }

build_one() {
    local key="$1"
    local url fmt access local_path src base raw
    if ! url="$(field "$key" url)"; then echo "[$key] not in $MANIFEST (try: list)" >&2; return 1; fi
    fmt="$(field "$key" format)"
    access="$(field "$key" access)"
    local_path="$(field "$key" local_path)"
    mkdir -p "$OUTDIR/raw"

    if [ "$CHECK_ONLY" = 1 ]; then
        [ -s "$OUTDIR/$key.pep.fa" ] || { echo "[$key] no $OUTDIR/$key.pep.fa; build it first" >&2; return 1; }
        check_match "$key"; return 0
    fi

    # source: LOCAL_SRC (single key) > local_path (if readable) > url (only for access=public...)
    if [ -n "${LOCAL_SRC:-}" ] && [ "$KEY" != "all" ]; then
        [ -r "$LOCAL_SRC" ] || { echo "[$key] LOCAL_SRC not readable: $LOCAL_SRC" >&2; return 1; }
        src="$LOCAL_SRC"
    elif [ -n "$local_path" ] && [ -r "$local_path" ]; then
        src="$local_path"
    elif [[ "$access" == public* ]] && [[ "$url" =~ ^https?://[^[:space:]]+$ ]]; then
        base="$(basename "${url%%\?*}")"
        raw="$OUTDIR/raw/$base"
        if [ ! -s "$raw" ] || [ "${FORCE:-0}" = 1 ]; then
            echo "[$key] downloading $url"
            if ! curl -sSfL --retry 3 --retry-delay 5 -o "$raw.part" "$url"; then
                echo "[$key] download failed: $url" >&2; return 1
            fi
            mv -f "$raw.part" "$raw"
        else
            echo "[$key] using cached $raw"
        fi
        src="$raw"
    else
        echo "[$key] SKIPPED ($access)."
        echo "[$key]   Get the protein FASTA from $url (see the notes column of $MANIFEST),"
        echo "[$key]   then: LOCAL_SRC=/path/to/proteins.fa.gz bash $0 $key $OUTDIR"
        return 0
    fi

    local out="$OUTDIR/$key.pep.fa"
    if [ -s "$out" ] && ! [ "$src" -nt "$out" ] && [ "${FORCE:-0}" != 1 ]; then
        echo "[$key] $out is up to date"
    else
        echo "[$key] parsing $src (format=$fmt)"
        python3 - "$src" "$out" "$OUTDIR/${key}_annotation.tsv" "$fmt" \
            "$(field "$key" id_strip_regex)" "$(field "$key" id_rewrite)" <<'PY' || { echo "[$key] parse failed" >&2; return 1; }
import gzip, re, sys
src, out, ann_out, fmt, strip_re, rewrite = sys.argv[1:7]
strip_c = re.compile(strip_re) if strip_re else None
rw = None
if rewrite:
    pat, rep = rewrite.split('=>', 1)
    rw = (re.compile(pat), rep)

def opener(p):
    with open(p, 'rb') as fh:
        magic = fh.read(2)
    return gzip.open(p, 'rt') if magic == b'\x1f\x8b' else open(p)

def kv(header, key, stop):
    """value of key: or key= up to the next field of the same style"""
    m = re.search(r'(?:^|\s)' + re.escape(key) + r'(.*?)(?=' + stop + r'|$)', header)
    return m.group(1).strip() if m else ''

def parse_header(h):
    tok = h.split()[0]
    rest = h[len(tok):].strip()
    gene, sym, desc = '', '', ''
    if fmt == 'ensembl':
        m = re.search(r'\sgene:(\S+)', h)
        gene = m.group(1) if m else ''
        m = re.search(r'\sgene_symbol:(\S+)', h)
        sym = m.group(1) if m else ''
        m = re.search(r'\sdescription:(.*)$', h)   # last field; may contain ':'
        desc = re.sub(r'\s*\[Source:.*$', '', m.group(1)) if m else ''
    elif fmt == 'phytozome':
        m = re.search(r'\slocus=(\S+)', h)
        gene = m.group(1) if m else ''
    elif fmt == 'lis':
        m = re.search(r'\sgn=(\S+)', h)
        gene = m.group(1) if m else ''
        desc = kv(h, 'def=', r'\s\S+=')
        if not desc:
            m = re.match(r'(?:sp|tr)\|\S+\s+(.*?)\s+OS=', rest)
            desc = m.group(1) if m else ''
    elif fmt == 'msu':
        desc = rest.split('|', 1)[1] if '|' in rest else rest
    elif fmt == 'sgn':
        desc = re.sub(r'\s*\(AHRD[^)]*\)\s*$', '', rest).replace('%2C', ',')
    else:  # generic: rest of the line
        desc = rest
    return fix_id(gene or tok), sym, desc

best = {}   # gene -> (len, seq, sym, desc, order)
n_rec = 0
BAD = re.compile(r'[^A-Z*]')

def add(g, sym, desc, s):
    global n_rec
    s = BAD.sub('X', s.replace(' ', '').upper().rstrip('*.'))   # DIAMOND rejects '.' etc.
    if not s or not g:
        return
    n_rec += 1
    if sym and sym.upper() == g.upper():
        sym = ''
    desc = desc.replace('\t', ' ').strip()
    prev = best.get(g)
    if prev is None or len(s) > prev[0]:
        # keep symbol/description from any isoform if the longest lacks them
        sym = sym or (prev[2] if prev else '')
        desc = desc or (prev[3] if prev else '')
        best[g] = (len(s), s, sym, desc, prev[4] if prev else len(best))
    elif (not prev[2] and sym) or (not prev[3] and desc):
        best[g] = (prev[0], prev[1], prev[2] or sym, prev[3] or desc, prev[4])

def fix_id(gene):
    if strip_c:
        gene = strip_c.sub('', gene)
    if rw:
        gene = rw[0].sub(rw[1], gene)
    return gene

if fmt == 'genpept':
    # NCBI GenPept (*.gpff): gene ID from /locus_tag, symbol from /gene, description from /product
    def qual(rec, name):
        m = re.search(r'^\s+/' + name + r'="(.*?)"', rec, re.M | re.S)
        return re.sub(r'\s+', ' ', m.group(1)) if m else ''
    buf = []
    with opener(src) as fh:
        for line in fh:
            if line.startswith('//'):
                rec = ''.join(buf); buf = []
                if 'ORIGIN' not in rec:
                    continue
                feat, origin = rec.split('\nORIGIN', 1)
                seq = re.sub(r'[^A-Za-z*]', '', origin)
                add(fix_id(qual(feat, 'locus_tag')), qual(feat, 'gene'), qual(feat, 'product'), seq)
            else:
                buf.append(line)
else:
    def flush(h, seq):
        if h is None:
            return
        g, sym, desc = parse_header(h)
        add(g, sym, desc, ''.join(seq))
    h, seq = None, []
    with opener(src) as fh:
        for line in fh:
            if line.startswith('>'):
                flush(h, seq)
                h, seq = line[1:].strip(), []
            else:
                seq.append(line.strip())
        flush(h, seq)

if not best:
    sys.exit('no sequences parsed from ' + src)
tmp = out + '.tmp'
with open(tmp, 'w') as fo, open(ann_out + '.tmp', 'w') as fa:
    fa.write('gene_id\tsymbol\tdescription\n')
    for g, (L, s, sym, desc, _) in sorted(best.items(), key=lambda kv_: kv_[1][4]):
        extra = (' symbol=' + sym + ';' if sym else '') + (' ' + desc if desc else '')
        fo.write('>' + g + extra + '\n')
        for i in range(0, len(s), 60):
            fo.write(s[i:i + 60] + '\n')
        fa.write('%s\t%s\t%s\n' % (g, sym, desc))
import os
os.replace(tmp, out)
os.replace(ann_out + '.tmp', ann_out)
n_sym = sum(1 for v in best.values() if v[2])
n_desc = sum(1 for v in best.values() if v[3])
dotnum = sum(1 for g in best if re.search(r'\.\d+$', g))
print('  %d protein records -> %d genes (longest isoform); %d with symbol, %d with description'
      % (n_rec, len(best), n_sym, n_desc))
print('  example IDs: ' + ', '.join(list(best)[:3]))
if dotnum:
    print("  WARNING: %d gene IDs end in .<digits>; map_markers.py strips '\\.\\d+$' from reference IDs "
          "by default, so pass --ref-strip-regex='' with this hub" % dotnum)
PY
    fi

    if have_diamond; then
        if [ ! -s "$OUTDIR/$key.dmnd" ] || [ "$out" -nt "$OUTDIR/$key.dmnd" ] || [ "${FORCE:-0}" = 1 ]; then
            echo "[$key] diamond makedb"
            diamond makedb --in "$out" -d "$OUTDIR/$key" --quiet \
                || { echo "[$key] diamond makedb failed" >&2; return 1; }
        fi
    else
        echo "[$key] diamond not on PATH: database not built. On an Lmod cluster:"
        echo "[$key]   module load biology && module load diamond/2.1.23 && diamond makedb --in $out -d $OUTDIR/$key"
    fi
    check_match "$key" || echo "[$key] table-match check failed" >&2
}

# fraction of the matching marker tables' IDs (ref_gene and alt_id) present in the proteome
check_match() {
    local key="$1"
    python3 - "$OUTDIR/$key.pep.fa" "$MARKERS" "$(field "$key" ref_species)" \
        "$OUTDIR/${key}_table_match.tsv" <<'PY'
import csv, glob, os, re, sys
fa, mdir, species, out = sys.argv[1:5]
species = {s.strip().lower() for s in species.split(',') if s.strip()}
genes = set()
with open(fa) as fh:
    for line in fh:
        if line.startswith('>'):
            genes.add(line[1:].split()[0])
low = {g.lower() for g in genes}
rows = []
for f in sorted(glob.glob(os.path.join(mdir, '*.tsv')) + glob.glob(os.path.join(mdir, '*', '*.tsv'))):
    if os.sep + 'source' + os.sep in f:
        continue
    with open(f) as fh:
        rd = csv.DictReader(fh, delimiter='\t')
        if not rd.fieldnames or 'ref_gene' not in rd.fieldnames:
            continue
        recs = [r for r in rd if (r.get('ref_species') or '').strip().lower() in species]
    for col in ('ref_gene', 'alt_id'):
        ids = set()
        for r in recs:
            v = (r.get(col) or '').strip()
            if not v or v == '-':
                continue
            ids.add(re.sub(r'\.\d+$', '', re.split(r'[;,\s]', v)[0]))
        if not ids:
            continue
        hit = sorted(i for i in ids if i in genes or i.lower() in low)
        miss = sorted(ids - set(hit))
        rows.append((os.path.relpath(f, mdir), col, len(ids), len(hit),
                     '%.1f' % (100.0 * len(hit) / len(ids)), ','.join(miss[:8])))
with open(out, 'w') as fo:
    fo.write('table\tcolumn\tn_ids\tn_found\tpct_found\texample_missing\n')
    for r in rows:
        fo.write('\t'.join(map(str, r)) + '\n')
print('  table match (ID in proteome / distinct IDs; ref_species %s):' % ','.join(sorted(species)))
for t, c, n, k, p, miss in rows:
    print('    %-40s %-8s %4d/%-4d %5s%%  %s' % (t, c, k, n, p, miss[:60]))
if not rows:
    print('    (no marker table has ref_species in: %s)' % ','.join(sorted(species)))
PY
}

if [ "$KEY" = "all" ]; then
    fail=()
    for k in $(keys); do
        build_one "$k" || fail+=("$k")
    done
    [ ${#fail[@]} -eq 0 ] || { echo "FAILED: ${fail[*]}" >&2; exit 1; }
else
    build_one "$KEY"
fi
