# KR Stereochemistry Prediction

## Overview

Ketoreductase (KR) domains in modular PKSs control the stereochemistry of β-hydroxy intermediates, which strongly influences the structure and bioactivity of polyketide natural products.  
This tool predicts KR stereochemical type directly from amino-acid sequences using pretrained machine-learning models.

**Key features**
- FASTA-based sequence input
- ESM2-3B protein language model embeddings
- Pretrained XGBoost classifier
- Command-line interface for easy use


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Xinyingtsai/KR_stereochemistry_prediction.git
cd KR_stereochemistry_prediction
```

### 2. Create and activate a Python environment
Using conda:
```bash
conda create -n kr_esm python=3.9
conda activate kr_esm
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Install bioinformatics tools
```bash
conda install -c conda-forge -c bioconda hmmer mafft -y
```

If PyTorch is not installed automatically, install it explicitly:
```bash
python -m pip install torch
python -m pip install fair-esm
```

## Input Format
Input must be a FASTA file containing one or more KR domain amino-acid sequences.
Example:
```bash
>KR_001
TYLITGGTGYLGLK...
>KR_002
GTVLVTGGTGA...
```
## Usage

## Step 1. KR Activity Filtering (Active vs Inactive)

Before stereochemical prediction, KR domains are filtered to remove inactive C-type KRs that do not perform β-reduction.

This step uses two HMM profiles:
- KR_active.hmm (A/B-type KRs)
- KR_Ctype.hmm (inactive C-type KRs)

Run:

```bash
python active_inactive.py example.fasta KR_active.hmm KR_Ctype.hmm
```
Output:
```bash
result.tsv
```
Example:
```bash
KR_001, active
KR_002, active
```

## Step 2 KR stereochemistry prediction
```bash
python run_predict_esm.py --fasta example.fasta
```
Output:
The script generates a CSV file containing prediction results:
```bash
KR_predictions_XGB.csv
```
The output file contains the following columns:

Sequence_ID: FASTA record identifier

Predicted_Type: KR stereochemical type (A-type or B-type)

Probability_A_type: predicted probability for an A-type KR

Example:
```bash
Sequence_ID,Predicted_Type,Probability_A_type
KR_001,B-type,0.0892843
KR_002,A-type,0.6946625
```

## Training Models

**1. Site-specific classification based on aligned KR sequences and residue-level features**

**2. PLM-based classification using embeddings from protein language models (ESM)**

Prepare KR sequences and data

Run KR_Extraction.ipynb to extract and preprocess KR domains

Run Site_specific.ipynb for residue-level classification

Run ESM.ipynb for PLM-based classification


## Applications

Predicting KR stereochemistry in uncharacterized PKS biosynthetic gene clusters

Assisting rational PKS engineering and module design

Bridging sequence diversity gaps not covered by rule-based methods

## Citation

If you use this code in your research, please cite our paper:





