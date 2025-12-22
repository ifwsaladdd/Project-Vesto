from investment_engine import MicroInvestment

def verify_inflation_tracking():
    print("Verifying Inflation Tracking...")
    
    # Setup: 8% Nominal Return, 3% Inflation
    # Daily investment of $10
    investor = MicroInvestment(
        investment_amount=10.0, 
        frequency='daily', 
        annual_return_rate=0.08,
        annual_inflation_rate=0.03
    )
    
    print("\nSimulating 365 days...")
    investor.invest_for_days(365)
    
    investor.print_summary()
    
    summary = investor.get_summary()
    
    # Verification Checks
    print("\n--- Verification Checks ---")
    
    # 1. Nominal ROI should be approx 4% (since investments are staggered over the year, ~half the full year rate)
    # Actually, if we invest daily, the average age of money is ~6 months.
    # So we expect roughly 4% return on the total principal.
    print(f"Nominal Return %: {summary['return_percentage']}% (Expected approx 4.0%)")
    
    # 2. Real ROI
    # Real Rate ~ (1.08 / 1.03) - 1 = 4.85%
    # Average age ~ 6 months -> Expected Real ROI ~ 2.4%
    print(f"Real Return %: {summary['real_return_percentage']}% (Expected approx 2.4%)")
    
    # 3. Real Invested < Nominal Invested
    print(f"Nominal Net Invested: ${summary['total_net_invested']}")
    print(f"Real Net Invested:    ${summary['total_real_invested']}")
    if summary['total_real_invested'] < summary['total_net_invested']:
        print("✅ Real Invested is less than Nominal Invested (Correct)")
    else:
        print("❌ Error: Real Invested should be less than Nominal Invested")

    # 4. Real Portfolio Value < Nominal Portfolio Value
    if summary['real_portfolio_value'] < summary['portfolio_value']:
        print("✅ Real Portfolio Value is less than Nominal Portfolio Value (Correct)")
    else:
        print("❌ Error: Real Portfolio Value should be less than Nominal Portfolio Value")

if __name__ == "__main__":
    verify_inflation_tracking()
