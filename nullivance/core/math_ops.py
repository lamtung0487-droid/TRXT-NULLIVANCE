import numpy as np
from typing import Union, List

def elementwise_stability(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Implements f(x) = 1 - 2|x - 0.5|
    Section 2.1
    """
    return 1.0 - 2.0 * np.abs(x - 0.5)

def global_stability_geo(theta: np.ndarray, epsilon: float = 1e-9) -> float:
    """
    Implements Phi_geo(Theta) = exp( (1/d) * sum( log( max(f(Theta_k), epsilon) ) ) )
    Production v1.0 (Section 2.2)
    """
    # Ensure theta is a numpy array
    theta = np.asarray(theta)
    d = theta.shape[0]

    if d == 0:
        return 0.0 # Define behavior for empty dimension if necessary, or raise error.
                   # Spec implies d >= 1.

    # Calculate elementwise stability
    f_vals = elementwise_stability(theta)

    # Apply max(., epsilon)
    clamped_f = np.maximum(f_vals, epsilon)

    # Calculate log
    log_vals = np.log(clamped_f)

    # Mean of logs
    mean_log = np.mean(log_vals)

    # Exp
    return float(np.exp(mean_log))

def similarity_lcs(sig1: str, sig2: str) -> float:
    """
    LCS ratio as per Section 3.1
    sim_sigma = |LCS| / max(|sig1|, |sig2|)
    """
    if not sig1 or not sig2:
        return 0.0

    # Classic LCS Dynamic Programming
    m, n = len(sig1), len(sig2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if sig1[i - 1] == sig2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_len = dp[m][n]
    max_len = max(m, n)

    return lcs_len / max_len if max_len > 0 else 0.0

def similarity_phase_cosine(theta1: np.ndarray, theta2: np.ndarray, epsilon: float = 1e-9) -> float:
    """
    Phase similarity based on centered cosine.
    Section 3.2

    u = Theta1 - 0.5
    v = Theta2 - 0.5
    cos(u, v) = (u . v) / (|u||v| + epsilon)
    sim = (cos + 1) / 2
    """
    theta1 = np.asarray(theta1)
    theta2 = np.asarray(theta2)

    u = theta1 - 0.5
    v = theta2 - 0.5

    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)

    # Special case: If both vectors are effectively the center (0.5),
    # they are identical, so similarity is 1.0.
    # The center represents "perfect stability/resonance".
    if norm_u < epsilon and norm_v < epsilon:
        return 1.0

    dot_product = np.dot(u, v)
    cosine_sim = dot_product / (norm_u * norm_v + epsilon)

    return (cosine_sim + 1.0) / 2.0
