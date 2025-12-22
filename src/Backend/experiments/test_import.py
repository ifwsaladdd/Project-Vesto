import sys
import io
from investment_engine import MicroInvestment

def test_engine():
    # Capture stdout to ensure no printing
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        # Instantiate
        investor = MicroInvestment(
            investment_amount=10.0, 
            frequency='daily', 
            annual_return_rate=0.08, 
            annual_inflation_rate=0.03
        )
        
        # Run simulation
        investor.invest_for_days(30)
        
        # Check summary
        summary = investor.get_summary()
        
        # Check required keys in summary
        required_keys = [
            'total_gross_invested', 'total_net_invested', 
            'portfolio_value', 'real_portfolio_value', 
            'return_percentage', 'real_return_percentage'
        ]
        
        for key in required_keys:
            if key not in summary:
                raise ValueError(f"Missing key in summary: {key}")
        
        # Check values are structurally correct (basic type check)
        if not isinstance(summary['portfolio_value'], (int, float)):
             raise ValueError("Portfolio value should be a number")
            
        sys.stdout = sys.__stdout__
        
        # Check if anything was printed
        if captured_output.getvalue().strip():
            print("❌ FAILURE: Engine printed to stdout!")
            print("Captured:", captured_output.getvalue())
        else:
            print("✅ SUCCESS: Engine ran silently and produced valid data.")
            print(f"   Sample Output: Portfolio={summary['portfolio_value']}, Real ROI={summary['real_return_percentage']}%")
            
    except Exception as e:
        sys.stdout = sys.__stdout__
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_engine()
