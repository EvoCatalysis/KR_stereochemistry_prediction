import subprocess
import sys

if len(sys.argv) != 4:
    print("Usage: python predict_KR_activity_simple.py query.fasta KR_active.hmm KR_Ctype.hmm")
    sys.exit(1)

query_fasta = sys.argv[1]
active_hmm = sys.argv[2]
ctype_hmm = sys.argv[3]

# run hmmsearch
subprocess.run(f"hmmsearch --tblout active.tbl {active_hmm} {query_fasta}", shell=True, stdout=subprocess.DEVNULL)
subprocess.run(f"hmmsearch --tblout ctype.tbl {ctype_hmm} {query_fasta}", shell=True, stdout=subprocess.DEVNULL)

def parse_tbl(tbl_file):
    scores = {}
    with open(tbl_file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            seq_id = parts[0]
            bit_score = float(parts[5])
            scores[seq_id] = bit_score
    return scores

active_scores = parse_tbl("active.tbl")
ctype_scores = parse_tbl("ctype.tbl")

all_ids = set(active_scores.keys()).union(set(ctype_scores.keys()))

# ONLY output label
for seq_id in all_ids:
    s_active = active_scores.get(seq_id, 0)
    s_ctype = ctype_scores.get(seq_id, 0)

    if s_active > s_ctype:
        print(f"{seq_id}\tactive")
    else:
        print(f"{seq_id}\tinactive")
