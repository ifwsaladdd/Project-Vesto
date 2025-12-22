from datetime import datetime, timedelta

class MicroInvestment:
    """
    A production-ready simulator for tracking micro-investments with daily compounding returns.
    
    Supports:
    - Frequencies: Daily, Weekly, 15_days, Monthly
    - Inflation Adjustment (Real vs Nominal returns)
    - 2% Platform Fee
    - Daily Compounding
    """
    
    # Class constant: Minimum investment amount
    MINIMUM_INVESTMENT = 10.0
    
    # Class constant: Platform fee percentage (2%)
    PLATFORM_FEE_RATE = 0.02
    
    def __init__(self, investment_amount, frequency='daily', annual_return_rate=0.08, annual_inflation_rate=0.0):
        """
        Initialize the investment engine.
        
        Args:
            investment_amount (float): The gross amount to invest per period.
            frequency (str): 'daily', 'weekly', '15_days', or 'monthly'.
            annual_return_rate (float): Annual nominal return rate (default 0.08).
            annual_inflation_rate (float): Annual inflation rate (default 0.0).
        """
        # Validate frequency
        valid_frequencies = ['daily', 'weekly', '15_days', 'monthly']
        if frequency.lower() not in valid_frequencies:
            raise ValueError(f"Invalid frequency '{frequency}'. Must be one of: {', '.join(valid_frequencies)}")
        
        self.frequency = frequency.lower()
        self.investment_amount = investment_amount
        
        # Calculate days between investments
        if self.frequency == 'daily':
            self.investment_interval_days = 1
        elif self.frequency == 'weekly':
            self.investment_interval_days = 7
        elif self.frequency == '15_days':
            self.investment_interval_days = 15
        else:  # monthly
            self.investment_interval_days = 30
        
        self.daily_investment = investment_amount / self.investment_interval_days
        
        # Validate minimum investment
        if self.daily_investment < self.MINIMUM_INVESTMENT:
            min_required = self.MINIMUM_INVESTMENT * self.investment_interval_days
            raise ValueError(
                f"Investment amount too low. For {self.frequency} frequency, "
                f"minimum is ${min_required:.2f}."
            )
        
        self.annual_return_rate = annual_return_rate
        self.total_gross_invested = 0.0
        self.total_platform_fees = 0.0
        self.total_invested = 0.0
        self.portfolio_value = 0.0
        self.days_invested = 0
        self.next_investment_day = 1
        self.transaction_history = []
        self.start_date = datetime.now()
        self.vesto_main_funds = 0.0
        
        # Calculate daily rates
        self.daily_return_rate = (1 + annual_return_rate) ** (1/365) - 1
        
        self.annual_inflation_rate = annual_inflation_rate
        self.daily_inflation_rate = (1 + annual_inflation_rate) ** (1/365) - 1
        
        self.total_invested_real = 0.0
    
    
    def invest(self, net_amount):
        """
        Invest a lump sum (net amount after fees) directly into the portfolio.
        This is used by external APIs to add funds ad-hoc.
        """
        self.portfolio_value += net_amount
        self.total_invested += net_amount
        self.total_invested_real += net_amount  # Simplified real tracking for ad-hoc
    
    def invest_daily(self):
        """
        Simulate one day of investment activity.
        1. Compounding
        2. New Investment (if applicable)
        3. Record Transaction
        """
        portfolio_before = self.portfolio_value
        
        # 1. Apply daily compounding
        self.portfolio_value *= (1 + self.daily_return_rate)
        
        daily_return = self.portfolio_value - portfolio_before
        
        gross_investment = 0.0
        platform_fee = 0.0
        net_investment = 0.0
        
        self.days_invested += 1
        
        # 2. Check if today is an investment day
        if self.days_invested >= self.next_investment_day:
            gross_investment = self.investment_amount
            platform_fee = gross_investment * self.PLATFORM_FEE_RATE
            net_investment = gross_investment - platform_fee
            
            self.portfolio_value += net_investment
            
            self.total_gross_invested += gross_investment
            self.total_platform_fees += platform_fee
            self.vesto_main_funds += platform_fee
            self.total_invested += net_investment
            
            # Track Real (inflation-adjusted) investment
            discount_factor = 1 / ((1 + self.daily_inflation_rate) ** self.days_invested)
            self.total_invested_real += net_investment * discount_factor
            
            self.next_investment_day += self.investment_interval_days
        
        # 3. Record transaction
        transaction_date = self.start_date + timedelta(days=self.days_invested - 1)
        
        transaction = {
            'day': self.days_invested,
            'date': transaction_date.strftime('%Y-%m-%d'),
            'investment_amount': gross_investment,
            'gross_investment': round(gross_investment, 2),
            'platform_fee': round(platform_fee, 2),
            'net_investment': round(net_investment, 2),
            'portfolio_before': round(portfolio_before, 2),
            'daily_return': round(daily_return, 2),
            'portfolio_after': round(self.portfolio_value, 2),
            'total_gross_invested': round(self.total_gross_invested, 2),
            'total_platform_fees': round(self.total_platform_fees, 2),
            'total_net_invested': round(self.total_invested, 2),
            'vesto_main_funds': round(self.vesto_main_funds, 2)
        }
        
        self.transaction_history.append(transaction)
    
    def invest_for_days(self, num_days):
        """Simulate investing for multiple consecutive days."""
        for _ in range(num_days):
            self.invest_daily()
    
    def get_total_return(self):
        """Calculate Nominal total profit or loss."""
        return self.portfolio_value - self.total_invested
    
    def get_return_percentage(self):
        """Calculate Nominal ROI percentage."""
        if self.total_invested == 0:
            return 0.0
        return (self.get_total_return() / self.total_invested) * 100
    
    def get_real_portfolio_value(self):
        """Calculate Real (Inflation-Adjusted) portfolio value."""
        return self.portfolio_value / ((1 + self.daily_inflation_rate) ** self.days_invested)

    def get_real_total_return(self):
        """Calculate Real profit or loss."""
        return self.get_real_portfolio_value() - self.total_invested_real

    def get_real_return_percentage(self):
        """Calculate Real ROI percentage."""
        if self.total_invested_real == 0:
            return 0.0
        return (self.get_real_total_return() / self.total_invested_real) * 100
    
    def get_summary(self):
        """
        Get a complete summary of the investment state.
        Returns a dictionary suitable for API responses.
        """
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
            'annual_return_rate': self.annual_return_rate * 100,
            'annual_inflation_rate': self.annual_inflation_rate * 100,
            'vesto_main_funds': round(self.vesto_main_funds, 2),
            'total_real_invested': round(self.total_invested_real, 2),
            'real_portfolio_value': round(self.get_real_portfolio_value(), 2),
            'real_total_return': round(self.get_real_total_return(), 2),
            'real_return_percentage': round(self.get_real_return_percentage(), 2)
        }
    
    def get_transaction_history(self, last_n=None):
        """Get the transaction history records."""
        if last_n is None:
            return self.transaction_history
        return self.transaction_history[-last_n:]
    
    def get_portfolio_dashboard(self):
        """
        Get comprehensive portfolio dashboard data with weekly summaries.
        """
        net_profit = self.get_total_return()
        roi_percentage = self.get_return_percentage()
        
        weekly_data = []
        week_num = 1
        
        for i in range(0, len(self.transaction_history), 7):
            week_transactions = self.transaction_history[i:i+7]
            
            if week_transactions:
                last_txn = week_transactions[-1]
                weekly_return = sum(txn['daily_return'] for txn in week_transactions)
                
                weekly_data.append({
                    'week': week_num,
                    'end_date': last_txn['date'],
                    'total_invested': last_txn['total_invested'],
                    'portfolio_value': last_txn['portfolio_after'],
                    'weekly_return': weekly_return
                })
                week_num += 1
        
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
