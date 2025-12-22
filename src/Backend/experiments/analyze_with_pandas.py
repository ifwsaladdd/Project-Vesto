#!/usr/bin/env python3
"""
Per-User Returns Analysis using Pandas and NumPy
Displays comprehensive user data in DataFrame format
"""

import pandas as pd
import numpy as np
from investment_engine import MicroInvestment

print("="*100)
print("PER-USER RETURNS ANALYSIS - Using Pandas & NumPy")
print("="*100)

# Simulation parameters
SIMULATION_DAYS = 180
ANNUAL_RETURN_RATE = 0.08

# User distribution
user_groups = [
    {'count': 50, 'amount': 40.0, 'label': '$40/day'},
    {'count': 25, 'amount': 10.0, 'label': '$10/day'},
    {'count': 25, 'amount': 20.0, 'label': '$20/day'}
]

print(f"\n⏳ Simulating 100 users over {SIMULATION_DAYS} days...")
print("-"*100)

# Create all users and simulate
user_data_list = []
user_id = 1

for group in user_groups:
    for i in range(group['count']):
        investor = MicroInvestment(
            investment_amount=group['amount'],
            frequency='daily',
            annual_return_rate=ANNUAL_RETURN_RATE
        )
        investor.invest_for_days(SIMULATION_DAYS)
        
        user_data_list.append({
            'User_ID': user_id,
            'Investment_Type': group['label'],
            'Daily_Amount': group['amount'],
            'Gross_Invested': investor.total_gross_invested,
            'Platform_Fees': investor.total_platform_fees,
            'Net_Invested': investor.total_invested,
            'Portfolio_Value': investor.portfolio_value,
            'Total_Return': investor.get_total_return(),
            'ROI_Percent': investor.get_return_percentage()
        })
        user_id += 1

print(f"✓ Simulation complete!")

# Create pandas DataFrame
df = pd.DataFrame(user_data_list)

# Display full DataFrame
print(f"\n📊 COMPLETE USER DATA (All 100 Users)")
print("="*100)
print(df.to_string(index=False))

# Summary statistics by group
print(f"\n\n📈 SUMMARY STATISTICS BY GROUP")
print("="*100)

summary_by_group = df.groupby('Investment_Type').agg({
    'User_ID': 'count',
    'Gross_Invested': ['sum', 'mean'],
    'Platform_Fees': ['sum', 'mean'],
    'Net_Invested': ['sum', 'mean'],
    'Portfolio_Value': ['sum', 'mean'],
    'Total_Return': ['sum', 'mean', 'min', 'max'],
    'ROI_Percent': ['mean', 'std']
}).round(2)

summary_by_group.columns = ['_'.join(col).strip() for col in summary_by_group.columns.values]
print(summary_by_group)

# Overall statistics
print(f"\n\n💰 OVERALL STATISTICS")
print("="*100)

overall_stats = pd.DataFrame({
    'Metric': [
        'Total Users',
        'Total Gross Invested',
        'Total Platform Fees',
        'Total Net Invested',
        'Total Portfolio Value',
        'Total Returns Generated',
        'Average Return per User',
        'Average ROI',
        'Min Return',
        'Max Return',
        'Std Dev of Returns'
    ],
    'Value': [
        len(df),
        f"${df['Gross_Invested'].sum():,.2f}",
        f"${df['Platform_Fees'].sum():,.2f}",
        f"${df['Net_Invested'].sum():,.2f}",
        f"${df['Portfolio_Value'].sum():,.2f}",
        f"${df['Total_Return'].sum():,.2f}",
        f"${df['Total_Return'].mean():,.2f}",
        f"{df['ROI_Percent'].mean():.2f}%",
        f"${df['Total_Return'].min():,.2f}",
        f"${df['Total_Return'].max():,.2f}",
        f"${df['Total_Return'].std():,.2f}"
    ]
})

print(overall_stats.to_string(index=False))

# Top 10 performers
print(f"\n\n🏆 TOP 10 PERFORMERS")
print("="*100)

top_10 = df.nlargest(10, 'Total_Return')[['User_ID', 'Investment_Type', 'Net_Invested', 
                                            'Portfolio_Value', 'Total_Return', 'ROI_Percent']]
print(top_10.to_string(index=False))

# Distribution analysis using numpy
print(f"\n\n📊 RETURN DISTRIBUTION ANALYSIS (Using NumPy)")
print("="*100)

returns = df['Total_Return'].values

# Create bins for distribution
bins = [0, 50, 100, 150, 200]
labels = ['$0-$50', '$50-$100', '$100-$150', '$150-$200']

distribution = pd.cut(df['Total_Return'], bins=bins, labels=labels, include_lowest=True)
dist_counts = distribution.value_counts().sort_index()

dist_df = pd.DataFrame({
    'Return Range': dist_counts.index,
    'User Count': dist_counts.values,
    'Percentage': (dist_counts.values / len(df) * 100).round(1)
})

print(dist_df.to_string(index=False))

# NumPy statistics
print(f"\n\n📈 NUMPY STATISTICAL ANALYSIS")
print("="*100)

numpy_stats = pd.DataFrame({
    'Statistic': [
        'Mean Return',
        'Median Return',
        'Std Deviation',
        '25th Percentile',
        '75th Percentile',
        'Min Return',
        'Max Return',
        'Range',
        'Variance'
    ],
    'Value': [
        f"${np.mean(returns):.2f}",
        f"${np.median(returns):.2f}",
        f"${np.std(returns):.2f}",
        f"${np.percentile(returns, 25):.2f}",
        f"${np.percentile(returns, 75):.2f}",
        f"${np.min(returns):.2f}",
        f"${np.max(returns):.2f}",
        f"${np.ptp(returns):.2f}",
        f"${np.var(returns):.2f}"
    ]
})

print(numpy_stats.to_string(index=False))

# Correlation analysis
print(f"\n\n🔗 CORRELATION ANALYSIS")
print("="*100)

correlation_df = df[['Daily_Amount', 'Gross_Invested', 'Platform_Fees', 
                      'Net_Invested', 'Portfolio_Value', 'Total_Return', 'ROI_Percent']].corr()

print("Correlation Matrix:")
print(correlation_df.round(3))

# Export to Excel
excel_filename = 'user_returns_analysis.xlsx'
print(f"\n\n💾 EXPORTING TO EXCEL")
print("="*100)

with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
    # Sheet 1: All user data
    df.to_excel(writer, sheet_name='All Users', index=False)
    
    # Sheet 2: Summary by group
    summary_by_group.to_excel(writer, sheet_name='Group Summary')
    
    # Sheet 3: Overall statistics
    overall_stats.to_excel(writer, sheet_name='Overall Stats', index=False)
    
    # Sheet 4: Top performers
    top_10.to_excel(writer, sheet_name='Top 10', index=False)
    
    # Sheet 5: Distribution
    dist_df.to_excel(writer, sheet_name='Distribution', index=False)
    
    # Sheet 6: Correlation matrix
    correlation_df.to_excel(writer, sheet_name='Correlations')

print(f"✓ Data exported to: {excel_filename}")
print(f"  Contains 6 sheets: All Users, Group Summary, Overall Stats, Top 10, Distribution, Correlations")

# Save DataFrame to CSV as well
csv_filename = 'user_returns_pandas.csv'
df.to_csv(csv_filename, index=False)
print(f"✓ Data also saved to: {csv_filename}")

print("\n" + "="*100)
print("✨ ANALYSIS COMPLETE!")
print("="*100)
print(f"\nDataFrame Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Total Returns: ${df['Total_Return'].sum():,.2f}")
print(f"Average ROI: {df['ROI_Percent'].mean():.2f}%")
print(f"All users profitable: {(df['Total_Return'] > 0).all()}")
print("="*100)
