"""Generate fictional facet scores from parameters chosen for demonstration."""

import numpy as np
import pandas as pd

BLOCKS = {
    "Detachment": "DET",
    "Unusual experiences": "UE",
    "Antagonism": "ANT",
    "Disinhibition": "DIS",
    "Negative affect": "NA",
}
FACETS = [f"{prefix}{i}" for prefix in BLOCKS.values() for i in range(1, 6)]


def simulate_facets(n_samples=1000, seed=314159):
    """Return 25 scores per synthetic record. No external inputs are used."""
    rng = np.random.default_rng(seed)
    # The two interior components differ in shape as well as average elevation.
    elevations = np.array([-1.05, -0.30, 0.30, 1.05])
    shape = np.array([0.0, 0.0, 0.65, 0.20, -0.85])
    block_means = elevations[:, None] + np.array([0, 1, -1, 0])[:, None] * shape
    means = np.repeat(block_means, 5, axis=1)
    means *= rng.uniform(0.85, 1.15, size=len(FACETS))

    component = rng.choice(4, size=n_samples, p=[0.27, 0.23, 0.26, 0.24])
    noise = rng.normal(0, 0.78, size=(n_samples, len(FACETS)))
    return pd.DataFrame(means[component] + noise, columns=FACETS)
