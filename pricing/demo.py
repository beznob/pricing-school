#!/usr/bin/env python3
"""
Test script to demonstrate the insurance pricing with causal inference project.
This script shows how to use the utilities and generate synthetic data.
"""

# Add current directory to Python path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    generate_synthetic_insurance_data,
    calculate_profit_metrics,
    optimize_pricing_simple,
    plot_pricing_optimization,
    set_style
)

def main():
    """Main function to demonstrate the pricing framework."""
    print("=" * 60)
    print("INSURANCE PRICING WITH CAUSAL INFERENCE - DEMO")
    print("=" * 60)
    
    # Set up styling
    set_style()
    
    # Generate synthetic data
    print("\n1. Generating synthetic insurance dataset...")
    df = generate_synthetic_insurance_data(n_samples=5000)
    print(f"Generated dataset with {len(df)} customers")
    
    # Display basic statistics
    print("\n2. Basic Dataset Statistics:")
    print(f"   - Average age: {df['age'].mean():.1f} years")
    print(f"   - Average income: ${df['income'].mean():,.0f}")
    print(f"   - Average price: ${df['price'].mean():.2f}")
    print(f"   - Conversion rate: {df['conversion'].mean():.2%}")
    print(f"   - Average profit per customer: ${df['profit'].mean():.2f}")
    
    # Calculate P&L metrics
    print("\n3. Profit & Loss Analysis:")
    pnl_metrics = calculate_profit_metrics(df)
    print(f"   - Total revenue: ${pnl_metrics['total_revenue']:,.2f}")
    print(f"   - Total profit: ${pnl_metrics['total_profit']:,.2f}")
    print(f"   - Profit margin: {pnl_metrics['profit_margin']:.2%}")
    print(f"   - Average CLV: ${pnl_metrics['average_clv']:,.2f}")
    
    # Demonstrate pricing optimization
    print("\n4. Pricing Optimization:")
    opt_results = optimize_pricing_simple(df, price_range=(200, 2000), n_points=50)
    print(f"   - Current average price: ${df['price'].mean():.2f}")
    print(f"   - Optimal price: ${opt_results['optimal_price']:.2f}")
    print(f"   - Expected profit improvement: ${opt_results['optimal_profit'] - df['profit'].sum():,.2f}")
    
    # Show price sensitivity analysis
    print("\n5. Price Sensitivity Analysis:")
    price_quartiles = pd.qcut(df['price'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    conversion_by_price = df.groupby(price_quartiles)['conversion'].mean()
    print("   Conversion rates by price quartile:")
    for quartile, rate in conversion_by_price.items():
        print(f"   - {quartile}: {rate:.2%}")
    
    # Regional analysis
    print("\n6. Regional Analysis:")
    regional_metrics = df.groupby('region').agg({
        'conversion': 'mean',
        'price': 'mean',
        'profit': 'mean'
    }).round(3)
    print(regional_metrics)
    
    # Risk-based analysis
    print("\n7. Risk-Based Analysis:")
    df['risk_category'] = pd.cut(df['risk_score'], 
                                bins=[0, 33, 66, 100], 
                                labels=['Low', 'Medium', 'High'])
    risk_metrics = df.groupby('risk_category').agg({
        'conversion': 'mean',
        'price': 'mean',
        'profit': 'mean'
    }).round(3)
    print(risk_metrics)
    
    # Save sample data for further analysis
    sample_data = df.head(1000)
    sample_data.to_csv('sample_insurance_data.csv', index=False)
    print(f"\n8. Sample data saved to 'sample_insurance_data.csv'")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open 01_data_generation.ipynb in Jupyter to run the full analysis")
    print("2. Explore the other notebooks for advanced pricing techniques")
    print("3. Modify the parameters in utils.py to test different scenarios")
    print("4. Check the README.md for detailed explanations")

if __name__ == "__main__":
    main()
