#!/bin/bash
set -e
echo "Starting Corporate Identity & Tax Audit Pipeline..."
python fraud_mitigation.py
echo "Audit pipeline executed successfully."
