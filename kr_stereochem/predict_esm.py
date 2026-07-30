import torch, esm, numpy as np, pandas as pd
from Bio import SeqIO
from tqdm import tqdm
import joblib
from xgboost import XGBClassifier

def predict_from_fasta(
    fasta_path,
    model_path,
    scaler_path,
    output_file="KR_predictions_XGB.csv",
    batch_size=4
):
    # ==========================
    # Load trained model + scaler
    # ==========================
    xgb_model = XGBClassifier()
    xgb_model.load_model(model_path)

    scaler = joblib.load(scaler_path)
    # ==========================
    # Load ESM2-3B
    # ==========================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, alphabet = esm.pretrained.esm2_t36_3B_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval().to(device)

    # ==========================
    # Read FASTA
    # ==========================
    records = list(SeqIO.parse(fasta_path, "fasta"))

    # ==========================
    # Generate embeddings
    # ==========================
    def get_embeddings(records):
        all_embs, names = [], []
        for i in tqdm(range(0, len(records), batch_size)):
            batch = [(rec.id, str(rec.seq)) for rec in records[i:i+batch_size]]
            names.extend([rec.id for rec in records[i:i+batch_size]])
            _, _, batch_tokens = batch_converter(batch)
            batch_tokens = batch_tokens.to(device)

            with torch.no_grad():
                results = model(batch_tokens, repr_layers=[model.num_layers])

            reps = results["representations"][model.num_layers]
            seq_reps = [
                reps[k, 1:(batch_tokens[k] != alphabet.padding_idx).sum()-1]
                .mean(0)
                .cpu()
                .numpy()
                for k in range(len(batch))
            ]
            all_embs.extend(seq_reps)
            torch.cuda.empty_cache()

        return np.array(all_embs), names

    X_new, names = get_embeddings(records)

    # ==========================
    # Predict
    # ==========================
    X_scaled = scaler.transform(X_new)
    labels = xgb_model.predict(X_scaled)
    probs = xgb_model.predict_proba(X_scaled)[:, 1]

    types = ["A-type" if x == 1 else "B-type" for x in labels]

    # ==========================
    # Save output
    # ==========================
    output = pd.DataFrame({
        "Sequence_ID": names,
        "Predicted_Type": types,
        "Probability_A_type": probs
    })

    output.to_csv(output_file, index=False)
    return output
