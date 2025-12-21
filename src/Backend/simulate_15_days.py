#!/usr/bin/env python3
"""
Multi-User Investment Simulation (15-Day Frequency)
Simulates 100 users investing every 15 days over 6 months with 2% platform fee.

User Distribution (Same daily equivalent rates):
- 50 users: $40/day rate -> $600 every 15 days
- 25 users: $10/day rate -> $150 every 15 days
- 25 users: $20/day rate -> $300 every 15 days
"""

from investment_engine import MicroInvestment
import csv

print("="*100)
print("MULTI-USER SIMULATION - EVERY 15 DAYS (180 DAYS TOTAL)")
print("="*100)

# Simulation parameters
SIMULATION_DAYS = 180  # 6 months
ANNUAL_RETURN_RATE = 0.08  # 8% annual return

# User distribution - Amounts adjusted for 15-day frequency
# calculating: daily_amount * 15
user_groups = [
    {'count': 50, 'daily_rate': 40.0, 'amount': 600.0, 'label': '$600/15days ($40/day)'},
    {'count': 25, 'daily_rate': 10.0, 'amount': 150.0, 'label': '$150/15days ($10/day)'},
    {'count': 25, 'daily_rate': 20.0, 'amount': 300.0, 'label': '$300/15days ($20/day)'}
]

print(f"\n📊 SIMULATION PARAMETERS")
print("-"*100)
print(f"Duration: {SIMULATION_DAYS} days (6 months)")
print(f"Frequency: Every 15 Days")
print(f"Frequency Count: {SIMULATION_DAYS // 15} investments per user")
print(f"Annual Return Rate: {ANNUAL_RETURN_RATE * 100}%")
print(f"Platform Fee: 2%")
print(f"Total Users: {sum(g['count'] for g in user_groups)}")

# Create all users
print(f"\n🚀 Creating {sum(g['count'] for g in user_groups)} user accounts...")
print("-"*100)

all_users = []
user_id = 1

for group in user_groups:
    for i in range(group['count']):
        investor = MicroInvestment(
            investment_amount=group['amount'],
            frequency='15_days',
            annual_return_rate=ANNUAL_RETURN_RATE
        )
        
        all_users.append({
            'user_id': user_id,
            'investor': investor,
            'amount': group['amount'],
            'daily_rate': group['daily_rate'],
            'label': group['label']
        })
        user_id += 1

print(f"✓ Created {len(all_users)} user accounts")

# Simulate 6 months for all users
print(f"\n⏳ Simulating {SIMULATION_DAYS} days of investing...")
print("-"*100)

for user_data in all_users:
    user_data['investor'].invest_for_days(SIMULATION_DAYS)

print(f"✓ Simulation complete!")

# Aggregate results by user group
print(f"\n📈 RESULTS BY USER GROUP")
print("="*100)

total_gross = 0
total_fees = 0
total_net = 0
total_portfolio_value = 0
total_returns = 0

for group in user_groups:
    # Get all users in this group (matching amount)
    group_users = [u for u in all_users if u['amount'] == group['amount']]
    
    # Aggregate metrics
    group_gross = sum(u['investor'].total_gross_invested for u in group_users)
    group_fees = sum(u['investor'].total_platform_fees for u in group_users)
    group_net = sum(u['investor'].total_invested for u in group_users)
    group_portfolio = sum(u['investor'].portfolio_value for u in group_users)
    group_returns = sum(u['investor'].get_total_return() for u in group_users)
    
    # Update totals
    total_gross += group_gross
    total_fees += group_fees
    total_net += group_net
    total_portfolio_value += group_portfolio
    total_returns += group_returns
    
    print(f"\n{group['label']} Users ({group['count']} users)")
    print("-"*100)
    print(f"  Gross Invested:       ${group_gross:>15,.2f}")
    print(f"  Platform Fees (2%):   ${group_fees:>15,.2f}")
    print(f"  Net Invested:         ${group_net:>15,.2f}")
    print(f"  Portfolio Value:      ${group_portfolio:>15,.2f}")
    print(f"  Total Returns:        ${group_returns:>15,.2f}")
    print(f"  Avg Return per User:  ${group_returns/group['count']:>15,.2f}")

# Platform-wide summary
print(f"\n💰 PLATFORM-WIDE SUMMARY (All 100 Users)")
print("="*100)
print(f"Total Gross Invested:     ${total_gross:>15,.2f}")
print(f"Total Platform Fees (2%): ${total_fees:>15,.2f}")
print(f"Total Net Invested:       ${total_net:>15,.2f}")
print(f"Total Portfolio Value:    ${total_portfolio_value:>15,.2f}")
print(f"Total Returns Generated:  ${total_returns:>15,.2f}")
print(f"Average ROI:              {(total_returns/total_net)*100:>15.2f}%")

# VestoFunds account
vesto_funds_balance = sum(u['investor'].vesto_main_funds for u in all_users)
print(f"\n🏦 VESTOFUNDS ACCOUNT (Platform Maintenance)")
print("="*100)
print(f"Total Fees Collected:     ${vesto_funds_balance:>15,.2f}")
print(f"Number of Transactions:   {sum(u['investor'].days_invested // 15 for u in all_users):>15,}")
print(f"Average Fee per User:     ${vesto_funds_balance/len(all_users):>15,.2f}")

# Generate per-user report
print(f"\n📊 GENERATING PER-USER CSV")
print("-" * 100)

csv_filename = 'user_returns_15_days.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['User ID', 'Investment Type', 'Amount per 15 Days', 'Gross Invested', 
                  'Platform Fees', 'Net Invested', 'Portfolio Value', 'Total Return', 'ROI %']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for u in all_users:
        inv = u['investor']
        writer.writerow({
            'User ID': u['user_id'],
            'Investment Type': u['label'],
            'Amount per 15 Days': f"${u['amount']:.2f}",
            'Gross Invested': inv.total_gross_invested,
            'Platform Fees': inv.total_platform_fees,
            'Net Invested': inv.total_invested,
            'Portfolio Value': inv.portfolio_value,
            'Total Return': inv.get_total_return(),
            'ROI %': inv.get_return_percentage()
        })

print(f"✓ Data exported to: {csv_filename}")

# Sample user comparison (Daily vs 15-Day)
print(f"\n⚖️ COMPARISON: DAILY VS 15-DAY (Sample $40/day user)")
print("="*100)
daily_sim_gross = 7200.00
daily_sim_return = 134.85
daily_sim_roi = 1.91

# Find a $600/15day user
sample = next(u['investor'] for u in all_users if u['amount'] == 600.0)
curr_gross = sample.total_gross_invested
curr_return = sample.get_total_return()
curr_roi = sample.get_return_percentage()

print(f"{'Metric':<20} {'Daily Sim':<15} {'15-Day Sim':<15} {'Difference':<15}")
print("-" * 65)
print(f"{'Gross Invested':<20} ${daily_sim_gross:<14,.2f} ${curr_gross:<14,.2f} ${curr_gross - daily_sim_gross:<14,.2f}")
print(f"{'Total Return':<20} ${daily_sim_return:<14,.2f} ${curr_return:<14,.2f} ${curr_return - daily_sim_return:<14,.2f}")
print(f"{'ROI':<20} {daily_sim_roi:<14.2f}% {curr_roi:<14.2f}% {curr_roi - daily_sim_roi:<14.2f}%")
print("-" * 65)
print("Note: 15-day investing has slightly lower returns due to")
print("delayed compounding (money sits idle for 14 days before investing)")

print("\n" + "="*100)
print("✨ SIMULATION COMPLETE!")
print("="*100)
