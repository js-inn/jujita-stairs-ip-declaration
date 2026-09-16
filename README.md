# Edge Tax Audit Engine & Cryptographic Integrity Pipeline

A lightweight, audit-compliant tax ingestion, verification, and reporting pipeline designed to run on local edge environments (including Termux/Android). The engine processes Canadian tax payloads (T619/T550), validates incoming XML structures against schema rules, maps line items against a 55-category taxonomy, and enforces immutable SHA-256 payload integrity verification.

---

## Architecture Overview

