import re
import unicodedata

def normalize(text):
    """
    Normalize text to lowercase, remove accents and non-alphanumeric characters.
    """
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def compute_wer(reference, hypothesis):
    """
    Compute Word Error Rate (WER) between reference and hypothesis strings.
    Returns a float between 0 and 1.
    """
    r = normalize(reference).split()
    h = normalize(hypothesis).split()

    n = len(r)
    m = len(h)
    # initialize DP matrix
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    return dp[n][m] / n if n else 0.0

def compute_tmr(ref_terms, hyp_terms, severity_weights=None):
    """
    Compute Terminology Medical Recall (TMR) with severity weighting.
    - ref_terms: list of gold terms (strings)
    - hyp_terms: iterable of recognized terms (strings)
    - severity_weights: dict mapping term->weight (default weight 1)
    Returns error rate in [0,1], representing percentage of missing/incorrect terms.
    """
    if severity_weights is None:
        severity_weights = {}

    total_weight = sum(severity_weights.get(t, 1) for t in ref_terms)
    hyp_set = set(hyp_terms)
    missing = set(ref_terms) - hyp_set

    # penalty for missing terms
    missed_w = sum(severity_weights.get(t, 1) for t in missing)
    # incorrect-term handling can be added here if desired
    incorrect_w = 0

    penalty = missed_w + incorrect_w
    return penalty / total_weight if total_weight else 0.0

def teme_error(wer, tmr, alpha=0.5):
    """
    Compute composite TEME-Error(alpha) = alpha * WER + (1-alpha) * TMR.
    Lower is better.
    """
    return alpha * wer + (1 - alpha) * tmr
