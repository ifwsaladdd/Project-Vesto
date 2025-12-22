#!/usr/bin/env python3
"""
Multi-User Investment Simulation
Simulates 100 users investing over 6 months with 2% platform fee.

User Distribution:
- 50 users: $40/day
- 25 users: $10/day
- 25 users: $20/day
"""

from investment_engine import MicroInvestment

print("="*90)
print("MULTI-USER INVESTMENT SIMULATION - 100 USERS OVER 6 MONTHS")
print("="*90)

# Simulation parameters
SIMULATION_DAYS = 180  # 6 months (approximately)
ANNUAL_RETURN_RATE = 0.08  # 8% annual return

# User distribution
user_groups = [
    {'count': 50, 'amount': 40.0, 'label': '$40/day'},
    {'count': 25, 'amount': 10.0, 'label': '$10/day'},
    {'count': 25, 'amount': 20.0, 'label': '$20/day'}
]

print(f"\n📊 SIMULATION PARAMETERS")
print("-"*90)
print(f"Duration: {SIMULATION_DAYS} days (6 months)")
print(f"Annual Return Rate: {ANNUAL_RETURN_RATE * 100}%")
print(f"Platform Fee: 2%")
print(f"Total Users: {sum(g['count'] for g in user_groups)}")
print()
print("User Distribution:")
for group in user_groups:
    print(f"  • {group['count']} users investing {group['label']}")

# Create all users
print(f"\n🚀 Creating {sum(g['count'] for g in user_groups)} user accounts...")
print("-"*90)

all_users = []
for group in user_groups:
    for i in range(group['count']):
        user = MicroInvestment(
            investment_amount=group['amount'],
            frequency='daily',
            annual_return_rate=ANNUAL_RETURN_RATE
        )
        all_users.append({
            'investor': user,
            'amount': group['amount'],
            'label': group['label']
        })

print(f"✓ Created {len(all_users)} user accounts")

# Simulate 6 months for all users
print(f"\n⏳ Simulating {SIMULATION_DAYS} days of investing...")
print("-"*90)

for user_data in all_users:
    user_data['investor'].invest_for_days(SIMULATION_DAYS)

print(f"✓ Simulation complete!")

# Aggregate results by user group
print(f"\n📈 RESULTS BY USER GROUP")
print("="*90)

total_gross = 0
total_fees = 0
total_net = 0
total_portfolio_value = 0
total_returns = 0

for group in user_groups:
    # Get all users in this group
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
    print("-"*90)
    print(f"  Gross Invested:       ${group_gross:>15,.2f}")
    print(f"  Platform Fees (2%):   ${group_fees:>15,.2f}")
    print(f"  Net Invested:         ${group_net:>15,.2f}")
    print(f"  Portfolio Value:      ${group_portfolio:>15,.2f}")
    print(f"  Total Returns:        ${group_returns:>15,.2f}")
    print(f"  Avg Return per User:  ${group_returns/group['count']:>15,.2f}")

# Platform-wide summary
print(f"\n💰 PLATFORM-WIDE SUMMARY (All 100 Users)")
print("="*90)
print(f"Total Gross Invested:     ${total_gross:>15,.2f}")
print(f"Total Platform Fees (2%): ${total_fees:>15,.2f}")
print(f"Total Net Invested:       ${total_net:>15,.2f}")
print(f"Total Portfolio Value:    ${total_portfolio_value:>15,.2f}")
print(f"Total Returns Generated:  ${total_returns:>15,.2f}")
print(f"Average ROI:              {(total_returns/total_net)*100:>15.2f}%")

# VestoFunds account
vesto_funds_balance = sum(u['investor'].vesto_main_funds for u in all_users)
print(f"\n🏦 VESTOFUNDS ACCOUNT (Platform Maintenance)")
print("="*90)
print(f"Total Fees Collected:     ${vesto_funds_balance:>15,.2f}")
print(f"Number of Transactions:   {sum(u['investor'].days_invested for u in all_users):>15,}")
print(f"Average Fee per User:     ${vesto_funds_balance/len(all_users):>15,.2f}")

# Verification
print(f"\n✅ VERIFICATION")
print("="*90)
expected_daily_gross = (50 * 40) + (25 * 10) + (25 * 20)
expected_total_gross = expected_daily_gross * SIMULATION_DAYS
expected_total_fees = expected_total_gross * 0.02
expected_total_net = expected_total_gross - expected_total_fees

print(f"Expected daily gross: ${expected_daily_gross:,.2f}")
print(f"Expected total gross (6 months): ${expected_total_gross:,.2f}")
print(f"Expected total fees (2%): ${expected_total_fees:,.2f}")
print(f"Expected total net: ${expected_total_net:,.2f}")
print()
print(f"Actual total gross: ${total_gross:,.2f} {'✓' if abs(total_gross - expected_total_gross) < 0.01 else '✗'}")
print(f"Actual total fees: ${total_fees:,.2f} {'✓' if abs(total_fees - expected_total_fees) < 0.01 else '✗'}")
print(f"Actual total net: ${total_net:,.2f} {'✓' if abs(total_net - expected_total_net) < 0.01 else '✗'}")
print(f"VestoFunds balance: ${vesto_funds_balance:,.2f} {'✓' if abs(vesto_funds_balance - expected_total_fees) < 0.01 else '✗'}")

# Individual user examples
print(f"\n👤 SAMPLE INDIVIDUAL USER RESULTS")
print("="*90)

for group in user_groups:
    # Get first user from each group
    sample_user = next(u for u in all_users if u['amount'] == group['amount'])
    investor = sample_user['investor']
    
    print(f"\nSample {group['label']} User:")
    print("-"*90)
    print(f"  Gross Invested:       ${investor.total_gross_invested:>12,.2f}")
    print(f"  Platform Fees:        ${investor.total_platform_fees:>12,.2f}")
    print(f"  Net Invested:         ${investor.total_invested:>12,.2f}")
    print(f"  Portfolio Value:      ${investor.portfolio_value:>12,.2f}")
    print(f"  Total Return:         ${investor.get_total_return():>12,.2f}")
    print(f"  ROI:                  {investor.get_return_percentage():>12.2f}%")

# Key insights
print(f"\n💡 KEY INSIGHTS")
print("="*90)
print(f"1. Platform Revenue (VestoFunds): ${vesto_funds_balance:,.2f}")
print(f"2. Total User Portfolios: ${total_portfolio_value:,.2f}")
print(f"3. Total Returns Generated: ${total_returns:,.2f}")
print(f"4. Platform Fee Percentage: {(total_fees/total_gross)*100:.2f}%")
print(f"5. Average User Portfolio: ${total_portfolio_value/len(all_users):,.2f}")
print(f"6. Average User Return: ${total_returns/len(all_users):,.2f}")
print(f"7. Daily Platform Revenue: ${vesto_funds_balance/SIMULATION_DAYS:,.2f}")
print(f"8. Monthly Platform Revenue: ${(vesto_funds_balance/SIMULATION_DAYS)*30:,.2f}")

# Growth projection
print(f"\n📊 GROWTH PROJECTION")
print("="*90)
print("If this trend continues for 1 year:")
annual_vesto_funds = (vesto_funds_balance / SIMULATION_DAYS) * 365
annual_user_portfolios = (total_portfolio_value / SIMULATION_DAYS) * 365
print(f"  Projected VestoFunds (1 year): ${annual_vesto_funds:,.2f}")
print(f"  Projected User Portfolios (1 year): ${annual_user_portfolios:,.2f}")

print("\n" + "="*90)
print("✨ SIMULATION COMPLETE!")
print("="*90)
print("\nSummary:")
print(f"  • {len(all_users)} users invested over {SIMULATION_DAYS} days")
print(f"  • ${total_gross:,.2f} total gross investments")
print(f"  • ${vesto_funds_balance:,.2f} collected in platform fees")
print(f"  • ${total_returns:,.2f} in returns generated for users")
print(f"  • All fees properly segregated in VestoFunds account")
print("="*90)
