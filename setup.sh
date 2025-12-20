#!/bin/bash

# Setup script for Project Vesto Investment Engine

echo "Setting up Python virtual environment for Project Vesto..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the investment engine:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the script: python src/Backend/investment_engine.py"
echo "  3. Deactivate when done: deactivate"
