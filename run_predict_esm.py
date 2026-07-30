import argparse
from kr_stereochem.predict_esm import predict_from_fasta

def main():
    parser = argparse.ArgumentParser(
        description="KR stereochemistry prediction using ESM2-3B + XGBoost"
    )
    parser.add_argument("--fasta", required=True, help="Input FASTA file")
    parser.add_argument("--model", default="models/xgb_final_ESM2_3B.json")
    parser.add_argument("--scaler", default="models/scaler_ESM2_3B.pkl")
    parser.add_argument("--out", default="KR_predictions_XGB.csv")
    args = parser.parse_args()

    predict_from_fasta(
        fasta_path=args.fasta,
        model_path=args.model,
        scaler_path=args.scaler,
        output_file=args.out
    )

if __name__ == "__main__":
    main()
