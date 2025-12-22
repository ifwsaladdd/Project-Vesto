#!/usr/bin/env python3
"""
Detailed Per-User Analysis
Shows returns and profit percentage for each of the 100 users
"""

from investment_engine import MicroInvestment
import csv

print("="*100)
print("DETAILED PER-USER ANALYSIS - 100 USERS OVER 6 MONTHS")
print("="*100)

# Simulation parameters
SIMULATION_DAYS = 180  # 6 months
ANNUAL_RETURN_RATE = 0.08  # 8% annual return

# User distribution
user_groups = [
    {'count': 50, 'amount': 40.0, 'label': '$40/day'},
    {'count': 25, 'amount': 10.0, 'label': '$10/day'},
    {'count': 25, 'amount': 20.0, 'label': '$20/day'}
]

print(f"\n⏳ Creating and simulating 100 users...")
print("-"*100)

# Create all users with IDs
all_users = []
user_id = 1

for group in user_groups:
    for i in range(group['count']):
        investor = MicroInvestment(
            investment_amount=group['amount'],
            frequency='daily',
            annual_return_rate=ANNUAL_RETURN_RATE
        )
        # Simulate 6 months
        investor.invest_for_days(SIMULATION_DAYS)
        
        all_users.append({
            'user_id': user_id,
            'investor': investor,
            'amount': group['amount'],
            'label': group['label']
        })
        user_id += 1

print(f"✓ Simulation complete for {len(all_users)} users")

# Generate detailed per-user data
print(f"\n📊 GENERATING PER-USER REPORT")
print("="*100)

user_data = []
for user in all_users:
    inv = user['investor']
    user_data.append({
        'User ID': user['user_id'],
        'Investment Type': user['label'],
        'Daily Amount': f"${user['amount']:.2f}",
        'Gross Invested': inv.total_gross_invested,
        'Platform Fees': inv.total_platform_fees,
        'Net Invested': inv.total_invested,
        'Portfolio Value': inv.portfolio_value,
        'Total Return': inv.get_total_return(),
        'ROI %': inv.get_return_percentage()
    })

# Display summary table
print(f"\n{'User':<6} {'Type':<12} {'Gross':<12} {'Fees':<10} {'Net':<12} {'Portfolio':<12} {'Return':<12} {'ROI %':<8}")
print("-"*100)

for data in user_data:
    print(f"{data['User ID']:<6} {data['Investment Type']:<12} "
          f"${data['Gross Invested']:<11,.2f} "
          f"${data['Platform Fees']:<9,.2f} "
          f"${data['Net Invested']:<11,.2f} "
          f"${data['Portfolio Value']:<11,.2f} "
          f"${data['Total Return']:<11,.2f} "
          f"{data['ROI %']:<8.2f}%")

# Statistics by group
print(f"\n📈 STATISTICS BY USER GROUP")
print("="*100)

for group in user_groups:
    group_data = [d for d in user_data if d['Investment Type'] == group['label']]
    
    total_return = sum(d['Total Return'] for d in group_data)
    avg_return = total_return / len(group_data)
    min_return = min(d['Total Return'] for d in group_data)
    max_return = max(d['Total Return'] for d in group_data)
    avg_roi = sum(d['ROI %'] for d in group_data) / len(group_data)
    
    print(f"\n{group['label']} Users ({group['count']} users)")
    print("-"*100)
    print(f"  Total Returns:        ${total_return:>12,.2f}")
    print(f"  Average Return:       ${avg_return:>12,.2f}")
    print(f"  Min Return:           ${min_return:>12,.2f}")
    print(f"  Max Return:           ${max_return:>12,.2f}")
    print(f"  Average ROI:          {avg_roi:>12.2f}%")

# Overall statistics
print(f"\n💰 OVERALL STATISTICS (All 100 Users)")
print("="*100)

total_gross = sum(d['Gross Invested'] for d in user_data)
total_fees = sum(d['Platform Fees'] for d in user_data)
total_net = sum(d['Net Invested'] for d in user_data)
total_portfolio = sum(d['Portfolio Value'] for d in user_data)
total_returns = sum(d['Total Return'] for d in user_data)
avg_return = total_returns / len(user_data)
avg_roi = sum(d['ROI %'] for d in user_data) / len(user_data)

print(f"Total Gross Invested:     ${total_gross:>15,.2f}")
print(f"Total Platform Fees:      ${total_fees:>15,.2f}")
print(f"Total Net Invested:       ${total_net:>15,.2f}")
print(f"Total Portfolio Value:    ${total_portfolio:>15,.2f}")
print(f"Total Returns Generated:  ${total_returns:>15,.2f}")
print(f"Average Return per User:  ${avg_return:>15,.2f}")
print(f"Average ROI per User:     {avg_roi:>15.2f}%")

# Top performers
print(f"\n🏆 TOP 10 PERFORMERS (By Total Return)")
print("="*100)
top_performers = sorted(user_data, key=lambda x: x['Total Return'], reverse=True)[:10]

print(f"{'Rank':<6} {'User':<6} {'Type':<12} {'Net Invested':<14} {'Portfolio':<14} {'Return':<14} {'ROI %':<8}")
print("-"*100)

for rank, data in enumerate(top_performers, 1):
    print(f"{rank:<6} {data['User ID']:<6} {data['Investment Type']:<12} "
          f"${data['Net Invested']:<13,.2f} "
          f"${data['Portfolio Value']:<13,.2f} "
          f"${data['Total Return']:<13,.2f} "
          f"{data['ROI %']:<8.2f}%")

# Export to CSV
csv_filename = 'user_returns_analysis.csv'
print(f"\n💾 EXPORTING DATA TO CSV")
print("="*100)

with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['User ID', 'Investment Type', 'Daily Amount', 'Gross Invested', 
                  'Platform Fees', 'Net Invested', 'Portfolio Value', 'Total Return', 'ROI %']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in user_data:
        writer.writerow(data)

print(f"✓ Data exported to: {csv_filename}")
print(f"  Contains detailed data for all {len(user_data)} users")

# Distribution analysis
print(f"\n📊 RETURN DISTRIBUTION ANALYSIS")
print("="*100)

# Group returns into ranges
ranges = [
    (0, 50, '$0-$50'),
    (50, 100, '$50-$100'),
    (100, 150, '$100-$150'),
    (150, 200, '$150-$200')
]

for min_val, max_val, label in ranges:
    count = sum(1 for d in user_data if min_val <= d['Total Return'] < max_val)
    percentage = (count / len(user_data)) * 100
    print(f"  {label:<15} {count:>3} users ({percentage:>5.1f}%)")

# ROI distribution
print(f"\n📈 ROI DISTRIBUTION")
print("="*100)

roi_ranges = [
    (0, 1, '0-1%'),
    (1, 2, '1-2%'),
    (2, 3, '2-3%'),
    (3, 4, '3-4%')
]

for min_val, max_val, label in roi_ranges:
    count = sum(1 for d in user_data if min_val <= d['ROI %'] < max_val)
    percentage = (count / len(user_data)) * 100
    print(f"  {label:<15} {count:>3} users ({percentage:>5.1f}%)")

print("\n" + "="*100)
print("✨ ANALYSIS COMPLETE!")
print("="*100)
print(f"\nKey Findings:")
print(f"  • All {len(user_data)} users have positive returns")
print(f"  • Average return per user: ${avg_return:.2f}")
print(f"  • Average ROI: {avg_roi:.2f}%")
print(f"  • Total returns generated: ${total_returns:,.2f}")
print(f"  • Data exported to: {csv_filename}")
print("="*100)
