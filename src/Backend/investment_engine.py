from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class MicroInvestment:
    
    def __init__(self, daily_investment, annual_return_rate=0.08):
        """
        Initialize the micro-investment simulator.
        
        Args:
            daily_investment (float): Amount to invest each day
            annual_return_rate (float): Annual return rate (default: 0.08 for 8%)
        """
        self.daily_investment = daily_investment
        self.annual_return_rate = annual_return_rate
        self.total_invested = 0.0
        self.portfolio_value = 0.0
        self.days_invested = 0
        self.transaction_history = []  # List to store all transactions
        self.start_date = datetime.now()  # Track when investing started
        
        # Calculate daily return rate from annual rate
        # Using compound interest formula: (1 + annual_rate)^(1/365) - 1
        self.daily_return_rate = (1 + annual_return_rate) ** (1/365) - 1
    
    def invest_daily(self):
        """
        Simulate one day of investment.
        - Adds the daily investment amount
        - Applies daily compounding to the existing portfolio
        - Records transaction in history
        """
        # Store portfolio value before today's activity
        portfolio_before = self.portfolio_value
        
        # Apply daily compounding to existing portfolio
        self.portfolio_value *= (1 + self.daily_return_rate)
        daily_return = self.portfolio_value - portfolio_before
        
        # Add today's investment
        self.portfolio_value += self.daily_investment
        self.total_invested += self.daily_investment
        self.days_invested += 1
        
        # Record transaction
        transaction_date = self.start_date + timedelta(days=self.days_invested - 1)
        transaction = {
            'day': self.days_invested,
            'date': transaction_date.strftime('%Y-%m-%d'),
            'investment_amount': self.daily_investment,
            'portfolio_before': round(portfolio_before, 2),
            'daily_return': round(daily_return, 2),
            'portfolio_after': round(self.portfolio_value, 2),
            'total_invested': round(self.total_invested, 2)
        }
        self.transaction_history.append(transaction)
    
    def invest_for_days(self, num_days):
        """
        Simulate investing for multiple days.
        
        Args:
            num_days (int): Number of days to simulate
        """
        for _ in range(num_days):
            self.invest_daily()
    
    def get_total_return(self):
        """
        Calculate total return (profit/loss).
        
        Returns:
            float: Total return amount
        """
        return self.portfolio_value - self.total_invested
    
    def get_return_percentage(self):
        """
        Calculate return as a percentage.
        
        Returns:
            float: Return percentage (0 if nothing invested yet)
        """
        if self.total_invested == 0:
            return 0.0
        return (self.get_total_return() / self.total_invested) * 100
    
    def get_summary(self):
        """
        Get a summary of the investment.
        
        Returns:
            dict: Dictionary containing investment summary
        """
        return {
            'days_invested': self.days_invested,
            'daily_investment': self.daily_investment,
            'total_invested': round(self.total_invested, 2),
            'portfolio_value': round(self.portfolio_value, 2),
            'total_return': round(self.get_total_return(), 2),
            'return_percentage': round(self.get_return_percentage(), 2),
            'annual_return_rate': self.annual_return_rate * 100
        }
    
    def print_summary(self):
        """
        Print a formatted summary of the investment.
        """
        summary = self.get_summary()
        print("\n" + "="*50)
        print("MICRO-INVESTMENT SUMMARY")
        print("="*50)
        print(f"Days Invested:        {summary['days_invested']}")
        print(f"Daily Investment:     ${summary['daily_investment']:.2f}")
        print(f"Annual Return Rate:   {summary['annual_return_rate']:.1f}%")
        print("-"*50)
        print(f"Total Invested:       ${summary['total_invested']:.2f}")
        print(f"Portfolio Value:      ${summary['portfolio_value']:.2f}")
        print(f"Total Return:         ${summary['total_return']:.2f}")
        print(f"Return Percentage:    {summary['return_percentage']:.2f}%")
        print("="*50 + "\n")
    
    def get_transaction_history(self, last_n=None):
        """
        Get transaction history.
        
        Args:
            last_n (int, optional): Return only the last N transactions
        
        Returns:
            list: List of transaction dictionaries
        """
        if last_n is None:
            return self.transaction_history
        return self.transaction_history[-last_n:]
    
    def print_transaction_history(self, last_n=10):
        """
        Print formatted transaction history.
        
        Args:
            last_n (int): Number of recent transactions to display (default: 10)
        """
        transactions = self.get_transaction_history(last_n)
        
        if not transactions:
            print("No transactions yet.")
            return
        
        print("\n" + "="*80)
        print(f"TRANSACTION HISTORY (Last {len(transactions)} transactions)")
        print("="*80)
        print(f"{'Day':<6} {'Date':<12} {'Invested':<12} {'Daily Return':<14} {'Portfolio':<14} {'Total Invested':<15}")
        print("-"*80)
        
        for txn in transactions:
            print(f"{txn['day']:<6} {txn['date']:<12} ${txn['investment_amount']:<11.2f} "
                  f"${txn['daily_return']:<13.2f} ${txn['portfolio_after']:<13.2f} "
                  f"${txn['total_invested']:<14.2f}")
        
        print("="*80 + "\n")
    
    def get_portfolio_dashboard(self):
        """
        Get comprehensive portfolio dashboard data.
        
        Returns:
            dict: Dashboard data including metrics and weekly summaries
        """
        # Calculate key metrics
        net_profit = self.get_total_return()
        roi_percentage = self.get_return_percentage()
        
        # Calculate weekly summaries
        weekly_data = []
        week_num = 1
        
        for i in range(0, len(self.transaction_history), 7):
            week_transactions = self.transaction_history[i:i+7]
            if week_transactions:
                last_txn = week_transactions[-1]
                weekly_data.append({
                    'week': week_num,
                    'end_date': last_txn['date'],
                    'total_invested': last_txn['total_invested'],
                    'portfolio_value': last_txn['portfolio_after'],
                    'weekly_return': sum(txn['daily_return'] for txn in week_transactions)
                })
                week_num += 1
        
        return {
            'total_invested': round(self.total_invested, 2),
            'portfolio_value': round(self.portfolio_value, 2),
            'net_profit': round(net_profit, 2),
            'roi_percentage': round(roi_percentage, 2),
            'days_invested': self.days_invested,
            'daily_investment': self.daily_investment,
            'annual_return_rate': self.annual_return_rate * 100,
            'weekly_data': weekly_data
        }
    
    def print_dashboard(self):
        """
        Print a comprehensive portfolio dashboard.
        """
        dashboard = self.get_portfolio_dashboard()
        
        print("\n" + "="*60)
        print("📊 PORTFOLIO DASHBOARD")
        print("="*60)
        
        # Key Metrics Section
        print("\n💰 KEY METRICS")
        print("-"*60)
        print(f"  Total Invested:        ${dashboard['total_invested']:>12,.2f}")
        print(f"  Portfolio Value:       ${dashboard['portfolio_value']:>12,.2f}")
        print(f"  Net Profit:            ${dashboard['net_profit']:>12,.2f}")
        print(f"  Return on Investment:   {dashboard['roi_percentage']:>11.2f}%")
        
        # Investment Details
        print("\n📈 INVESTMENT DETAILS")
        print("-"*60)
        print(f"  Days Invested:          {dashboard['days_invested']:>12}")
        print(f"  Daily Investment:      ${dashboard['daily_investment']:>12,.2f}")
        print(f"  Annual Return Rate:     {dashboard['annual_return_rate']:>11.1f}%")
        
        # Weekly Performance (last 4 weeks)
        if dashboard['weekly_data']:
            print("\n📅 RECENT WEEKLY PERFORMANCE (Last 4 weeks)")
            print("-"*60)
            print(f"{'Week':<6} {'Date':<12} {'Invested':<14} {'Portfolio':<14} {'Weekly Return':<15}")
            print("-"*60)
            
            recent_weeks = dashboard['weekly_data'][-4:]
            for week in recent_weeks:
                print(f"{week['week']:<6} {week['end_date']:<12} "
                      f"${week['total_invested']:<13,.2f} "
                      f"${week['portfolio_value']:<13,.2f} "
                      f"${week['weekly_return']:<14.2f}")
        
        print("\n" + "="*60 + "\n")
    
    def plot_weekly_growth(self, save_path=None):
        """
        Generate a graph showing weekly investment growth.
        
        Args:
            save_path (str, optional): Path to save the graph image
        """
        dashboard = self.get_portfolio_dashboard()
        weekly_data = dashboard['weekly_data']
        
        if not weekly_data:
            print("No data available to plot.")
            return
        
        # Extract data for plotting
        weeks = [w['week'] for w in weekly_data]
        invested = [w['total_invested'] for w in weekly_data]
        portfolio = [w['portfolio_value'] for w in weekly_data]
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        
        # Plot both lines
        plt.plot(weeks, invested, label='Total Invested', 
                marker='o', linewidth=2, color='#3498db', markersize=4)
        plt.plot(weeks, portfolio, label='Portfolio Value', 
                marker='s', linewidth=2, color='#2ecc71', markersize=4)
        
        # Fill the area between (profit area)
        plt.fill_between(weeks, invested, portfolio, 
                        where=[p >= i for p, i in zip(portfolio, invested)],
                        alpha=0.3, color='#2ecc71', label='Profit')
        
        # Customize the plot
        plt.title('Weekly Investment Growth', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Week Number', fontsize=12, fontweight='bold')
        plt.ylabel('Amount ($)', fontsize=12, fontweight='bold')
        plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Format y-axis as currency
        ax = plt.gca()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add annotations for start and end
        if len(weeks) > 0:
            # Start point
            plt.annotate(f'Start\n${invested[0]:,.0f}',
                        xy=(weeks[0], invested[0]),
                        xytext=(10, -30), textcoords='offset points',
                        fontsize=9, ha='left',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            # End point
            plt.annotate(f'Current\n${portfolio[-1]:,.0f}',
                        xy=(weeks[-1], portfolio[-1]),
                        xytext=(-10, 30), textcoords='offset points',
                        fontsize=9, ha='right',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        
        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Graph saved to: {save_path}")
        else:
            plt.show()
        
        plt.close()


# Example usage
if __name__ == "__main__":
    # Create an investment simulator with $10 daily investment
    investor = MicroInvestment(daily_investment=10.0, annual_return_rate=0.08)
    
    print("Starting micro-investment simulation...")
    print(f"Daily investment: ${investor.daily_investment}")
    print(f"Annual return rate: {investor.annual_return_rate * 100}%")
    
    # Simulate investing for 1 year
    print("\n" + "="*60)
    print("SIMULATING 1 YEAR OF DAILY INVESTMENTS")
    print("="*60)
    investor.invest_for_days(365)
    
    # Show the portfolio dashboard
    investor.print_dashboard()
    
    # Show some transaction history
    print("Last 10 transactions:")
    investor.print_transaction_history(last_n=10)
    
    # Generate and save the weekly growth graph
    print("\nGenerating weekly growth graph...")
    investor.plot_weekly_growth(save_path='portfolio_growth_1year.png')
    
    # Continue for another year (total 2 years)
    print("\n" + "="*60)
    print("CONTINUING TO 2 YEARS")
    print("="*60)
    investor.invest_for_days(365)
    
    # Show updated dashboard
    investor.print_dashboard()
    
    # Generate updated graph
    print("\nGenerating updated weekly growth graph...")
    investor.plot_weekly_growth(save_path='portfolio_growth_2years.png')
    
    # Show summary statistics
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    investor.print_summary()
    
    # Access dashboard data programmatically
    dashboard_data = investor.get_portfolio_dashboard()
    print(f"\nTotal weeks invested: {len(dashboard_data['weekly_data'])}")
    print(f"Average weekly return: ${sum(w['weekly_return'] for w in dashboard_data['weekly_data']) / len(dashboard_data['weekly_data']):.2f}")
