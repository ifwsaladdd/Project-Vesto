from flask import Flask, jsonify, request
import sys
import os

# Add Engine directory to path to allow import
sys.path.append(os.path.join(os.path.dirname(__file__), '../Engine'))
from investment_engine import MicroInvestment

# Create the Flask application
app = Flask(__name__)

# Manual CORS support
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialize the investment engine
engine = MicroInvestment(investment_amount=10.0)  # Default init

@app.route('/invest', methods=['POST'])
def invest():
    """
    Invest funds into a specific fund.
    Expects JSON: { "amount": 100.0, "fund_id": "fund_001" }
    """
    data = request.get_json()
    
    if not data or 'amount' not in data or 'fund_id' not in data:
        return jsonify({'error': 'Invalid request. Provide amount and fund_id.'}), 400
        
    gross_amount = float(data['amount'])
    fund_id = data['fund_id']
    
    # Calculate fees (2%)
    fee = gross_amount * 0.02
    net_invested = gross_amount - fee
    
    # Call the engine
    engine.invest(net_invested)
    
    return jsonify({
        'gross_amount': gross_amount,
        'fee': fee,
        'net_invested': net_invested,
        'fund_id': fund_id,
        'status': 'success'
    }), 201

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint.
    Returns status: 'ok' to verify the API is running.
    """
    return jsonify({
        'status': 'ok'
    })

@app.route('/funds', methods=['GET'])
def get_funds():
    """
    Returns a list of available funds.
    Currently hardcoded with one liquid mutual fund.
    """
    funds = [
        {
            'fund_id': 'fund_001',
            'name': 'Vesto Liquid Fund Direct Growth',
            'type': 'Liquid Mutual Fund',
            'risk_level': 'Low',
            'expected_return_range': '6-7%',
            'description': 'A low-risk fund that works like a high-yield savings account. It invests in safe, short-term assets so you earn steady returns without locking your money away.'
        }
    ]
    return jsonify({
        'funds': funds,
        'count': len(funds)
    })

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    """
    Returns the current portfolio summary.
    Includes Nominal and Real (inflation-adjusted) metrics.
    """
    summary = engine.get_summary()
    
    return jsonify({
        'total_invested': summary['total_net_invested'],
        'portfolio_value': summary['portfolio_value'],
        'nominal_roi': summary['return_percentage'],
        'real_roi': summary['real_return_percentage']
    })

@app.route('/insights', methods=['GET'])
def get_insights():
    """
    Returns insights on investment performance.
    """
    return jsonify(engine.get_insights())

@app.route('/simulate', methods=['POST'])
def simulate_time():
    """
    Simulate the passage of time for demo purposes.
    Expects JSON: { "days": 30 }
    """
    data = request.get_json()
    days = data.get('days', 30) if data else 30
    
    try:
        engine.advance_time(int(days))
        return jsonify({
            'status': 'success',
            'days_advanced': days,
            'message': f'Simulated passage of {days} days.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#DEBUGGING ENDPOINT
@app.route("/debug", methods=["GET"])
def debug():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])



if __name__ == '__main__':
    # Run the application
    # debug=True allows for auto-reloading during development
    print("Starting Flask API...")
    print("Try accessing: http://127.0.0.1:5000/health")
    app.run(debug=True, port=5000)
