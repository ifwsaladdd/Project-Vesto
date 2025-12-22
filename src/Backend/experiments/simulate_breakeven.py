from investment_engine import MicroInvestment

def simulate_breakeven_scenario():
    print("Running Simulation: 6% ROI vs 6% Inflation")
    print("------------------------------------------")
    
    # Configuration
    investment_amount = 10.0
    frequency = 'daily'
    roi = 0.06
    inflation = 0.03
    duration = 365
    
    investor = MicroInvestment(
        investment_amount=investment_amount, 
        frequency=frequency, 
        annual_return_rate=roi,
        annual_inflation_rate=inflation
    )
    
    # Run Simulation
    investor.invest_for_days(duration)
    
    summary = investor.get_summary()
    
    print(f"\nSimulation Results ({duration} days)")
    print(f"Invested: ${summary['investment_amount']} {summary['frequency']}")
    print(f"Annual ROI: {summary['annual_return_rate']}%")
    print(f"Annual Inflation: {summary['annual_inflation_rate']}%")
    print("\n--- Insights ---")
    
    # 1. Nominal Value
    print(f"1. Nominal Portfolio Value: ${summary['portfolio_value']:,.2f}")
    print(f"   (Nominal Profit: ${summary['total_return']:,.2f})")
    
    # 2. Real ROI
    print(f"2. Real ROI: {summary['real_return_percentage']:.4f}%")
    print(f"   (Real Portfolio Value: ${summary['real_portfolio_value']:,.2f})")
    print(f"   (Real Profit: ${summary['real_total_return']:,.2f})")
    
    # 3. Profit/Loss % (Nominal)
    print(f"3. Profit/Loss % (Nominal): {summary['return_percentage']:.4f}%")
    
    print("\nAnalysis:")
    if summary['real_return_percentage'] < 0:
        print("Note: Even though Nominal Profit is positive, Real Return is negative because of fees/timing.")
    elif abs(summary['real_return_percentage']) < 0.1:
        print("Result: Effectively breaking even in real terms (close to 0%).")
    else:
        print("Result: Positive real return.")

if __name__ == "__main__":
    simulate_breakeven_scenario()
