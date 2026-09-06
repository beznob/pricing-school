"""
Utility functions for insurance pricing with causal inference.
This module contains common functions used across all notebooks.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def set_style():
    """Set matplotlib and seaborn styling"""
    try:
        plt.style.use('seaborn')
    except:
        plt.style.use('default')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12

def generate_synthetic_insurance_data(n_samples=10000, time_periods=12):
    """
    Generate synthetic insurance dataset with endogenous and exogenous variables.
    
    Parameters:
    -----------
    n_samples : int, default=10000
        Number of customers to generate
    time_periods : int, default=12
        Number of time periods for dynamic pricing
    
    Returns:
    --------
    pd.DataFrame: Synthetic insurance dataset
    """
    
    # Exogenous variables (not affected by price)
    age = np.random.normal(45, 15, n_samples)
    age = np.clip(age, 18, 80)  # Clip to realistic age range
    
    income = np.random.lognormal(10.5, 0.5, n_samples)  # Log-normal income distribution
    income = np.clip(income, 20000, 500000)  # Clip to realistic range
    
    # Geographic region (categorical)
    region = np.random.choice(['Urban', 'Suburban', 'Rural'], n_samples, p=[0.4, 0.4, 0.2])
    
    # Risk score (higher = more risky)
    risk_score = np.random.beta(2, 5, n_samples) * 100  # 0-100 scale
    
    # Previous claims history
    previous_claims = np.random.poisson(0.5, n_samples)  # Poisson distribution
    previous_claims = np.clip(previous_claims, 0, 5)
    
    # Market conditions (seasonal effects)
    market_volatility = np.random.normal(0.1, 0.05, n_samples)
    market_volatility = np.clip(market_volatility, 0.01, 0.3)
    
    # Competitor pricing (exogenous)
    competitor_price = np.random.normal(800, 200, n_samples)
    competitor_price = np.clip(competitor_price, 300, 2000)
    
    # Base price calculation (before treatment)
    base_price = (
        300 +  # Base premium
        (age - 18) * 5 +  # Age factor
        income * 0.0001 +  # Income factor
        risk_score * 8 +  # Risk factor
        previous_claims * 100 +  # Claims history
        np.where(region == 'Urban', 100, 0) +  # Urban premium
        np.where(region == 'Rural', -50, 0) +  # Rural discount
        competitor_price * 0.1 +  # Competitor response
        np.random.normal(0, 50, n_samples)  # Noise
    )
    
    # Treatment: Price levels (this is our intervention)
    # We'll simulate different pricing strategies
    price_multiplier = np.random.choice([0.8, 0.9, 1.0, 1.1, 1.2], n_samples, 
                                       p=[0.2, 0.2, 0.2, 0.2, 0.2])
    
    price = base_price * price_multiplier
    price = np.clip(price, 200, 3000)  # Realistic price range
    
    # Endogenous variables (affected by price)
    # Price sensitivity varies by customer characteristics
    price_sensitivity = (
        -0.001 +  # Base sensitivity
        (income - 50000) * -0.000001 +  # Higher income = less sensitive
        (age - 45) * -0.00001 +  # Older customers less sensitive
        risk_score * -0.00002 +  # Higher risk customers less sensitive
        np.where(region == 'Urban', -0.0005, 0) +  # Urban less sensitive
        np.random.normal(0, 0.0005, n_samples)  # Individual variation
    )
    
    # Calculate conversion probability (logistic function)
    price_effect = price_sensitivity * (price - base_price)
    
    # Base conversion probability
    base_conversion_logit = (
        -2 +  # Base conversion (low)
        (100 - risk_score) * 0.02 +  # Lower risk = higher conversion
        np.log(income / 50000) * 0.5 +  # Higher income = higher conversion
        (50 - age) * 0.01 +  # Younger customers more likely to convert
        np.where(region == 'Urban', 0.3, 0) +  # Urban advantage
        (competitor_price - price) * 0.002  # Competitive advantage
    )
    
    conversion_logit = base_conversion_logit + price_effect * 1000
    conversion_probability = 1 / (1 + np.exp(-conversion_logit))
    
    # Generate actual conversions
    conversion = np.random.binomial(1, conversion_probability)
    
    # Calculate profit (simplified P&L)
    cost_base = 400  # Base cost per policy
    cost_variation = risk_score * 2 + previous_claims * 50  # Risk-based costs
    cost = cost_base + cost_variation + np.random.normal(0, 20, n_samples)
    
    # Profit = Revenue - Cost (only for conversions)
    revenue = price * conversion
    profit = (revenue - cost) * conversion
    
    # Calculate Customer Lifetime Value (CLV)
    retention_probability = 0.8 + (1 - price_sensitivity) * 0.2
    retention_probability = np.clip(retention_probability, 0.1, 0.95)
    
    # Simple CLV calculation (3-year horizon)
    clv = profit * (1 + retention_probability + retention_probability**2)
    
    # Create DataFrame
    df = pd.DataFrame({
        'customer_id': range(n_samples),
        'age': age,
        'income': income,
        'region': region,
        'risk_score': risk_score,
        'previous_claims': previous_claims,
        'market_volatility': market_volatility,
        'competitor_price': competitor_price,
        'base_price': base_price,
        'price_multiplier': price_multiplier,
        'price': price,
        'price_sensitivity': price_sensitivity,
        'conversion_probability': conversion_probability,
        'conversion': conversion,
        'cost': cost,
        'revenue': revenue,
        'profit': profit,
        'retention_probability': retention_probability,
        'clv': clv
    })
    
    return df

def calculate_treatment_effects(df, treatment_col, outcome_col, confounders=None):
    """
    Calculate basic treatment effects using different methods.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    treatment_col : str
        Name of treatment variable
    outcome_col : str
        Name of outcome variable
    confounders : list, optional
        List of confounder variables
    
    Returns:
    --------
    dict: Treatment effects from different methods
    """
    
    results = {}
    
    # Simple difference in means
    treatment_groups = df[treatment_col].unique()
    
    if len(treatment_groups) == 2:
        # Binary treatment
        treated = df[df[treatment_col] == treatment_groups[1]][outcome_col]
        control = df[df[treatment_col] == treatment_groups[0]][outcome_col]
        
        results['simple_diff'] = treated.mean() - control.mean()
        results['t_stat'] = stats.ttest_ind(treated, control)[0]
        results['p_value'] = stats.ttest_ind(treated, control)[1]
    
    elif len(treatment_groups) > 2:
        # Multi-level treatment - compare highest vs lowest
        df_sorted = df.groupby(treatment_col)[outcome_col].mean().sort_values()
        lowest_group = df_sorted.index[0]
        highest_group = df_sorted.index[-1]
        
        treated = df[df[treatment_col] == highest_group][outcome_col]
        control = df[df[treatment_col] == lowest_group][outcome_col]
        
        results['simple_diff'] = treated.mean() - control.mean()
        results['t_stat'] = stats.ttest_ind(treated, control)[0]
        results['p_value'] = stats.ttest_ind(treated, control)[1]
        results['lowest_group'] = lowest_group
        results['highest_group'] = highest_group
        
        # Calculate effects for all groups vs baseline
        baseline_mean = df[df[treatment_col] == lowest_group][outcome_col].mean()
        group_effects = {}
        for group in treatment_groups:
            group_mean = df[df[treatment_col] == group][outcome_col].mean()
            group_effects[str(group)] = group_mean - baseline_mean
        
        results['group_effects'] = group_effects
    
    # Regression adjustment (skip for categorical treatment to avoid encoding issues)
    if confounders and len(treatment_groups) == 2:
        # For binary treatment only
        try:
            # Prepare data
            X = df[confounders + [treatment_col]]
            y = df[outcome_col]
            
            # Fit regression
            model = LinearRegression()
            model.fit(X, y)
            
            # Treatment effect is the coefficient of treatment variable
            treatment_idx = X.columns.get_loc(treatment_col)
            results['regression_coef'] = model.coef_[treatment_idx]
            
            # Calculate R-squared
            results['r_squared'] = model.score(X, y)
        except:
            # Skip regression if there are issues
            pass
    
    return results

def plot_treatment_effect(df, treatment_col, outcome_col, title="Treatment Effect"):
    """
    Plot treatment effects visualization.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    treatment_col : str
        Name of treatment variable
    outcome_col : str
        Name of outcome variable
    title : str
        Plot title
    """
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Box plot
    sns.boxplot(data=df, x=treatment_col, y=outcome_col, ax=axes[0])
    axes[0].set_title(f'{title} - Distribution by Treatment')
    axes[0].set_ylabel(outcome_col.replace('_', ' ').title())
    
    # Violin plot
    sns.violinplot(data=df, x=treatment_col, y=outcome_col, ax=axes[1])
    axes[1].set_title(f'{title} - Density by Treatment')
    axes[1].set_ylabel(outcome_col.replace('_', ' ').title())
    
    plt.tight_layout()
    plt.show()

def calculate_profit_metrics(df):
    """
    Calculate key profit and business metrics.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with profit calculations
    
    Returns:
    --------
    dict: Key business metrics
    """
    
    metrics = {}
    
    # Overall metrics
    metrics['total_customers'] = len(df)
    metrics['conversion_rate'] = df['conversion'].mean()
    metrics['average_price'] = df['price'].mean()
    metrics['total_revenue'] = df['revenue'].sum()
    metrics['total_profit'] = df['profit'].sum()
    metrics['profit_margin'] = metrics['total_profit'] / metrics['total_revenue'] if metrics['total_revenue'] > 0 else 0
    
    # Customer segments
    metrics['high_risk_conversion'] = df[df['risk_score'] > 70]['conversion'].mean()
    metrics['low_risk_conversion'] = df[df['risk_score'] <= 30]['conversion'].mean()
    
    # Price sensitivity analysis
    price_quartiles = pd.qcut(df['price'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    metrics['price_conversion_by_quartile'] = df.groupby(price_quartiles)['conversion'].mean().to_dict()
    
    # CLV metrics
    metrics['average_clv'] = df['clv'].mean()
    metrics['clv_conversion_correlation'] = df['clv'].corr(df['conversion'])
    
    return metrics

def optimize_pricing_simple(df, price_range=(200, 2000), n_points=100):
    """
    Simple pricing optimization using grid search.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    price_range : tuple
        Range of prices to test
    n_points : int
        Number of price points to test
    
    Returns:
    --------
    dict: Optimization results
    """
    
    prices = np.linspace(price_range[0], price_range[1], n_points)
    results = []
    
    for price in prices:
        # Estimate conversion at this price
        # Simple linear model for demonstration
        price_effect = df['price_sensitivity'] * (price - df['base_price'])
        conversion_logit = -2 + price_effect * 1000  # Simplified
        conversion_prob = 1 / (1 + np.exp(-conversion_logit))
        
        # Calculate expected profit
        expected_conversions = conversion_prob.sum()
        expected_revenue = price * expected_conversions
        expected_cost = df['cost'].mean() * expected_conversions
        expected_profit = expected_revenue - expected_cost
        
        results.append({
            'price': price,
            'expected_conversions': expected_conversions,
            'expected_revenue': expected_revenue,
            'expected_profit': expected_profit,
            'conversion_rate': conversion_prob.mean()
        })
    
    results_df = pd.DataFrame(results)
    optimal_idx = results_df['expected_profit'].idxmax()
    
    return {
        'optimal_price': results_df.loc[optimal_idx, 'price'],
        'optimal_profit': results_df.loc[optimal_idx, 'expected_profit'],
        'results': results_df
    }

def plot_pricing_optimization(optimization_results):
    """
    Plot pricing optimization results.
    
    Parameters:
    -----------
    optimization_results : dict
        Results from optimize_pricing_simple
    """
    
    results_df = optimization_results['results']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Profit vs Price
    axes[0, 0].plot(results_df['price'], results_df['expected_profit'])
    axes[0, 0].axvline(optimization_results['optimal_price'], color='red', linestyle='--', 
                      label=f'Optimal: ${optimization_results["optimal_price"]:.0f}')
    axes[0, 0].set_xlabel('Price')
    axes[0, 0].set_ylabel('Expected Profit')
    axes[0, 0].set_title('Profit vs Price')
    axes[0, 0].legend()
    
    # Conversion Rate vs Price
    axes[0, 1].plot(results_df['price'], results_df['conversion_rate'])
    axes[0, 1].axvline(optimization_results['optimal_price'], color='red', linestyle='--')
    axes[0, 1].set_xlabel('Price')
    axes[0, 1].set_ylabel('Conversion Rate')
    axes[0, 1].set_title('Conversion Rate vs Price')
    
    # Revenue vs Price
    axes[1, 0].plot(results_df['price'], results_df['expected_revenue'])
    axes[1, 0].axvline(optimization_results['optimal_price'], color='red', linestyle='--')
    axes[1, 0].set_xlabel('Price')
    axes[1, 0].set_ylabel('Expected Revenue')
    axes[1, 0].set_title('Revenue vs Price')
    
    # Expected Conversions vs Price
    axes[1, 1].plot(results_df['price'], results_df['expected_conversions'])
    axes[1, 1].axvline(optimization_results['optimal_price'], color='red', linestyle='--')
    axes[1, 1].set_xlabel('Price')
    axes[1, 1].set_ylabel('Expected Conversions')
    axes[1, 1].set_title('Expected Conversions vs Price')
    
    plt.tight_layout()
    plt.show()

def create_time_series_data(base_df, time_periods=12):
    """
    Create time series data for dynamic pricing.
    
    Parameters:
    -----------
    base_df : pd.DataFrame
        Base dataset
    time_periods : int
        Number of time periods
    
    Returns:
    --------
    pd.DataFrame: Time series dataset
    """
    
    time_series_data = []
    
    for t in range(time_periods):
        # Create time-varying effects
        seasonal_effect = np.sin(2 * np.pi * t / 12) * 0.1  # Seasonal variation
        trend_effect = t * 0.01  # Linear trend
        
        # Copy base data
        period_data = base_df.copy()
        period_data['time_period'] = t
        period_data['seasonal_effect'] = seasonal_effect
        period_data['trend_effect'] = trend_effect
        
        # Adjust prices for time effects
        period_data['price'] = period_data['price'] * (1 + seasonal_effect + trend_effect)
        
        # Adjust conversion probabilities
        period_data['conversion_probability'] = period_data['conversion_probability'] * (1 + seasonal_effect/2)
        period_data['conversion_probability'] = np.clip(period_data['conversion_probability'], 0.01, 0.99)
        
        # Regenerate conversions
        period_data['conversion'] = np.random.binomial(1, period_data['conversion_probability'])
        
        # Recalculate profit
        period_data['revenue'] = period_data['price'] * period_data['conversion']
        period_data['profit'] = (period_data['revenue'] - period_data['cost']) * period_data['conversion']
        
        time_series_data.append(period_data)
    
    return pd.concat(time_series_data, ignore_index=True)

# Print available functions
print("Available functions:")
print("- generate_synthetic_insurance_data(): Generate synthetic dataset")
print("- calculate_treatment_effects(): Calculate treatment effects")
print("- plot_treatment_effect(): Visualize treatment effects")
print("- calculate_profit_metrics(): Calculate business metrics")
print("- optimize_pricing_simple(): Simple pricing optimization")
print("- plot_pricing_optimization(): Plot optimization results")
print("- create_time_series_data(): Create time series data")
print("- set_style(): Set plotting style")

# Create and sort dictionary, then select top 2 keys
my_dict = {'a': 5, 'b': 2, 'c': 9}
sorted_items = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)
top_2_keys
