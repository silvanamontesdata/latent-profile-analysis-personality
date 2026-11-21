"""Fit diagonal Gaussian mixtures and report aggregate diagnostics."""

from itertools import combinations

import numpy as np
import pandas as pd
from scipy.special import xlogy
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits


def standardize(scores):
    """Check the indicators before scaling the full exploratory sample."""
    values = scores.to_numpy(dtype=float)
    if not np.isfinite(values).all() or (np.ptp(values, axis=0) == 0).any():
        raise ValueError("All indicators must be finite and have nonzero range.")
    return StandardScaler().fit_transform(values)


def compare_models(values, counts=range(1, 9), seeds=(17, 43, 101, 271, 503), n_init=12):
    """Keep the best converged fit per k and compare the converged runs."""
    rows, models = [], {}
    with threadpool_limits(limits=1):
        for k in counts:
            runs = [
                GaussianMixture(
                    n_components=k, covariance_type="diag", n_init=n_init,
                    init_params="kmeans", reg_covar=1e-5, tol=1e-4,
                    max_iter=500, random_state=seed,
                ).fit(values)
                for seed in seeds
            ]
            fits = [model for model in runs if model.converged_]
            if not fits:
                raise RuntimeError(f"No fits converged for k={k}.")
            log_likelihoods = np.array([model.score(values) * len(values) for model in fits])
            best = fits[log_likelihoods.argmax()]
            models[k] = best
            probabilities = best.predict_proba(values)
            sizes = np.bincount(probabilities.argmax(axis=1), minlength=k)
            assignments = [model.predict(values) for model in fits]
            agreements = [adjusted_rand_score(a, b) for a, b in combinations(assignments, 2)]
            entropy = 1 + xlogy(probabilities, probabilities).sum() / (len(values) * np.log(k)) if k > 1 else np.nan
            rows.append({
                "k": k, "log_likelihood": log_likelihoods.max(),
                "AIC": best.aic(values), "BIC": best.bic(values), "relative_entropy": entropy,
                "min_modal_n": sizes.min(), "max_modal_n": sizes.max(),
                "converged_seeds": len(fits),
                "median_ARI": np.median(agreements) if agreements else np.nan,
                "min_ARI": min(agreements, default=np.nan),
            })
    return pd.DataFrame(rows).set_index("k"), models


def describe_profiles(model, values, facets):
    """Summarize model means and posterior certainty by modal profile."""
    order = np.argsort(model.means_.mean(axis=1))
    names = [f"P{i}" for i in range(1, len(order) + 1)]
    means = pd.DataFrame(model.means_[order], columns=facets, index=names)
    elevation = means.mean(axis=1)
    shape = means.sub(elevation, axis=0)
    probabilities = model.predict_proba(values)[:, order]
    assignments = probabilities.argmax(axis=1)
    sizes = np.bincount(assignments, minlength=len(order))
    posterior = pd.Series(probabilities.max(axis=1)).groupby(assignments)
    groups = range(len(order))
    weights = model.weights_[order]

    deviations = means.to_numpy() - weights @ means.to_numpy()
    total = (weights[:, None] * deviations**2).sum()
    uniform = means.shape[1] * np.sum(weights * deviations.mean(axis=1)**2)
    summary = pd.DataFrame({
        "n_modal": sizes, "modal_pct": 100 * sizes / len(values),
        "weight_pct": 100 * weights,
        "posterior_mean": posterior.mean().reindex(groups).to_numpy(),
        "posterior_p10": posterior.quantile(.1).reindex(groups).to_numpy(),
        "elevation_z": elevation,
    }, index=names)
    return summary, means, shape, uniform / total
