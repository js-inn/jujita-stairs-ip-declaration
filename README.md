# Decentralized Edge Agent & Arctic Powertrain Validation Engine

A multi-module repository containing local custodian edge architecture components and high-reliability aerospace/defense powertrain simulation pipelines. Designed to operate locally in resource-constrained environments with zero-cloud dependencies.

## Modules

### 1. Local Custodian Node (`edge_agent_node.py`)
A lightweight local custodian script designed for decentralized edge computing architectures.
* **Local Data Ingestion:** Bypasses cloud storage by ingesting raw data straight into an isolated local SQLite database.
* **Vector Hash Generation:** Simulates localized embedding and cryptographic fingerprinting using HMAC-SHA256.
* **Zero-Cloud Footprint:** Ensures private user logs and raw files remain entirely within the local environment.

### 2. Arctic Powertrain Simulator (`arctic_powertrain_sim.py`)
A transient thermodynamic and efficiency validation model designed to simulate extreme cold-soak conditions (down to $-40^\circ\text{C}$ / $-50^\circ\text{C}$) and high-torque takeoffs.
* **Loss Isolation:** Separates copper winding losses ($P_{\text{cu}}$), wide-bandgap inverter switching losses ($P_{\text{inv\_loss}}$), and mechanical/viscosity friction losses ($P_{\text{mech}}$).
* **Thermal Transient Mapping:** Models stator resistance changes based on temperature coefficients ($R_s(T)$) during a 5-minute takeoff sequence.
* **Compliance Logging:** Automatically logs time-series performance data into an isolated SQLite database (`arctic_validation.db`) to verify that the 93% to 95% efficiency target is maintained under duress.

## Requirements
* Python 3.x
* SQLite3

## Usage
Run the local custodian node:
```bash
python edge_agent_node.py
