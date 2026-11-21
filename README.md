# Latent Profile Analysis: A Reproducible Python Example with Maladaptive Personality Traits

Latent profile analysis, a form of model-based profiling, identifies groups of observations that share similar configurations across several continuous indicators. It can reveal heterogeneity and combinations of characteristics that may be obscured when indicators are examined separately or combined into a single overall score. This Python example illustrates a workflow that can be applied to other sets of continuous indicators.

The demonstration uses 25 continuous scores named after facets of the Personality Inventory for DSM-5 (PID-5; Krueger et al., 2012; Sánchez, Montes, et al., 2023). **All data are completely synthetic.** The data were generated with four components and a fixed seed specifically to demonstrate the procedure. No scores come from real participants, and the results provide no empirical or clinical evidence.

## What the models show

The Gaussian mixture model estimates a mean and variance for each facet within each component. It also estimates posterior probabilities of component membership for each observation. The diagonal covariance specification assumes independence between facets within a component.

- **Two profiles** mainly distinguish lower from higher overall elevation. Overall elevation accounts for about 85% of the weighted variation between the fitted centroids.
- **Four profiles** retain the low and high profiles and distinguish two intermediate configurations. All five runs agree on the maximum-posterior assignments for both two and four profiles.
- **Six profiles** improve in-sample log-likelihood relative to four. The smallest group falls from 218 to 35, and the minimum pairwise adjusted Rand index (ARI) across seeds falls from 1.00 to 0.75.

BIC balances in-sample fit and model complexity. Relative entropy measures certainty given the fitted model. Both AIC and BIC favor four in this run. Relative entropy is high for both two and four, even though they summarize different aspects of the scores. The notebook reads these results alongside group sizes, posterior probabilities and stability across seeds.

See the [analysis notebook](notebooks/latent_profile_analysis.ipynb) for the full comparison.

![Four synthetic profiles across all 25 facets, grouped under five domains](figures/four-profile-facets.png)

### How to read the profiles

Each line in the main figure traces the 25 standardized facet means for one of the four fitted profiles. Zero marks the synthetic sample mean for each facet.

In the **two-profile solution**, P1 scores relatively low on virtually all 25 facets (*Lower overall maladaptive-trait elevation*). P2 scores relatively high on virtually all 25 (*Higher overall maladaptive-trait elevation*). The two-component solution primarily summarizes a general elevation gradient.

In the **four-profile solution**, the two intermediate profiles have similar overall elevation and different configurations. P2 combines relatively higher Hostility, Callousness, Manipulativeness and Deceitfulness with higher Impulsivity and Risk Taking and lower Anxiousness. P3 shows an approximately opposite pattern, with higher Anxiousness and Depressivity and lower scores on several Antagonism facets, including Callousness and Manipulativeness. The contrast illustrates how observations with similar overall elevation can differ in their combinations of traits.

The five-domain **display grouping** is a visual guide. Some facets are associated with more than one domain or show cross-loadings in published models. The grouping does not assign each facet uniquely to a domain, provide an official PID-5 scoring key or establish a definitive factor structure.

<details>
<summary>Facet abbreviation key</summary>

| Abbreviation | Facet | Display grouping |
|---|---|---|
| Anx | Anxiousness | Negative Affectivity |
| EL | Emotional Lability | Negative Affectivity |
| SI | Separation Insecurity | Negative Affectivity |
| Sub | Submissiveness | Negative Affectivity |
| Hos | Hostility | Negative Affectivity |
| Pers | Perseveration | Negative Affectivity |
| With | Withdrawal | Detachment |
| Anh | Anhedonia | Detachment |
| IA | Intimacy Avoidance | Detachment |
| Dep | Depressivity | Detachment |
| RA | Restricted Affectivity | Detachment |
| Susp | Suspiciousness | Detachment |
| Man | Manipulativeness | Antagonism |
| Dec | Deceitfulness | Antagonism |
| Gra | Grandiosity | Antagonism |
| AS | Attention Seeking | Antagonism |
| Cal | Callousness | Antagonism |
| Irr | Irresponsibility | Disinhibition |
| Imp | Impulsivity | Disinhibition |
| Distr | Distractibility | Disinhibition |
| RT | Risk Taking | Disinhibition |
| RP | Rigid Perfectionism | Disinhibition |
| UBE | Unusual Beliefs and Experiences | Psychoticism |
| Ecc | Eccentricity | Psychoticism |
| PD | Perceptual Dysregulation | Psychoticism |

</details>

| Supporting figure | What to look for |
|---|---|
| [Fit and stability](figures/fit-and-stability.png) | AIC, BIC and seed-to-seed agreement for the candidate counts |
| [Elevation and shape](figures/profile-elevation-and-shape.png) | Standardized and centered centroids for two and four profiles |
| [Profile sizes](figures/profile-sizes.png) | Modal group proportions and estimated mixture weights |

## Run the project

Use Python 3.12. From the repository root, create a virtual environment and install the dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab notebooks/latent_profile_analysis.ipynb
```

On Windows, activate with `.venv\Scripts\Activate.ps1` in PowerShell. Select the Python kernel for that environment and use **Restart Kernel and Run All Cells**. The notebook generates the synthetic data in memory and regenerates the four PNG files in `figures/`.

For a headless run from the repository root:

```bash
python -m nbconvert --to notebook --execute --inplace notebooks/latent_profile_analysis.ipynb
```

The stack uses NumPy, pandas, SciPy, scikit-learn, Matplotlib and Jupyter. The implementation lives in `src/simulation.py`, `src/modeling.py` and `src/visualization.py`.

## Limitations

The generator deliberately builds in four components and a clear shape contrast. Agreement across seeds measures optimization stability on one simulated sample. Generalization and stability across samples require separate evaluation. In empirical data, skew, residual correlations, measurement error and sampling can all affect apparent profiles. The components here illustrate modeling choices and have no diagnostic meaning.

## References

Krueger, R. F., Derringer, J., Markon, K. E., Watson, D., & Skodol, A. E. (2012). Initial construction of a maladaptive personality trait model and inventory for DSM-5. *Psychological Medicine, 42*(9), 1879–1890. https://doi.org/10.1017/S0033291711002674

Sánchez, R. O., Montes, S. A., Galarza, A. L., Somerstein, L. D., & Gainza, M. D. (2023). Una versión reducida y modificada del Inventario de Personalidad para el DSM-5 (PID-5) en la Argentina. *Interdisciplinaria, 40*(1), 115–136. https://doi.org/10.16888/interd.2023.40.1.7
