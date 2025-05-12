import argparse
import json
import csv
from metrics import compute_wer, compute_tmr, teme_error, normalize

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_single(reference, hypothesis, ref_terms, severity_weights, alpha):
    """Process a single pair of reference/hypothesis texts."""
    # Compute metrics
    wer_val = compute_wer(reference, hypothesis)
    hyp_terms = find_terms_in_text(ref_terms, hypothesis)
    tmr_val = compute_tmr(ref_terms, hyp_terms, severity_weights)
    teme_err = teme_error(wer_val, tmr_val, alpha=alpha)

    # Output
    print(f"WER: {wer_val*100:.2f}%")
    print(f"TMR: {tmr_val*100:.2f}%")
    print(f"TEME-Error(α={alpha}): {teme_err*100:.2f}%")

def process_batch(csv_path, severity_weights, alpha):
    """Process multiple reference/hypothesis pairs from a CSV file."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            print(f"\nResults for entry {i}:")
            print("-" * 20)
            
            # Extract and clean data from CSV
            reference = row['Reference'].strip('\"')  # Remove potential quotes
            hypothesis = row['Hypothesis'].strip('\"')
            ref_terms = json.loads(row['Medical terms'])
            
            # Process this entry
            process_single(reference, hypothesis, ref_terms, severity_weights, alpha)

def find_terms_in_text(terms, text):
    """Find which terms from the list appear in the text."""
    normalized_text = normalize(text)
    found_terms = []
    for term in terms:
        if normalize(term) in normalized_text:
            found_terms.append(term)
    return found_terms

def main():
    parser = argparse.ArgumentParser(description='Compute WER, TMR, and TEME-Error metrics')
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--batch_file', help='Path to CSV file for batch processing')
    mode_group.add_argument('--ref', help='Path to reference transcript (.txt)')
    
    # Arguments for single-file mode
    parser.add_argument('--hyp', help='Path to hypothesis transcript (.txt)')
    parser.add_argument('--ref_terms', help='Path to JSON file with gold reference terms list')
    
    # Common arguments
    parser.add_argument('--severity', help='Path to JSON file with severity weights (term->weight)', default=None)
    parser.add_argument('--alpha', type=float, default=0.5, help='Alpha for TEME-Error (default 0.5)')
    args = parser.parse_args()

    # Load severity weights if provided
    severity_weights = load_json(args.severity) if args.severity else {}

    if args.batch_file:
        # Batch processing mode
        process_batch(args.batch_file, severity_weights, args.alpha)
    else:
        # Single file mode - validate required arguments
        if not all([args.ref, args.hyp, args.ref_terms]):
            parser.error("--ref, --hyp, and --ref_terms are required when not using --batch_file")
        
        # Load files
        with open(args.ref, 'r', encoding='utf-8') as f:
            reference = f.read()
        with open(args.hyp, 'r', encoding='utf-8') as f:
            hypothesis = f.read()
        ref_terms = load_json(args.ref_terms)
        
        # Process single file
        process_single(reference, hypothesis, ref_terms, severity_weights, args.alpha)

if __name__ == '__main__':
    main()
