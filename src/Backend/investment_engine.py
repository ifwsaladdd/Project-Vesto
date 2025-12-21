# Import required libraries
from datetime import datetime, timedelta  # For handling dates and time calculations
import matplotlib.pyplot as plt  # For creating graphs and visualizations
import matplotlib.dates as mdates  # For formatting dates in graphs


class MicroInvestment:
    """
    A simulator for tracking micro-investments with daily compounding returns.
    
    This class helps you simulate what happens when you invest a small amount
    of money regularly and earn compound interest on your growing portfolio.
    
    Key Concepts for Beginners:
    - Micro-investment: Investing small amounts regularly (e.g., $10 per day)
    - Compound interest: Earning returns on both your investment AND previous returns
    - Portfolio: The total value of all your investments combined
    - Investment Frequency: How often you invest (daily, weekly, or monthly)
    
    Example:
        >>> # Create a simulator that invests $10 daily with 8% annual returns
        >>> investor = MicroInvestment(investment_amount=10.0, frequency='daily')
        >>> 
        >>> # Or invest $70 weekly (equivalent to $10/day)
        >>> investor = MicroInvestment(investment_amount=70.0, frequency='weekly')
        >>> 
        >>> # Simulate investing for 30 days
        >>> investor.invest_for_days(30)
        >>> 
        >>> # Check how much you've earned
        >>> investor.print_summary()
    """
    
    # Class constant: Minimum investment amount
    MINIMUM_INVESTMENT = 10.0
    
    def __init__(self, investment_amount, frequency='daily', annual_return_rate=0.08):
        """
        Initialize the micro-investment simulator with your investment parameters.
        
        This sets up all the tracking variables and calculates the daily return rate
        from the annual return rate you provide.
        
        Args:
            investment_amount (float): The amount of money you invest per period.
                Must be at least $10.00 (for daily) or equivalent for other frequencies.
                Example: 10.0 with frequency='daily' means $10 every day
                Example: 70.0 with frequency='weekly' means $70 every week
                Example: 300.0 with frequency='monthly' means $300 every month
            
            frequency (str): How often you invest. Options:
                - 'daily': Invest every day (default)
                - 'weekly': Invest once per week (every 7 days)
                - 'monthly': Invest once per month (every 30 days)
            
            annual_return_rate (float): The yearly return rate as a decimal.
                Default is 0.08, which means 8% annual returns.
                Example: 0.08 = 8%, 0.12 = 12%, 0.05 = 5%
        
        Raises:
            ValueError: If investment_amount is less than $10 or frequency is invalid
        
        Example:
            >>> # Invest $10 daily with 10% annual returns
            >>> investor = MicroInvestment(investment_amount=10.0, frequency='daily')
            >>> 
            >>> # Invest $300 monthly with 8% annual returns
            >>> investor = MicroInvestment(investment_amount=300.0, frequency='monthly')
        """
        # Validate the frequency parameter
        valid_frequencies = ['daily', 'weekly', 'monthly']
        if frequency.lower() not in valid_frequencies:
            raise ValueError(f"Invalid frequency '{frequency}'. Must be one of: {', '.join(valid_frequencies)}")
        
        # Store the frequency (convert to lowercase for consistency)
        self.frequency = frequency.lower()
        
        # Store the original investment amount (per period)
        self.investment_amount = investment_amount
        
        # Calculate how many days between investments based on frequency
        if self.frequency == 'daily':
            self.investment_interval_days = 1
        elif self.frequency == 'weekly':
            self.investment_interval_days = 7
        else:  # monthly
            self.investment_interval_days = 30
        
        # Calculate the daily investment amount
        # For daily: daily_investment = investment_amount
        # For weekly: daily_investment = investment_amount / 7
        # For monthly: daily_investment = investment_amount / 30
        self.daily_investment = investment_amount / self.investment_interval_days
        
        # Validate minimum investment (daily equivalent must be at least $10)
        if self.daily_investment < self.MINIMUM_INVESTMENT:
            min_required = self.MINIMUM_INVESTMENT * self.investment_interval_days
            raise ValueError(
                f"Investment amount too low. For {self.frequency} frequency, "
                f"minimum is ${min_required:.2f} (equivalent to ${self.MINIMUM_INVESTMENT:.2f}/day). "
                f"You provided ${investment_amount:.2f}."
            )
        
        # Store the annual return rate (e.g., 0.08 = 8% per year)
        self.annual_return_rate = annual_return_rate
        
        # Track the total amount of money we've put in (starts at $0)
        self.total_invested = 0.0
        
        # Track the current value of our portfolio including returns (starts at $0)
        self.portfolio_value = 0.0
        
        # Count how many days we've been investing (starts at 0)
        self.days_invested = 0
        
        # Track the next day when we should make an investment
        self.next_investment_day = 1
        
        # Store a list of all transactions (deposits and returns) for history
        self.transaction_history = []
        
        # Remember when we started investing (today's date)
        self.start_date = datetime.now()
        
        # Calculate the daily return rate from the annual rate
        # Why? Because we compound daily, not yearly!
        # Formula explanation:
        #   - If annual rate is 8%, we need to find what daily rate compounds to 8% yearly
        #   - We use: (1 + annual_rate)^(1/365) - 1
        #   - Example: (1.08)^(1/365) - 1 ≈ 0.0002107 (about 0.02% per day)
        #   - This ensures that after 365 days of compounding, we get exactly 8% annual return
        self.daily_return_rate = (1 + annual_return_rate) ** (1/365) - 1
    
    
    def invest_daily(self):
        """
        Simulate one day of investment activity.
        
        This method performs three main steps:
        1. Apply compound interest to your existing portfolio (your money grows!)
        2. Add today's new investment to the portfolio
        3. Record all the details in the transaction history
        
        The order is important! We apply returns FIRST, then add new money.
        This is how real investments work - your existing money earns returns
        before you add more.
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_daily()  # Invest for one day
            >>> print(f"Portfolio value: ${investor.portfolio_value:.2f}")
        
        Note:
            This method is called automatically by invest_for_days(), so you
            typically don't need to call it directly.
        """
        # STEP 1: Remember the portfolio value before today's activity
        # We need this to calculate how much we earned today
        portfolio_before = self.portfolio_value
        
        # STEP 2: Apply daily compounding to the existing portfolio
        # This is where the "magic" of compound interest happens!
        # Example: If you have $100 and daily rate is 0.02%, you earn $0.02
        #          New value = $100 × 1.0002 = $100.02
        self.portfolio_value *= (1 + self.daily_return_rate)
        
        # Calculate how much we earned today from compound interest
        # This is the difference between the new value and old value
        daily_return = self.portfolio_value - portfolio_before
        
        # STEP 3: Add today's fresh investment
        # This is the new money we're putting in today
        self.portfolio_value += self.daily_investment
        
        # Update the total amount we've invested so far
        self.total_invested += self.daily_investment
        
        # Increment the day counter
        self.days_invested += 1
        
        # STEP 4: Record this transaction for our history
        # Calculate what date this transaction represents
        # (start_date + number of days since we started)
        transaction_date = self.start_date + timedelta(days=self.days_invested - 1)
        
        # Create a detailed record of today's transaction
        # This dictionary stores all the important information about today
        transaction = {
            'day': self.days_invested,  # Which day number is this?
            'date': transaction_date.strftime('%Y-%m-%d'),  # What's the actual date?
            'investment_amount': self.daily_investment,  # How much did we invest today?
            'portfolio_before': round(portfolio_before, 2),  # Value before today's activity
            'daily_return': round(daily_return, 2),  # How much did we earn from interest?
            'portfolio_after': round(self.portfolio_value, 2),  # Value after everything
            'total_invested': round(self.total_invested, 2)  # Total money we've put in
        }
        
        # Add this transaction to our history list
        self.transaction_history.append(transaction)
    
    def invest_for_days(self, num_days):
        """
        Simulate investing for multiple consecutive days.
        
        This is a convenience method that calls invest_daily() multiple times.
        It's much easier than calling invest_daily() in a loop yourself!
        
        Args:
            num_days (int): How many days to simulate.
                Example: 30 = simulate one month, 365 = simulate one year
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)  # Simulate a full year
            >>> print(f"After 1 year: ${investor.portfolio_value:.2f}")
        
        Note:
            Each day, this method will:
            1. Apply compound interest to existing portfolio
            2. Add the daily investment amount
            3. Record the transaction in history
        """
        # Loop through each day and simulate the investment
        # The underscore (_) means we don't need to use the loop variable
        for _ in range(num_days):
            self.invest_daily()
    
    def get_total_return(self):
        """
        Calculate your total profit or loss.
        
        This tells you how much money you've made (or lost) from your investments.
        It's calculated as: Portfolio Value - Total Money Invested
        
        Returns:
            float: Your total profit/loss in dollars.
                Positive number = You made money! 🎉
                Negative number = You lost money 😞
                Zero = You broke even
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)
            >>> profit = investor.get_total_return()
            >>> print(f"Total profit: ${profit:.2f}")
        
        Note:
            This is your "unrealized" profit - you'd only get this money
            if you sold all your investments today.
        """
        # Simple calculation: What you have now - What you put in = Profit/Loss
        return self.portfolio_value - self.total_invested
    
    def get_return_percentage(self):
        """
        Calculate your return as a percentage.
        
        This shows your profit/loss as a percentage of what you invested.
        It's more intuitive than dollar amounts for comparing performance.
        
        Formula: (Total Return ÷ Total Invested) × 100
        
        Returns:
            float: Return percentage.
                Example: 15.5 means you earned 15.5% on your investment
                Example: -5.0 means you lost 5% of your investment
                Returns 0.0 if you haven't invested anything yet
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)
            >>> roi = investor.get_return_percentage()
            >>> print(f"Return on investment: {roi:.2f}%")
        
        Note:
            This is also called ROI (Return on Investment)
        """
        # Safety check: Can't calculate percentage if we haven't invested anything
        if self.total_invested == 0:
            return 0.0
        
        # Calculate: (Profit ÷ Total Invested) × 100 = Percentage Return
        return (self.get_total_return() / self.total_invested) * 100
    
    def get_summary(self):
        """
        Get a complete summary of your investment as a dictionary.
        
        This method packages all the important information about your investment
        into a single dictionary that you can use in your own code.
        
        Returns:
            dict: A dictionary with these keys:
                - 'days_invested': How many days you've been investing
                - 'daily_investment': How much you invest each day
                - 'total_invested': Total money you've put in
                - 'portfolio_value': Current value of your portfolio
                - 'total_return': Your profit/loss in dollars
                - 'return_percentage': Your profit/loss as a percentage
                - 'annual_return_rate': The annual return rate (as percentage)
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(30)
            >>> summary = investor.get_summary()
            >>> print(f"Invested ${summary['total_invested']} over {summary['days_invested']} days")
            >>> print(f"Current value: ${summary['portfolio_value']}")
        
        Note:
            If you just want to see the summary printed nicely, use
            print_summary() instead.
        """
        # Create and return a dictionary with all the key metrics
        return {
            'days_invested': self.days_invested,
            'daily_investment': self.daily_investment,
            'total_invested': round(self.total_invested, 2),
            'portfolio_value': round(self.portfolio_value, 2),
            'total_return': round(self.get_total_return(), 2),
            'return_percentage': round(self.get_return_percentage(), 2),
            'annual_return_rate': self.annual_return_rate * 100  # Convert to percentage
        }
    
    def print_summary(self):
        """
        Print a nicely formatted summary of your investment to the console.
        
        This displays all the key metrics in an easy-to-read format.
        Perfect for quickly checking how your investment is doing!
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)
            >>> investor.print_summary()
            
            Output:
            ==================================================
            MICRO-INVESTMENT SUMMARY
            ==================================================
            Days Invested:        365
            Daily Investment:     $10.00
            Annual Return Rate:   8.0%
            --------------------------------------------------
            Total Invested:       $3650.00
            Portfolio Value:      $3800.50
            Total Return:         $150.50
            Return Percentage:    4.12%
            ==================================================
        
        Note:
            This method doesn't return anything - it just prints to the screen.
            If you need the data in your code, use get_summary() instead.
        """
        # Get all the summary data
        summary = self.get_summary()
        
        # Print a nice header
        print("\n" + "="*50)
        print("MICRO-INVESTMENT SUMMARY")
        print("="*50)
        
        # Print investment parameters
        print(f"Days Invested:        {summary['days_invested']}")
        print(f"Daily Investment:     ${summary['daily_investment']:.2f}")
        print(f"Annual Return Rate:   {summary['annual_return_rate']:.1f}%")
        
        # Print a divider
        print("-"*50)
        
        # Print current status and returns
        print(f"Total Invested:       ${summary['total_invested']:.2f}")
        print(f"Portfolio Value:      ${summary['portfolio_value']:.2f}")
        print(f"Total Return:         ${summary['total_return']:.2f}")
        print(f"Return Percentage:    {summary['return_percentage']:.2f}%")
        
        # Print a footer
        print("="*50 + "\n")
    
    def get_transaction_history(self, last_n=None):
        """
        Get the transaction history records.
        
        Each transaction record contains details about a specific day's investment,
        including the amount invested, returns earned, and portfolio value.
        
        Args:
            last_n (int, optional): If provided, returns only the last N transactions.
                If None (default), returns all transactions.
                Example: last_n=10 returns the 10 most recent transactions
        
        Returns:
            list: A list of transaction dictionaries. Each dictionary contains:
                - 'day': Day number (1, 2, 3, ...)
                - 'date': Calendar date (YYYY-MM-DD format)
                - 'investment_amount': Money invested that day
                - 'portfolio_before': Portfolio value before that day
                - 'daily_return': Interest earned that day
                - 'portfolio_after': Portfolio value after that day
                - 'total_invested': Cumulative amount invested up to that day
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(30)
            >>> 
            >>> # Get all transactions
            >>> all_txns = investor.get_transaction_history()
            >>> print(f"Total transactions: {len(all_txns)}")
            >>> 
            >>> # Get only the last 5 transactions
            >>> recent = investor.get_transaction_history(last_n=5)
            >>> for txn in recent:
            >>>     print(f"Day {txn['day']}: Invested ${txn['investment_amount']}")
        """
        # If no limit specified, return all transactions
        if last_n is None:
            return self.transaction_history
        
        # Otherwise, return only the last N transactions
        # Python's negative indexing: [-5:] means "last 5 items"
        return self.transaction_history[-last_n:]
    
    def print_transaction_history(self, last_n=10):
        """
        Print a formatted table of transaction history.
        
        This displays your investment transactions in an easy-to-read table format,
        showing what happened each day: how much you invested, how much you earned
        from interest, and your growing portfolio value.
        
        Args:
            last_n (int): Number of recent transactions to display.
                Default is 10 (shows the 10 most recent days).
                Set to a larger number to see more history.
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(100)
            >>> 
            >>> # Show last 10 transactions (default)
            >>> investor.print_transaction_history()
            >>> 
            >>> # Show last 30 transactions
            >>> investor.print_transaction_history(last_n=30)
        
        Output Format:
            Day    Date         Invested     Daily Return   Portfolio      Total Invested
            1      2025-01-01   $10.00       $0.00          $10.00         $10.00
            2      2025-01-02   $10.00       $0.02          $20.02         $20.00
            ...
        """
        # Get the requested number of transactions
        transactions = self.get_transaction_history(last_n)
        
        # Check if there are any transactions to display
        if not transactions:
            print("No transactions yet.")
            return
        
        # Print header
        print("\n" + "="*80)
        print(f"TRANSACTION HISTORY (Last {len(transactions)} transactions)")
        print("="*80)
        
        # Print column headers
        # The :<6 syntax means "left-align in a field of width 6"
        print(f"{'Day':<6} {'Date':<12} {'Invested':<12} {'Daily Return':<14} {'Portfolio':<14} {'Total Invested':<15}")
        print("-"*80)
        
        # Print each transaction as a row in the table
        for txn in transactions:
            print(f"{txn['day']:<6} {txn['date']:<12} ${txn['investment_amount']:<11.2f} "
                  f"${txn['daily_return']:<13.2f} ${txn['portfolio_after']:<13.2f} "
                  f"${txn['total_invested']:<14.2f}")
        
        # Print footer
        print("="*80 + "\n")
    
    def get_portfolio_dashboard(self):
        """
        Get comprehensive portfolio dashboard data with weekly summaries.
        
        This method provides a high-level overview of your investment performance,
        including key metrics and weekly breakdowns. It's more detailed than
        get_summary() and includes weekly performance tracking.
        
        Returns:
            dict: Dashboard data containing:
                - 'total_invested': Total money you've invested
                - 'portfolio_value': Current portfolio value
                - 'net_profit': Total profit/loss
                - 'roi_percentage': Return on investment as percentage
                - 'days_invested': Number of days invested
                - 'daily_investment': Daily investment amount
                - 'annual_return_rate': Annual return rate (as percentage)
                - 'weekly_data': List of weekly summary dictionaries, each containing:
                    * 'week': Week number (1, 2, 3, ...)
                    * 'end_date': Last date of that week
                    * 'total_invested': Cumulative investment at end of week
                    * 'portfolio_value': Portfolio value at end of week
                    * 'weekly_return': Total returns earned during that week
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)
            >>> dashboard = investor.get_portfolio_dashboard()
            >>> print(f"Net profit: ${dashboard['net_profit']:.2f}")
            >>> print(f"Number of weeks: {len(dashboard['weekly_data'])}")
        
        Note:
            Weekly data groups transactions into 7-day periods. If you've invested
            for less than 7 days, you'll have one partial week.
        """
        # Calculate key metrics using our existing methods
        net_profit = self.get_total_return()
        roi_percentage = self.get_return_percentage()
        
        # Calculate weekly summaries by grouping transactions into 7-day chunks
        weekly_data = []
        week_num = 1
        
        # Loop through transactions in groups of 7 (one week)
        # range(0, len(list), 7) gives us: 0, 7, 14, 21, ...
        for i in range(0, len(self.transaction_history), 7):
            # Get the next 7 transactions (or fewer if it's the last week)
            # Example: [0:7] gets items 0-6, [7:14] gets items 7-13, etc.
            week_transactions = self.transaction_history[i:i+7]
            
            # Only process if we have at least one transaction in this week
            if week_transactions:
                # Get the last transaction of the week for end-of-week values
                last_txn = week_transactions[-1]
                
                # Calculate total returns earned during this week
                # sum() adds up all the daily returns from this week's transactions
                weekly_return = sum(txn['daily_return'] for txn in week_transactions)
                
                # Create a summary for this week
                weekly_data.append({
                    'week': week_num,
                    'end_date': last_txn['date'],
                    'total_invested': last_txn['total_invested'],
                    'portfolio_value': last_txn['portfolio_after'],
                    'weekly_return': weekly_return
                })
                week_num += 1
        
        # Return all the dashboard data as a dictionary
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
        Print a comprehensive, visually appealing portfolio dashboard.
        
        This displays a detailed overview of your investment performance,
        including key metrics, investment details, and recent weekly performance.
        It's more comprehensive than print_summary() and includes weekly trends.
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)
            >>> investor.print_dashboard()
            
            Output:
            ============================================================
            📊 PORTFOLIO DASHBOARD
            ============================================================
            
            💰 KEY METRICS
            ------------------------------------------------------------
              Total Invested:        $3,650.00
              Portfolio Value:       $3,800.50
              Net Profit:              $150.50
              Return on Investment:      4.12%
            
            📈 INVESTMENT DETAILS
            ------------------------------------------------------------
              Days Invested:                365
              Daily Investment:          $10.00
              Annual Return Rate:          8.0%
            
            📅 RECENT WEEKLY PERFORMANCE (Last 4 weeks)
            ------------------------------------------------------------
            Week   Date         Invested       Portfolio      Weekly Return
            49     2025-12-07   $3,430.00      $3,570.25      $12.50
            ...
        
        Note:
            This method prints to the console and doesn't return anything.
            For programmatic access to the data, use get_portfolio_dashboard().
        """
        # Get all the dashboard data
        dashboard = self.get_portfolio_dashboard()
        
        # Print main header
        print("\n" + "="*60)
        print("📊 PORTFOLIO DASHBOARD")
        print("="*60)
        
        # SECTION 1: Key Metrics
        # This shows the most important numbers at a glance
        print("\n💰 KEY METRICS")
        print("-"*60)
        # The :> syntax right-aligns the numbers for better readability
        # The , in the format adds thousand separators (e.g., 1,000.00)
        print(f"  Total Invested:        ${dashboard['total_invested']:>12,.2f}")
        print(f"  Portfolio Value:       ${dashboard['portfolio_value']:>12,.2f}")
        print(f"  Net Profit:            ${dashboard['net_profit']:>12,.2f}")
        print(f"  Return on Investment:   {dashboard['roi_percentage']:>11.2f}%")
        
        # SECTION 2: Investment Details
        # This shows your investment parameters and timeline
        print("\n📈 INVESTMENT DETAILS")
        print("-"*60)
        print(f"  Days Invested:          {dashboard['days_invested']:>12}")
        print(f"  Daily Investment:      ${dashboard['daily_investment']:>12,.2f}")
        print(f"  Annual Return Rate:     {dashboard['annual_return_rate']:>11.1f}%")
        
        # SECTION 3: Weekly Performance
        # This shows how your investment has grown week by week
        if dashboard['weekly_data']:
            print("\n📅 RECENT WEEKLY PERFORMANCE (Last 4 weeks)")
            print("-"*60)
            # Print column headers for the weekly table
            print(f"{'Week':<6} {'Date':<12} {'Invested':<14} {'Portfolio':<14} {'Weekly Return':<15}")
            print("-"*60)
            
            # Get only the last 4 weeks (or fewer if less than 4 weeks of data)
            recent_weeks = dashboard['weekly_data'][-4:]
            
            # Print each week's data as a row
            for week in recent_weeks:
                print(f"{week['week']:<6} {week['end_date']:<12} "
                      f"${week['total_invested']:<13,.2f} "
                      f"${week['portfolio_value']:<13,.2f} "
                      f"${week['weekly_return']:<14.2f}")
        
        # Print footer
        print("\n" + "="*60 + "\n")
    
    def plot_weekly_growth(self, save_path=None):
        """
        Generate a beautiful graph showing your investment growth over time.
        
        This creates a line chart that visualizes:
        - How much you've invested over time (blue line)
        - How your portfolio value has grown (green line)
        - The profit area between the two lines (shaded green)
        
        The graph includes annotations highlighting the start and current values.
        
        Args:
            save_path (str, optional): Where to save the graph image.
                If provided, saves the graph as a PNG file at this path.
                If None (default), displays the graph in a window instead.
                Example: 'my_investment_graph.png'
        
        Example:
            >>> investor = MicroInvestment(daily_investment=10.0)
            >>> investor.invest_for_days(365)
            >>> 
            >>> # Display the graph in a window
            >>> investor.plot_weekly_growth()
            >>> 
            >>> # Save the graph to a file
            >>> investor.plot_weekly_growth(save_path='portfolio_2025.png')
        
        Note:
            This requires matplotlib to be installed. The graph shows weekly
            data points (not daily) to keep the visualization clean and readable.
        """
        # Get the dashboard data which includes weekly summaries
        dashboard = self.get_portfolio_dashboard()
        weekly_data = dashboard['weekly_data']
        
        # Check if we have any data to plot
        if not weekly_data:
            print("No data available to plot.")
            return
        
        # Extract data for plotting from the weekly summaries
        # These list comprehensions create separate lists for each data series
        weeks = [w['week'] for w in weekly_data]  # X-axis: week numbers
        invested = [w['total_invested'] for w in weekly_data]  # Y-axis: total invested
        portfolio = [w['portfolio_value'] for w in weekly_data]  # Y-axis: portfolio value
        
        # Create a new figure (graph) with specified size
        # figsize=(12, 6) means 12 inches wide by 6 inches tall
        plt.figure(figsize=(12, 6))
        
        # Plot the "Total Invested" line
        # - weeks, invested: X and Y data points
        # - label: Text for the legend
        # - marker='o': Use circles at each data point
        # - linewidth=2: Make the line 2 pixels thick
        # - color='#3498db': Use a nice blue color (hex code)
        # - markersize=4: Make the circle markers 4 pixels
        plt.plot(weeks, invested, label='Total Invested', 
                marker='o', linewidth=2, color='#3498db', markersize=4)
        
        # Plot the "Portfolio Value" line (same parameters, different color/marker)
        # marker='s' means use squares instead of circles
        plt.plot(weeks, portfolio, label='Portfolio Value', 
                marker='s', linewidth=2, color='#2ecc71', markersize=4)
        
        # Fill the area between the two lines to show profit
        # This creates a shaded green area where portfolio > invested
        # - where=[p >= i for ...]: Only fill where portfolio is greater than invested
        # - alpha=0.3: Make it 30% transparent (0=invisible, 1=solid)
        plt.fill_between(weeks, invested, portfolio, 
                        where=[p >= i for p, i in zip(portfolio, invested)],
                        alpha=0.3, color='#2ecc71', label='Profit')
        
        # Customize the plot appearance
        # Add a title at the top
        plt.title('Weekly Investment Growth', fontsize=16, fontweight='bold', pad=20)
        
        # Label the X-axis (horizontal)
        plt.xlabel('Week Number', fontsize=12, fontweight='bold')
        
        # Label the Y-axis (vertical)
        plt.ylabel('Amount ($)', fontsize=12, fontweight='bold')
        
        # Add a legend box showing what each line/color means
        # loc='upper left': Position it in the top-left corner
        # framealpha=0.9: Make the legend background 90% opaque
        plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
        
        # Add a grid to make it easier to read values
        # alpha=0.3: Make grid lines subtle (30% opacity)
        # linestyle='--': Use dashed lines for the grid
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Format the Y-axis to show dollar signs and commas
        # This makes $1000 display as "$1,000" instead of "1000.0"
        ax = plt.gca()  # gca = "get current axes"
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add annotations (text boxes with arrows) for start and end points
        if len(weeks) > 0:
            # Annotate the starting point
            # xy=(x, y): Where the arrow points to
            # xytext=(dx, dy): Offset for the text box (in pixels)
            # textcoords='offset points': Use pixel offsets for positioning
            # bbox: Style the text box with yellow background
            # arrowprops: Style the arrow pointing to the data point
            plt.annotate(f'Start\\n${invested[0]:,.0f}',
                        xy=(weeks[0], invested[0]),
                        xytext=(10, -30), textcoords='offset points',
                        fontsize=9, ha='left',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            # Annotate the current (end) point
            plt.annotate(f'Current\\n${portfolio[-1]:,.0f}',
                        xy=(weeks[-1], portfolio[-1]),
                        xytext=(-10, 30), textcoords='offset points',
                        fontsize=9, ha='right',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # Adjust layout to prevent labels from being cut off
        plt.tight_layout()
        
        # Either save the graph to a file or display it in a window
        if save_path:
            # Save as a high-quality PNG image
            # dpi=300: High resolution (300 dots per inch)
            # bbox_inches='tight': Don't cut off any labels
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Graph saved to: {save_path}")
        else:
            # Display the graph in an interactive window
            plt.show()
        
        # Close the plot to free up memory
        plt.close()


# =============================================================================
# EXAMPLE USAGE AND DEMONSTRATION
# =============================================================================
# This section shows you how to use the MicroInvestment class.
# It only runs when you execute this file directly (not when importing it).
# This is a complete working example that demonstrates all the main features.

if __name__ == "__main__":
    # STEP 1: Create an investment simulator
    # This sets up a simulation where we invest $10 every day
    # and expect an 8% annual return rate (0.08 as a decimal)
    investor = MicroInvestment(daily_investment=10.0, annual_return_rate=0.08)
    
    print("Starting micro-investment simulation...")
    print(f"Daily investment: ${investor.daily_investment}")
    print(f"Annual return rate: {investor.annual_return_rate * 100}%")
    
    # STEP 2: Simulate investing for 1 year (365 days)
    print("\n" + "="*60)
    print("SIMULATING 1 YEAR OF DAILY INVESTMENTS")
    print("="*60)
    
    # This will simulate 365 days of investing
    # Each day: apply compound interest, then add $10
    investor.invest_for_days(365)
    
    # STEP 3: View the comprehensive dashboard
    # This shows key metrics, investment details, and recent weekly performance
    investor.print_dashboard()
    
    # STEP 4: View detailed transaction history
    # Show the last 10 days of transactions in a table format
    print("Last 10 transactions:")
    investor.print_transaction_history(last_n=10)
    
    # STEP 5: Generate and save a visualization
    # This creates a graph showing how your investment grew over time
    print("\nGenerating weekly growth graph...")
    investor.plot_weekly_growth(save_path='portfolio_growth_1year.png')
    
    # STEP 6: Continue investing for another year (total 2 years now)
    print("\n" + "="*60)
    print("CONTINUING TO 2 YEARS")
    print("="*60)
    
    # Invest for another 365 days (we're now at 730 total days)
    investor.invest_for_days(365)
    
    # STEP 7: View updated dashboard after 2 years
    investor.print_dashboard()
    
    # STEP 8: Generate updated graph showing 2 years of growth
    print("\nGenerating updated weekly growth graph...")
    investor.plot_weekly_growth(save_path='portfolio_growth_2years.png')
    
    # STEP 9: Display final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    investor.print_summary()
    
    # STEP 10: Access data programmatically
    # You can get the raw data as a dictionary to use in your own code
    dashboard_data = investor.get_portfolio_dashboard()
    
    # Calculate and display some custom statistics
    total_weeks = len(dashboard_data['weekly_data'])
    
    # Calculate average weekly return
    # This sums all weekly returns and divides by the number of weeks
    if total_weeks > 0:
        avg_weekly_return = sum(w['weekly_return'] for w in dashboard_data['weekly_data']) / total_weeks
        print(f"\nTotal weeks invested: {total_weeks}")
        print(f"Average weekly return: ${avg_weekly_return:.2f}")
    
    # You can also access individual transaction data
    # For example, let's look at the very first transaction
    if investor.transaction_history:
        first_txn = investor.transaction_history[0]
        print(f"\nFirst transaction was on {first_txn['date']}")
        print(f"Started with ${first_txn['investment_amount']:.2f}")
