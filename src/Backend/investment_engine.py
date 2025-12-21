# Import required libraries
from datetime import datetime, timedelta  # For handling dates and time calculations

# Optional: matplotlib for creating graphs (not required for core functionality)
try:
    import matplotlib.pyplot as plt  # For creating graphs and visualizations
    import matplotlib.dates as mdates  # For formatting dates in graphs
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


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
    
    # Class constant: Platform fee percentage (2%)
    PLATFORM_FEE_RATE = 0.02
    
    def __init__(self, investment_amount, frequency='daily', annual_return_rate=0.08):
        """
        Initialize the micro-investment simulator with your investment parameters.
        
        This sets up all the tracking variables and calculates the daily return rate
        from the annual return rate you provide.
        
        Args:
            investment_amount (float): The amount of money you invest per period.
                Must be at least $10.00 (for daily) or equivalent for other frequencies.
                Note: A 2% platform fee will be deducted from each investment.
                Example: $10.00 investment → $0.20 fee → $9.80 net invested
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
            >>> # After 2% fee: $9.80 goes to portfolio, $0.20 to platform
            >>> investor = MicroInvestment(investment_amount=10.0, frequency='daily')
            >>> 
            >>> # Invest $300 monthly with 8% annual returns
            >>> # After 2% fee: $294 goes to portfolio, $6 to platform
            >>> investor = MicroInvestment(investment_amount=300.0, frequency='monthly')
        """
        # Validate the frequency parameter
        valid_frequencies = ['daily', 'weekly', '15_days', 'monthly']
        if frequency.lower() not in valid_frequencies:
            raise ValueError(f"Invalid frequency '{frequency}'. Must be one of: {', '.join(valid_frequencies)}")
        
        # Store the frequency (convert to lowercase for consistency)
        self.frequency = frequency.lower()
        
        # Store the original investment amount (per period) - this is the GROSS amount
        self.investment_amount = investment_amount
        
        # Calculate how many days between investments based on frequency
        if self.frequency == 'daily':
            self.investment_interval_days = 1
        elif self.frequency == 'weekly':
            self.investment_interval_days = 7
        elif self.frequency == '15_days':
            self.investment_interval_days = 15
        else:  # monthly
            self.investment_interval_days = 30
        
        # Calculate the daily investment amount (gross)
        # For daily: daily_investment = investment_amount
        # For weekly: daily_investment = investment_amount / 7
        # For 15_days: daily_investment = investment_amount / 15
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
        
        # Track the total GROSS amount invested (before fees)
        self.total_gross_invested = 0.0
        
        # Track the total platform fees collected (2% of each investment)
        self.total_platform_fees = 0.0
        
        # Track the total NET amount invested (after fees - what actually goes to portfolio)
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
        
        # Vesto main-funds account: tracks all platform fees collected
        self.vesto_main_funds = 0.0
        
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
        
<<<<<<< HEAD
        This method performs three main steps:
        1. Apply compound interest to your existing portfolio (your money grows!)
        2. Add today's new investment to the portfolio
        3. Record all the details in the transaction history
        
=======
        This method performs these steps each day:
        1. Apply compound interest to your existing portfolio (your money grows!)
        2. If it's an investment day:
           a. Calculate 2% platform fee from gross investment
           b. Add platform fee to Vesto main-funds account
           c. Add net amount (after fee) to portfolio
        3. Record all the details in the transaction history
        
        Platform Fee Example:
            - Gross investment: $100.00
            - Platform fee (2%): $2.00 → goes to Vesto main-funds
            - Net invested: $98.00 → goes to your portfolio
        
        Important: Compound interest is applied EVERY day, but new money is only
        added based on your frequency (daily, weekly, or monthly).
        
>>>>>>> f4970ac (Added options to choose varying investment amounts)
        The order is important! We apply returns FIRST, then add new money.
        This is how real investments work - your existing money earns returns
        before you add more.
        
        Example:
<<<<<<< HEAD
            >>> investor = MicroInvestment(daily_investment=10.0)
=======
            >>> investor = MicroInvestment(investment_amount=10.0, frequency='daily')
>>>>>>> f4970ac (Added options to choose varying investment amounts)
            >>> investor.invest_daily()  # Invest for one day
            >>> print(f"Portfolio value: ${investor.portfolio_value:.2f}")
            >>> print(f"Platform fees collected: ${investor.vesto_main_funds:.2f}")
        
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
<<<<<<< HEAD
=======
        # NOTE: This happens EVERY day, regardless of investment frequency
>>>>>>> f4970ac (Added options to choose varying investment amounts)
        self.portfolio_value *= (1 + self.daily_return_rate)
        
        # Calculate how much we earned today from compound interest
        # This is the difference between the new value and old value
        daily_return = self.portfolio_value - portfolio_before
        
<<<<<<< HEAD
        # STEP 3: Add today's fresh investment
        # This is the new money we're putting in today
        self.portfolio_value += self.daily_investment
        
        # Update the total amount we've invested so far
        self.total_invested += self.daily_investment
        
        # Increment the day counter
        self.days_invested += 1
        
=======
        # STEP 3: Check if today is an investment day
        # For daily: invest every day (next_investment_day = 1, 2, 3, ...)
        # For weekly: invest every 7 days (next_investment_day = 1, 8, 15, ...)
        # For 15_days: invest every 15 days (next_investment_day = 1, 16, 31, ...)
        # For monthly: invest every 30 days (next_investment_day = 1, 31, 61, ...)
        gross_investment = 0.0
        platform_fee = 0.0
        net_investment = 0.0
        
        # Increment the day counter first
        self.days_invested += 1
        
        # Check if we should invest today
        if self.days_invested >= self.next_investment_day:
            # Yes! Today is an investment day
            
            # Calculate the gross investment amount (what the client pays)
            gross_investment = self.investment_amount
            
            # Calculate the 2% platform fee
            # Example: $100 × 0.02 = $2.00 fee
            platform_fee = gross_investment * self.PLATFORM_FEE_RATE
            
            # Calculate the net investment (what actually goes to the portfolio)
            # Example: $100 - $2.00 = $98.00 net invested
            net_investment = gross_investment - platform_fee
            
            # Add the net amount to the portfolio (NOT the gross amount!)
            # Only the money after fees contributes to portfolio growth
            self.portfolio_value += net_investment
            
            # Track the gross amount (total client paid)
            self.total_gross_invested += gross_investment
            
            # Track the platform fee collected
            self.total_platform_fees += platform_fee
            
            # Transfer the platform fee to Vesto main-funds account
            self.vesto_main_funds += platform_fee
            
            # Track the net amount invested (what's actually in the portfolio)
            self.total_invested += net_investment
            
            # Schedule the next investment day
            self.next_investment_day += self.investment_interval_days
        
>>>>>>> f4970ac (Added options to choose varying investment amounts)
        # STEP 4: Record this transaction for our history
        # Calculate what date this transaction represents
        # (start_date + number of days since we started)
        transaction_date = self.start_date + timedelta(days=self.days_invested - 1)
        
        # Create a detailed record of today's transaction
        # This dictionary stores all the important information about today
        transaction = {
            'day': self.days_invested,  # Which day number is this?
            'date': transaction_date.strftime('%Y-%m-%d'),  # What's the actual date?
<<<<<<< HEAD
<<<<<<< HEAD
            'investment_amount': self.daily_investment,  # How much did we invest today?
=======
            'investment_amount': investment_made_today,  # How much did we invest today?
>>>>>>> f4970ac (Added options to choose varying investment amounts)
=======
            'gross_investment': round(gross_investment, 2),  # Amount client paid (before fee)
            'platform_fee': round(platform_fee, 2),  # 2% fee deducted
            'net_investment': round(net_investment, 2),  # Amount added to portfolio (after fee)
>>>>>>> 0c3abf9 (data of simulations)
            'portfolio_before': round(portfolio_before, 2),  # Value before today's activity
            'daily_return': round(daily_return, 2),  # How much did we earn from interest?
            'portfolio_after': round(self.portfolio_value, 2),  # Value after everything
            'total_gross_invested': round(self.total_gross_invested, 2),  # Total client paid
            'total_platform_fees': round(self.total_platform_fees, 2),  # Total fees collected
            'total_net_invested': round(self.total_invested, 2),  # Total in portfolio
            'vesto_main_funds': round(self.vesto_main_funds, 2)  # Platform fees account balance
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
<<<<<<< HEAD
<<<<<<< HEAD
                - 'daily_investment': How much you invest each day
=======
                - 'investment_amount': How much you invest per period
                - 'frequency': How often you invest (daily/weekly/monthly)
>>>>>>> f4970ac (Added options to choose varying investment amounts)
                - 'total_invested': Total money you've put in
=======
                - 'investment_amount': How much you invest per period (gross)
                - 'frequency': How often you invest (daily/weekly/monthly)
                - 'total_gross_invested': Total amount paid (before fees)
                - 'total_platform_fees': Total 2% fees collected
                - 'total_net_invested': Total actually invested (after fees)
>>>>>>> 0c3abf9 (data of simulations)
                - 'portfolio_value': Current value of your portfolio
                - 'total_return': Your profit/loss in dollars
                - 'return_percentage': Your profit/loss as a percentage
                - 'annual_return_rate': The annual return rate (as percentage)
                - 'vesto_main_funds': Platform fees account balance
        
        Example:
<<<<<<< HEAD
            >>> investor = MicroInvestment(daily_investment=10.0)
=======
            >>> investor = MicroInvestment(investment_amount=10.0, frequency='daily')
>>>>>>> f4970ac (Added options to choose varying investment amounts)
            >>> investor.invest_for_days(30)
            >>> summary = investor.get_summary()
            >>> print(f"Gross invested: ${summary['total_gross_invested']}")
            >>> print(f"Platform fees: ${summary['total_platform_fees']}")
            >>> print(f"Net invested: ${summary['total_net_invested']}")
        
        Note:
            If you just want to see the summary printed nicely, use
            print_summary() instead.
        """
        # Create and return a dictionary with all the key metrics
        return {
            'days_invested': self.days_invested,
            'investment_amount': self.investment_amount,
            'frequency': self.frequency,
            'total_gross_invested': round(self.total_gross_invested, 2),
            'total_platform_fees': round(self.total_platform_fees, 2),
            'total_net_invested': round(self.total_invested, 2),
            'portfolio_value': round(self.portfolio_value, 2),
            'total_return': round(self.get_total_return(), 2),
            'return_percentage': round(self.get_return_percentage(), 2),
            'annual_return_rate': self.annual_return_rate * 100,  # Convert to percentage
            'vesto_main_funds': round(self.vesto_main_funds, 2)
        }
    
    def print_summary(self):
        """
        Print a nicely formatted summary of your investment to the console.
        
        This displays all the key metrics in an easy-to-read format.
        Perfect for quickly checking how your investment is doing!
        
        Example:
<<<<<<< HEAD
            >>> investor = MicroInvestment(daily_investment=10.0)
=======
            >>> investor = MicroInvestment(investment_amount=70.0, frequency='weekly')
>>>>>>> f4970ac (Added options to choose varying investment amounts)
            >>> investor.invest_for_days(365)
            >>> investor.print_summary()
            
            Output:
            ==================================================
            MICRO-INVESTMENT SUMMARY
            ==================================================
            Days Invested:        365
<<<<<<< HEAD
            Daily Investment:     $10.00
=======
            Investment Amount:    $70.00 weekly
>>>>>>> f4970ac (Added options to choose varying investment amounts)
            Annual Return Rate:   8.0%
            --------------------------------------------------
            Gross Invested:       $3650.00
            Platform Fees (2%):   $73.00
            Net Invested:         $3577.00
            Portfolio Value:      $3720.50
            Total Return:         $143.50
            Return Percentage:    4.01%
            --------------------------------------------------
            Vesto Main-Funds:     $73.00
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
        print(f"Investment Amount:    ${summary['investment_amount']:.2f} {summary['frequency']}")
        print(f"Annual Return Rate:   {summary['annual_return_rate']:.1f}%")
        
        # Print a divider
        print("-"*50)
        
        # Print investment breakdown with fees
        print(f"Gross Invested:       ${summary['total_gross_invested']:.2f}")
        print(f"Platform Fees (2%):   ${summary['total_platform_fees']:.2f}")
        print(f"Net Invested:         ${summary['total_net_invested']:.2f}")
        print(f"Portfolio Value:      ${summary['portfolio_value']:.2f}")
        print(f"Total Return:         ${summary['total_return']:.2f}")
        print(f"Return Percentage:    ${summary['return_percentage']:.2f}%")
        
        # Print platform fees section
        print("-"*50)
        print(f"Vesto Main-Funds:     ${summary['vesto_main_funds']:.2f}")
        
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
            'investment_amount': self.investment_amount,
            'frequency': self.frequency,
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
        print(f"  Investment Amount:     ${dashboard['investment_amount']:>12,.2f} {dashboard['frequency']}")
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
        # Check if matplotlib is available
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib is not installed. Cannot generate graph.")
            print("   To install: pip install matplotlib")
            return
        
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
# HELPER FUNCTION FOR USER INPUT
# =============================================================================

def get_user_investment_parameters():
    """
    Interactively get investment parameters from the user.
    
    This function prompts the user to enter:
    - Investment amount (with validation for $10 minimum)
    - Investment frequency (daily, weekly, or monthly)
    - Annual return rate (optional, defaults to 8%)
    
    Returns:
        tuple: (investment_amount, frequency, annual_return_rate)
    
    Example:
        >>> amount, freq, rate = get_user_investment_parameters()
        >>> investor = MicroInvestment(investment_amount=amount, frequency=freq, annual_return_rate=rate)
    """
    print("\n" + "="*60)
    print("MICRO-INVESTMENT SIMULATOR - SETUP")
    print("="*60)
    print("Let's set up your investment simulation!\n")
    
    # STEP 1: Get investment frequency
    print("How often do you want to invest?")
    print("  1. Daily")
    print("  2. Weekly")
    print("  3. Monthly")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == '1':
            frequency = 'daily'
            interval_days = 1
            break
        elif choice == '2':
            frequency = 'weekly'
            interval_days = 7
            break
        elif choice == '3':
            frequency = 'monthly'
            interval_days = 30
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    # STEP 2: Get investment amount with validation
    min_amount = MicroInvestment.MINIMUM_INVESTMENT * interval_days
    
    print(f"\nYou selected: {frequency.upper()} investments")
    print(f"Minimum investment amount: ${min_amount:.2f} per {frequency} period")
    print(f"(This ensures at least ${MicroInvestment.MINIMUM_INVESTMENT:.2f}/day equivalent)")
    
    while True:
        try:
            amount_input = input(f"\nEnter your {frequency} investment amount ($): ").strip()
            investment_amount = float(amount_input)
            
            if investment_amount < min_amount:
                print(f"❌ Amount too low! Minimum is ${min_amount:.2f} for {frequency} frequency.")
                print(f"   (This equals ${investment_amount/interval_days:.2f}/day, but we need ${MicroInvestment.MINIMUM_INVESTMENT:.2f}/day minimum)")
                continue
            
            print(f"✓ Great! You'll invest ${investment_amount:.2f} {frequency}")
            print(f"  (Equivalent to ${investment_amount/interval_days:.2f} per day)")
            break
        except ValueError:
            print("❌ Invalid input. Please enter a number (e.g., 10.00)")
    
    # STEP 3: Get annual return rate (optional)
    print("\nWhat annual return rate do you expect?")
    print("  (Press Enter to use default: 8.0%)")
    
    while True:
        rate_input = input("Enter annual return rate (%) or press Enter: ").strip()
        
        if rate_input == '':
            annual_return_rate = 0.08
            print(f"✓ Using default: 8.0% annual return")
            break
        
        try:
            rate_percent = float(rate_input)
            if rate_percent <= 0 or rate_percent > 100:
                print("❌ Please enter a rate between 0 and 100")
                continue
            
            annual_return_rate = rate_percent / 100
            print(f"✓ Using {rate_percent}% annual return")
            break
        except ValueError:
            print("❌ Invalid input. Please enter a number (e.g., 8.5)")
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print(f"Investment Amount: ${investment_amount:.2f} {frequency}")
    print(f"Annual Return Rate: {annual_return_rate * 100:.1f}%")
    print("="*60 + "\n")
    
    return investment_amount, frequency, annual_return_rate


# =============================================================================
# EXAMPLE USAGE AND DEMONSTRATION
# =============================================================================
# This section shows you how to use the MicroInvestment class.
# It only runs when you execute this file directly (not when importing it).
# This is a complete working example that demonstrates all the main features.

if __name__ == "__main__":
    print("Welcome to the Micro-Investment Simulator!")
    print("This tool helps you visualize how regular investments grow over time.\n")
    
    # Ask user if they want to use interactive mode or example mode
    print("Choose a mode:")
    print("  1. Interactive Mode (enter your own values)")
    print("  2. Example Mode (use pre-set values for demonstration)")
    
    mode_choice = input("\nEnter your choice (1-2): ").strip()
    
    if mode_choice == '1':
        # INTERACTIVE MODE: Get user input
        investment_amount, frequency, annual_return_rate = get_user_investment_parameters()
        
        # Create the investor with user's parameters
        investor = MicroInvestment(
            investment_amount=investment_amount,
            frequency=frequency,
            annual_return_rate=annual_return_rate
        )
        
        # Ask how long to simulate
        print("How long would you like to simulate?")
        while True:
            try:
                days_input = input("Enter number of days (e.g., 30, 365): ").strip()
                num_days = int(days_input)
                if num_days <= 0:
                    print("❌ Please enter a positive number")
                    continue
                break
            except ValueError:
                print("❌ Invalid input. Please enter a whole number")
        
        print(f"\n🚀 Simulating {num_days} days of investing...")
        investor.invest_for_days(num_days)
        
        # Show results
        investor.print_dashboard()
        investor.print_summary()
        
        # Offer to show transaction history
        show_history = input("\nWould you like to see transaction history? (y/n): ").strip().lower()
        if show_history == 'y':
            try:
                num_txns = int(input("How many recent transactions to show? (default 10): ").strip() or "10")
                investor.print_transaction_history(last_n=num_txns)
            except ValueError:
                investor.print_transaction_history(last_n=10)
        
    else:
        # EXAMPLE MODE: Use pre-set values for demonstration
        print("\n" + "="*60)
        print("RUNNING EXAMPLE DEMONSTRATION")
        print("="*60)
        
        # STEP 1: Create an investment simulator
        # This sets up a simulation where we invest $70 every week
        # and expect an 8% annual return rate (0.08 as a decimal)
        investor = MicroInvestment(investment_amount=70.0, frequency='weekly', annual_return_rate=0.08)
        
        print("Example setup:")
        print(f"  Investment: ${investor.investment_amount} {investor.frequency}")
        print(f"  Annual return rate: {investor.annual_return_rate * 100}%")
        
        # STEP 2: Simulate investing for 1 year (365 days)
        print("\n" + "="*60)
        print("SIMULATING 1 YEAR OF WEEKLY INVESTMENTS")
        print("="*60)
        
        # This will simulate 365 days of investing
        # Each day: apply compound interest
        # Every 7 days: add $70
        investor.invest_for_days(365)
        
        # STEP 3: View the comprehensive dashboard
        # This shows key metrics, investment details, and recent weekly performance
        investor.print_dashboard()
        
        # STEP 4: View detailed transaction history
        # Show the last 10 days of transactions in a table format
        print("Last 10 transactions:")
        investor.print_transaction_history(last_n=10)
        
        # STEP 5: Display final summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        investor.print_summary()
        
        # STEP 6: Access data programmatically
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
