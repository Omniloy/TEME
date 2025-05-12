### README.md

# TEME Scoring Demo

A **minimal, self‑contained example** that shows how to compute the new  
**TMR** metric and the tunable **TEME‑Error(α)** score described in the paper  
> *TEME: A Benchmark for Spanish Medical Speech Recognition*.

The repository contains:

| File | Purpose |
|------|---------|
| `metrics.py` | Core metrics: `compute_wer`, `compute_tmr`, `teme_error` |
| `score.py`   | CLI wrapper that prints WER, TMR and TEME‑Error(α) |
| `reference.txt` | Ground‑truth transcript for the long neurology dialogue |
| `hypothesis.txt` | Model output for the same dialogue |
| `ref_terms.json` | List of gold medical concepts to search for |
| `severity.json`  | *(optional)* per‑term weights — empty here but ready for CSS scores |

---

## 1 . Quick start

```bash
# For single dialogue evaluation:
python score.py \
  --ref reference.txt \
  --hyp hypothesis.txt \
  --ref_terms ref_terms.json \
  --alpha 0.5

# For batch processing from a CSV file:
python score.py \
  --batch_file TEME\ example.csv \
  --alpha 0.5
````

Sample outputs:

Single mode:
```
WER: 2.77%
TMR: 2.11%    # Error rate: percentage of missing/incorrect medical terms
TEME-Error(α=0.5): 2.44%
```

Batch mode:
```
Results for entry 1:
--------------------
WER: 2.77%
TMR: 2.11%
TEME-Error(α=0.5): 2.44%

Results for entry 2:
--------------------
WER: 3.15%
TMR: 2.89%
TEME-Error(α=0.5): 3.02%
```

Change **α** to emphasise safety vs. literal fidelity:

| Use‑case                             | α   | Command snippet |
| ------------------------------------ | --- | --------------- |
| Safety‑oriented (weight TMR 70 %)    | 0.3 | `--alpha 0.3`   |
| Dictation‑oriented (weight WER 70 %) | 0.7 | `--alpha 0.7`   |

---

## 2 . File overview

### `metrics.py`

```text
normalize()    – lower‑cases, strips accents/punct.
compute_wer()  – classic Levenshtein WER
compute_tmr()  – severity‑weighted term error rate (missing/incorrect terms)
teme_error()   – α·WER + (1‑α)·TMR
```

### `score.py`

Reads plain‑text transcripts and term lists from files, automatically detects medical terms in the hypothesis by searching for terms from ref_terms.json, then prints the three metrics:
- WER: Word Error Rate (percentage of incorrect words)
- TMR: Term Missing Rate (percentage of missing/incorrect medical terms)
- TEME-Error: Combined metric weighted by α

Add `--severity severity.json` once you have CSS weights.

### Input Formats

#### Single Mode Files


```jsonc
# ref_terms.json - List of medical terms to search for
[
  "cefalea",
  "fotofobia",
  "resonancia magnética nuclear cerebral",
  ...
]

# severity.json - Optional weights for terms
{
  "amitriptilina": 2,
  "onabotulinumtoxinA": 2,
  "cefalea": 1
}
```

Severity weight **2** doubles the penalty for a miss/incorrect term.

#### Batch Mode File

The CSV file for batch processing should have three columns:
- **Reference**: The reference transcript text
- **Medical terms**: A JSON array of medical terms as a string (e.g., `["term1", "term2", ...]`)
- **Hypothesis**: The hypothesis transcript text

Example CSV structure:
```csv
Reference,Medical terms,Hypothesis
"Patient reports...",["fever","headache","nausea"],"Patient reports..."
"Next dialogue...",["term1","term2"],"Next dialogue..."
```

---

## 3 . Extending the demo

1. **Replace** `reference.txt` / `hypothesis.txt` with your own dialogue pair.
2. **Extract** terms automatically (regex, neural NER) to create ref_terms.json.
3. **Annotate** high‑risk items in `severity.json` (optional).
4. **Run** `score.py` and compare α‑weighted scores.

---

## 4 . Dependencies

Pure Python 3 (no external libraries).
If you wish to speed up Levenshtein distance, install `python-Levenshtein`, but it's optional.

```bash
pip install python-Levenshtein
```

---

## 5 . Licence

Code and example data are released under the **Apache 2.0** licence.
If you use this template in academic work, please cite the TEME paper.

---

## 6 . Citation

```bibtex
@misc{Alcazar2025TEME,
  title   = {TEME: A Benchmark for Spanish Medical Speech Recognition},
  author  = {Enrique Alcázar and Paulina García Corral},
  year    = {2025},
  howpublished = {arXiv preprint not published yet arXiv:2505.XXXX}
}
