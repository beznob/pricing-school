# Probability Distributions in Insurance Pricing

## Overview

Insurance pricing models rely heavily on probability theory to model uncertain events and quantify risk. This document explains the key probability distributions used in insurance pricing and their mathematical properties.

## Frequency-Severity Modeling Framework

Insurance pricing typically separates the modeling of claims into two components:
- **Frequency**: How often claims occur
- **Severity**: How much each claim costs when it occurs
- **Aggregate Claims**: The total cost combining both frequency and severity

---

## 1. Frequency Distributions

Frequency distributions model the number of claims that occur in a given time period.

### Poisson Distribution

**Use Case**: Models the number of claims when events occur independently at a constant rate.

**Probability Mass Function**:
```
P(X = k) = (λ^k × e^(-λ)) / k!
```

**Parameters**:
- λ (lambda): Average number of claims per period
- k: Number of claims (0, 1, 2, ...)

**Properties**:
- Mean = λ
- Variance = λ
- Mean equals variance (equidispersion)

**Mathematical Characteristics**:
- Memoryless property
- Sum of independent Poisson variables is Poisson
- Suitable for rare events

**Insurance Applications**:
- Auto insurance claims per year
- Property damage claims
- Fire insurance claims
- Workers' compensation claims

**Example**: If λ = 2.5 claims per year:
- P(0 claims) = e^(-2.5) ≈ 0.082
- P(1 claim) = 2.5 × e^(-2.5) ≈ 0.205
- P(2 claims) = (2.5²/2!) × e^(-2.5) ≈ 0.257

### Negative Binomial Distribution

**Use Case**: Models claim frequency when there's overdispersion (variance > mean) or when claims cluster.

**Probability Mass Function**:
```
P(X = k) = C(k+r-1, k) × p^r × (1-p)^k
```

**Parameters**:
- r: Shape parameter (number of successes)
- p: Probability parameter
- k: Number of claims

**Properties**:
- Mean = r(1-p)/p
- Variance = r(1-p)/p²
- Variance > Mean (overdispersion)

**Mathematical Characteristics**:
- Gamma-Poisson mixture distribution
- Allows for heterogeneity in claim rates
- More flexible than Poisson

**Insurance Applications**:
- Health insurance claims (multiple conditions)
- Commercial liability claims
- Marine insurance claims
- Any scenario with claim clustering

**When to Use**:
- Data shows overdispersion
- Different risk profiles in portfolio
- Claims tend to cluster

---

## 2. Severity Distributions

Severity distributions model the cost of individual claims when they occur.

### Gamma Distribution

**Use Case**: Models claim amounts that are continuous, positive, and right-skewed.

**Probability Density Function**:
```
f(x) = (β^α / Γ(α)) × x^(α-1) × e^(-βx)
```

**Parameters**:
- α (alpha): Shape parameter
- β (beta): Rate parameter
- Scale parameter = 1/β

**Properties**:
- Mean = α/β
- Variance = α/β²
- Coefficient of Variation = 1/√α

**Mathematical Characteristics**:
- Flexible shape (can be exponential when α=1)
- Sum of independent Gamma variables is Gamma
- Conjugate prior for Poisson likelihood

**Insurance Applications**:
- Auto repair costs
- Medical expenses
- Property damage amounts
- General liability claims

**Shape Variations**:
- α < 1: Decreasing hazard rate
- α = 1: Exponential distribution (constant hazard)
- α > 1: Increasing hazard rate

### Log-Normal Distribution

**Use Case**: Models claim amounts that are the product of many independent factors.

**Probability Density Function**:
```
f(x) = (1/(x×σ×√(2π))) × e^(-(ln(x)-μ)²/(2σ²))
```

**Parameters**:
- μ (mu): Mean of log(X)
- σ (sigma): Standard deviation of log(X)

**Properties**:
- Mean = e^(μ + σ²/2)
- Variance = e^(2μ + σ²) × (e^(σ²) - 1)
- Highly right-skewed

**Mathematical Characteristics**:
- If X ~ Log-Normal, then ln(X) ~ Normal
- Multiplicative central limit theorem
- Heavy right tail

**Insurance Applications**:
- Large commercial property losses
- Liability claims with settlement negotiations
- Reinsurance claims
- Environmental liability

**Advantages**:
- Models multiplicative processes well
- Heavy tail for catastrophic losses
- Well-studied mathematical properties

### Pareto Distribution

**Use Case**: Models extreme losses and catastrophic claims with very heavy tails.

**Probability Density Function**:
```
f(x) = (α × x_m^α) / x^(α+1), for x ≥ x_m
```

**Parameters**:
- α (alpha): Shape parameter (tail index)
- x_m: Scale parameter (minimum value)

**Properties**:
- Mean = (α × x_m)/(α - 1) for α > 1
- Variance = (α × x_m²)/((α-1)² × (α-2)) for α > 2
- Very heavy tail

**Mathematical Characteristics**:
- Power law distribution
- Scale invariant
- Pareto principle (80-20 rule)

**Insurance Applications**:
- Catastrophic natural disasters
- Large liability claims
- Reinsurance pricing
- Cyber security losses

**Tail Behavior**:
- α ≤ 1: Infinite mean
- α ≤ 2: Infinite variance
- Smaller α = heavier tail

---

## 3. Aggregate Claims Distribution

### Compound Distribution

**Concept**: Combines frequency and severity to model total claims cost.

**Mathematical Formulation**:
```
S = X₁ + X₂ + ... + X_N
```

Where:
- N ~ Frequency distribution (Poisson, Negative Binomial)
- X_i ~ Severity distribution (Gamma, Log-normal, Pareto)
- S = Total aggregate claims

**Properties**:
- E[S] = E[N] × E[X]
- Var[S] = E[N] × Var[X] + Var[N] × (E[X])²

**Compound Poisson Model**:
- Most common in insurance
- N ~ Poisson(λ)
- X_i ~ Severity distribution
- Analytical solutions possible for some cases

**Compound Negative Binomial Model**:
- Used when frequency shows overdispersion
- More complex but more flexible
- Better for heterogeneous portfolios

### Moment Generating Functions

**Purpose**: Calculate moments and probabilities of aggregate claims.

**Compound Distribution MGF**:
```
M_S(t) = M_N(ln(M_X(t)))
```

**Applications**:
- Premium calculation
- Reserve estimation
- Capital allocation
- Risk assessment

---

## 4. Model Selection and Validation

### Goodness of Fit Tests

**Kolmogorov-Smirnov Test**:
- Tests if data follows specified distribution
- Sensitive to all aspects of distribution

**Anderson-Darling Test**:
- More sensitive to tail behavior
- Important for extreme losses

**Chi-Square Test**:
- Tests fit in different ranges
- Good for frequency distributions

### Information Criteria

**Akaike Information Criterion (AIC)**:
```
AIC = 2k - 2ln(L)
```

**Bayesian Information Criterion (BIC)**:
```
BIC = k×ln(n) - 2ln(L)
```

Where:
- k = number of parameters
- L = likelihood
- n = sample size

### Visual Diagnostics

**Q-Q Plots**: Compare quantiles of data vs. theoretical distribution
**P-P Plots**: Compare cumulative probabilities
**Density Plots**: Overlay fitted density with histogram
**Residual Analysis**: Check for patterns in residuals

---

## 5. Practical Implementation Considerations

### Parameter Estimation

**Method of Moments**:
- Simple and intuitive
- May not be efficient

**Maximum Likelihood Estimation**:
- Asymptotically optimal
- Requires numerical optimization

**Bayesian Estimation**:
- Incorporates prior knowledge
- Provides uncertainty quantification

### Data Quality Issues

**Censoring and Truncation**:
- Policy limits affect severity distribution
- Deductibles truncate small claims
- Requires specialized estimation methods

**Inflation Adjustment**:
- Claims costs increase over time
- Must adjust historical data
- Use appropriate price indices

**Development Patterns**:
- Claims may develop over time
- Need chain-ladder or other methods
- Affects both frequency and severity

### Regulatory Considerations

**Solvency Requirements**:
- Distributions must support capital calculations
- Tail risk measures important
- Value-at-Risk and Expected Shortfall

**Rate Filing Requirements**:
- Must demonstrate actuarial soundness
- Statistical significance of parameters
- Model validation documentation

---

## 6. Advanced Topics

### Mixed Distributions

**Zero-Inflated Models**:
- Handle excess zeros in data
- Combine point mass at zero with continuous distribution

**Mixture Models**:
- Combine multiple distributions
- Model heterogeneous populations
- EM algorithm for parameter estimation

### Copulas

**Purpose**: Model dependence between frequency and severity

**Applications**:
- Multi-peril modeling
- Catastrophe modeling
- Portfolio optimization

### Extreme Value Theory

**Generalized Extreme Value Distribution**:
- Models maximum claims in period
- Important for catastrophe modeling

**Peaks Over Threshold**:
- Models exceedances over high threshold
- Generalized Pareto Distribution

---

## 7. Software Implementation

### R Packages
- `fitdistrplus`: Distribution fitting
- `actuar`: Actuarial functions
- `MASS`: Statistical functions

### Python Libraries
- `scipy.stats`: Statistical distributions
- `numpy`: Numerical computations
- `pandas`: Data manipulation

### Example Model Selection Code

```python
# Fit multiple distributions and compare
from scipy import stats
import numpy as np

# Sample claim data
claims = np.array([...])  # Your claim data

# Fit different distributions
gamma_params = stats.gamma.fit(claims)
lognorm_params = stats.lognorm.fit(claims)
pareto_params = stats.pareto.fit(claims)

# Calculate AIC for each
def calculate_aic(params, data, dist):
    log_likelihood = np.sum(dist.logpdf(data, *params))
    return 2 * len(params) - 2 * log_likelihood

gamma_aic = calculate_aic(gamma_params, claims, stats.gamma)
lognorm_aic = calculate_aic(lognorm_params, claims, stats.lognorm)
pareto_aic = calculate_aic(pareto_params, claims, stats.pareto)

# Select best model (lowest AIC)
best_model = min([
    ('Gamma', gamma_aic),
    ('Log-Normal', lognorm_aic),
    ('Pareto', pareto_aic)
], key=lambda x: x[1])
```

---

## 8. Supplementary distributions and concepts

*(Merged from the former `Risk modelling job/Notes/general_notes.md`.)*

### The discrete building blocks

- **Bernoulli** — 0/1 claim occurrence per policy per period; the atom of frequency and conversion modelling.
- **Binomial** — number of policies with ≥1 claim out of a **fixed** n homogeneous units; variance `np(1−p)` understates variability when heterogeneity exists.
- **Geometric** — trials until the first event; the discrete memoryless distribution.
- **Poisson approximates Binomial** when n is large and p small (λ = np); if p isn't small or counts are over-dispersed, switch to Binomial or Negative Binomial.
- **Memoryless property**: `P(X > s+t | X > s) = P(X > t)` — Geometric (discrete), Exponential (continuous). The chance of an event next period doesn't depend on how long you've waited.

### More severity families

- **Exponential** — Gamma with α=1; constant hazard, memoryless; a tractable baseline for small claims and inter-arrival times. Mean 1/λ, Var 1/λ².
- **Weibull** — flexible increasing/decreasing hazard; lifetimes and varying tail shapes.
- **Tweedie** — the GLM workhorse family spanning Poisson→Gamma; a power parameter in (1,2) gives a compound Poisson–Gamma with **point mass at zero plus continuous positive amounts** — frequency and severity in a single model.
- **Beta** — on [0,1]; loss ratios, retention rates, probability priors, development factors.
- **Inverse Gaussian** — right-skewed, thick-tailed alternative to Gamma/Log-normal with convenient GLM properties.

### Gamma vs Log-normal vs Pareto — the tail decision

All three are positive-only. Tails: Gamma light-to-moderate (exponential decay) < Log-normal (sub-exponential) < Pareto (power law). Pick Gamma for positive skew without extremes, Log-normal for multiplicative processes with moderate tails, Pareto when extreme losses dominate. **The choice drives capital**: Pareto-like tails materially raise reserves, reinsurance prices and VaR/TVaR relative to Gamma/Log-normal fits.

### Mixing and heterogeneity

A portfolio of different risk classes makes the observed distribution a **mixture** — the reason simple models fail and over-dispersion appears. The canonical example: a Gamma-mixed Poisson **is** the Negative Binomial. Practical use: risk segmentation and pricing by class; ignoring heterogeneity invites adverse selection.

### Risk-management concepts

- **Tail measures**: **VaR** = a quantile of the loss distribution (e.g. 99.5th); **TVaR / expected shortfall** = expected loss *beyond* VaR — coherent, preferred for capital.
- **Loading & risk premium**: pure premium = E[Loss]; risk premium adds loading for parameter uncertainty, catastrophe risk, capital and profit.
- **Credibility theory**: blend individual experience with class averages in proportion to data volume — experience rating, bonus-malus, Bayesian shrinkage (the hierarchical-elasticity idea in pricing_school file 14 A5 is the same maths).
- **Ruin probability**: chance the insurer's surplus goes below zero; drives solvency monitoring and capital adequacy.

### Quick interview drill (distributions)

- Over-dispersion (variance > mean in counts)? → Negative Binomial, mixtures, or zero-inflated models.
- Many zeros plus positive continuous amounts? → Tweedie GLM (or a two-part frequency × severity model).
- Exposure varies by policy? → log link with `offset = log(exposure)` to model rates.
- Pricing a high excess-of-loss layer? → Pareto/GPD tail models, exceedance plots, tail-weighted goodness-of-fit, stress scenarios.
- VaR vs TVaR? → percentile vs average beyond the percentile; TVaR is coherent and better for tail risk.
- Censoring/truncation/reporting delays? → truncated/censored likelihoods or survival methods (policy limits censor severity; deductibles truncate it).

---

## Summary

Understanding these probability distributions and their mathematical properties is crucial for:

1. **Accurate Risk Modeling**: Choose appropriate distributions based on data characteristics
2. **Parameter Estimation**: Use proper statistical methods for parameter estimation
3. **Model Validation**: Apply appropriate tests to ensure model adequacy
4. **Business Applications**: Calculate premiums, reserves, and capital requirements
5. **Regulatory Compliance**: Meet actuarial standards and solvency requirements

The key is matching the distribution to the underlying data generating process and validating the model thoroughly before use in pricing decisions.
