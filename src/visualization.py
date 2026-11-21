"""Compact, labeled figures for aggregate mixture diagnostics."""

import matplotlib.pyplot as plt
import numpy as np

BLUE, TEAL, GRAY = "#285887", "#1F786E", "#536173"


def plot_selection(metrics):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for criterion, color in [("AIC", BLUE), ("BIC", TEAL)]:
        values = metrics[criterion]
        axes[0].plot(values.index, values - values.min(), "o-", label=criterion, color=color)
    axes[0].set(title="Penalized fit", ylabel="Difference from criterion minimum")
    axes[0].legend(frameon=False)
    stability = metrics.loc[metrics.index > 1]
    axes[1].plot(stability.index, stability["median_ARI"], "o-", color=BLUE, label="Median ARI")
    axes[1].plot(stability.index, stability["min_ARI"], "s--", color=GRAY, label="Minimum ARI")
    axes[1].set(title="Agreement across seeds", ylabel="Adjusted Rand index", ylim=(-0.05, 1.04))
    axes[1].legend(frameon=False, loc="lower left")
    fig.suptitle("Fit and stability in the synthetic sample")
    for ax in axes:
        ax.set(xlabel="Number of components", xticks=metrics.index)
    return fig


def plot_sizes(summaries):
    fig, axes = plt.subplots(1, len(summaries), figsize=(9, 3.6), sharey=True, layout="constrained")
    for ax, (k, summary) in zip(axes, summaries.items()):
        x = np.arange(k)
        ax.bar(x - .18, summary["modal_pct"], .36, color=BLUE, label="Modal assignment")
        ax.bar(x + .18, summary["weight_pct"], .36, color="white", edgecolor=TEAL,
               linewidth=1.5, label="Estimated mixture weight")
        ax.set(title=f"{k} profiles", xticks=x, xticklabels=summary.index)
    fig.suptitle("Profile sizes in the synthetic sample")
    axes[0].set_ylabel("Share of synthetic sample (%)")
    axes[-1].legend(frameon=False)
    return fig


def plot_profiles(profiles, blocks):
    fig, axes = plt.subplots(len(profiles), 2, figsize=(11, 6), layout="constrained")
    for column, label in enumerate(["Standardized centroids", "Centered within profiles"]):
        limit = max(np.abs(pair[column].to_numpy()).max() for pair in profiles.values())
        for ax, (k, pair) in zip(axes[:, column], profiles.items()):
            matrix = pair[column]
            heatmap = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-limit, vmax=limit)
            ax.set(yticks=np.arange(k), yticklabels=matrix.index, xticks=[])
            ax.grid(False)
            for boundary in range(5, matrix.shape[1], 5):
                ax.axvline(boundary - .5, color="white", linewidth=1.5)
        axes[0, column].set_title(label)
        axes[-1, column].set(xticks=np.arange(2, 25, 5), xticklabels=list(blocks.values()))
        fig.colorbar(heatmap, ax=axes[:, column], label="z" if column == 0 else "z minus profile mean", shrink=.85)
    fig.suptitle("Profile elevation and shape in the synthetic sample")
    for ax, k in zip(axes[:, 0], profiles):
        ax.set_ylabel(f"{k} profiles")
    return fig
