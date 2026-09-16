#!/bin/bash
set -e

echo "=================================================="
echo " 🛠️ EXECUTING EDGE TAX AUDIT PIPELINE"
echo "=================================================="

echo "[1/6] Running XML Schema Validation & Parser..."
python validate_schema.py
python xml_parser.py

echo "[2/6] Initializing Database Schema & Audit Payload..."
python audit_logger.py

echo "[3/6] Seeding 55-Category Taxonomy Matrix..."
python update_taxonomy.py

echo "[4/6] Computing Immutable SHA-256 Hashes..."
python log_payload_hash.py

echo "[5/6] Verifying Cryptographic Payload Integrity..."
python verify_integrity.py

echo "[6/6] Generating Masked Audit Exports & Package..."
python audit_report.py
python export_audit_package.py

echo "=================================================="
echo " ✅ AUDIT PIPELINE COMPLETED SUCCESSFULLY"
echo "=================================================="

# [4/6] Parse T661 XSD Schema & Validate Submission
python3 parse_t661.py
python3 validate_t661.py
