"""Generate fictional scores for 25 named PID-5 facets."""

import numpy as np
import pandas as pd

# Each entry gives a plot label, the facet name, and its contrast in the two
# intermediate components. The ordering is for display, not domain scoring.
DOMAINS = {
    "Negative Affectivity": (
        ("Anx", "Anxiousness", -1.10), ("EL", "Emotional Lability", -.75),
        ("SI", "Separation Insecurity", -.45), ("Sub", "Submissiveness", -.30),
        ("Hos", "Hostility", .75), ("Pers", "Perseveration", -.40),
    ),
    "Detachment": (
        ("With", "Withdrawal", -.35), ("Anh", "Anhedonia", -.50),
        ("IA", "Intimacy Avoidance", .25), ("Dep", "Depressivity", -.75),
        ("RA", "Restricted Affectivity", .55), ("Susp", "Suspiciousness", .20),
    ),
    "Antagonism": (
        ("Man", "Manipulativeness", .85), ("Dec", "Deceitfulness", .70),
        ("Gra", "Grandiosity", .55), ("AS", "Attention Seeking", -.15),
        ("Cal", "Callousness", .95),
    ),
    "Disinhibition": (
        ("Irr", "Irresponsibility", .15), ("Imp", "Impulsivity", .45),
        ("Distr", "Distractibility", -.45), ("RT", "Risk Taking", .65),
        ("RP", "Rigid Perfectionism", -.70),
    ),
    "Psychoticism": (
        ("UBE", "Unusual Beliefs and Experiences", -.20),
        ("Ecc", "Eccentricity", .30), ("PD", "Perceptual Dysregulation", -.30),
    ),
}
FACETS = [name for group in DOMAINS.values() for _, name, _ in group]


def simulate_facets(n_samples=1000, seed=314159):
    """Draw continuous scores from a four-component teaching simulation."""
    rng = np.random.default_rng(seed)
    elevations = np.array([-1.15, -.13, .13, 1.15])
    shape = np.array([contrast for group in DOMAINS.values() for _, _, contrast in group])
    shape -= shape.mean()
    means = elevations[:, None] + np.array([0, 1, -1, 0])[:, None] * shape
    # Facets also differ in how strongly they reflect the general gradient.
    means += elevations[:, None] * rng.uniform(-.18, .18, size=len(FACETS))
    scales = rng.uniform(.68, .91, size=len(FACETS))
    component = rng.choice(4, size=n_samples, p=[.27, .23, .26, .24])
    return pd.DataFrame(rng.normal(means[component], scales), columns=FACETS)
