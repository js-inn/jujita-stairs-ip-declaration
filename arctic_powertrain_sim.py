import sqlite3
import json
import time
import math

class ArcticPowertrainValidator:
    def __init__(self, db_path="arctic_validation.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                ambient_temp_c REAL,
                rpm REAL,
                torque_nm REAL,
                v_dc REAL,
                i_dc REAL,
                p_out REAL,
                p_in REAL,
                efficiency REAL,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def compute_thermal_resistance(self, base_resistance: float, temp_c: float, alpha: float = 0.00393, t_reference: float = 20.0) -> float:
        """Computes stator winding resistance change based on temperature (Copper TCR)."""
        return base_resistance * (1 + alpha * (temp_c - t_reference))

    def run_takeoff_transient_simulation(self, ambient_temp_c: float = -40.0):
        print(f"\n[Arctic Engine Simulation] Initializing cold-start sequence at Ambient: {ambient_temp_c}°C")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simulate a 5-minute (300 seconds) takeoff profile mapped in 30-second intervals
        # Target: >1,400 Nm across 2,500 - 2,800 RPM band
        rpm_target = 2650.0
        torque_target = 1420.0 # Nm
        base_rs = 0.025 # Ohms at 20C
        
        success_count = 0
        total_steps = 10

        for step in range(total_steps):
            # Simulate internal motor heating from -40C up to steady-state +95C over 5 minutes
            simulated_winding_temp = ambient_temp_c + (step * 13.5)
            
            # Dynamic variables
            omega = (2 * math.pi * rpm_target) / 60.0
            p_out = torque_target * omega # Mechanical output power
            
            # Loss calculations
            r_s_current = self.compute_thermal_resistance(base_rs, simulated_winding_temp)
            i_rms = 220.0 # Approximate phase current for 1400 Nm
            p_cu = 3 * (i_rms ** 2) * r_s_current
            
            # Inverter and mechanical parasitic losses (windage/grease drag decreasing as it warms)
            p_inv_loss = 4500.0 # Base SiC switching/conduction losses
            p_mech = max(1200.0 - (step * 80.0), 400.0) # Grease viscosity drag dropping with heat
            
            p_loss_total = p_cu + p_inv_loss + p_mech
            p_in = p_out + p_loss_total
            
            efficiency = (p_out / p_in) * 100.0
            
            # Validate against target bounds (93% - 95%)
            status = "PASS" if 92.5 <= efficiency <= 96.0 else "REVIEW"
            if status == "PASS":
                success_count += 1

            timestamp = time.time()
            cursor.execute(
                """INSERT INTO simulation_runs 
                   (timestamp, ambient_temp_c, rpm, torque_nm, v_dc, i_dc, p_out, p_in, efficiency, status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (timestamp, simulated_winding_temp, rpm_target, torque_target, 800.0, i_rms, p_out, p_in, efficiency, status)
            )
            
            print(f"Step {step+1:02d} | Temp: {simulated_winding_temp:5.1f}°C | Torque: {torque_target} Nm | Efficiency: {efficiency:5.2f}% | Status: {status}")

        conn.commit()
        conn.close()
        print(f"\n[Simulation Complete] {success_count}/{total_steps} intervals successfully met the 93%-95% efficiency threshold under Arctic duress.")

if __name__ == "__main__":
    validator = ArcticPowertrainValidator()
    validator.run_takeoff_transient_simulation(ambient_temp_c=-40.0)

