# ADS-B Security Analysis

A practical aerospace cybersecurity project demonstrating real attack surfaces in ADS-B — the protocol modern aircraft use to broadcast position, altitude, and velocity. This project captures live aircraft data, models threat vectors, detects anomalies, and visualizes findings on an interactive map.

## Why This Matters

ADS-B was designed in the 1990s with no encryption and no authentication. Any aircraft's position, altitude, and identity can be received by anyone with basic SDR hardware, and the protocol has no built-in way to verify that a broadcast is genuine. This makes it a documented attack surface for spoofing and signal injection — a relevant concern in aviation and aerospace cybersecurity.

This project demonstrates that vulnerability practically: capturing real flight data and flagging the kind of anomalies a spoofed or malicious broadcast would produce.

## Threat Model

**Asset:** ADS-B broadcast signal from commercial and general aviation aircraft

**Attackers:** Anyone with ~$30 SDR hardware and basic RF knowledge

**Attack Vectors:**

| Attack | Description | Real-world Impact |
|--------|-------------|-------------------|
| Position Spoofing | Inject fake aircraft at arbitrary coordinates | False traffic alerts, ATC confusion |
| Ghost Aircraft | Broadcast non-existent flights with valid ICAO24 | Runway incursions, collision avoidance failures |
| ICAO24 Cloning | Duplicate a real aircraft's identifier | Impersonation, tracking evasion |
| Denial of Service | Flood receiver with fake broadcasts | Overwhelm ATC displays, blind ground stations |

**Why No Fix Exists Yet:** ADS-B was standardised before authentication was a design requirement. Retrofitting cryptographic verification across global aviation infrastructure is a multi-decade, multi-billion dollar problem. ICAO is actively working on ADS-B authentication standards (draft stage as of 2025).

**What This Project Detects:** Anomalies consistent with spoofing attempts — anonymous broadcasts, duplicate identifiers, physically impossible position jumps, altitude-velocity inconsistencies.

## What It Does

- **Captures live aircraft data** from the OpenSky Network API (real flights, real positions)
- **Analyzes the data for security red flags:**
  - Aircraft broadcasting with no callsign (anonymous/unidentifiable)
  - Duplicate ICAO24 addresses (possible spoofing indicator)
  - Abnormal altitude readings
  - High altitude paired with near-zero velocity (signal anomaly indicator)
- **Continuously monitors** for impossible position jumps between captures
- **Visualizes results** on an interactive map, color-coded by risk

## Project Structure

```
├── fetch_adsb.py         # Pulls live aircraft data from OpenSky Network API
├── analyze_security.py   # Runs security checks on captured data
├── visualize.py          # Generates interactive map of aircraft positions
├── monitor_anomalies.py  # Continuous monitoring — detects impossible position jumps
├── aircraft_data.json    # Sample captured data
└── aircraft_map.html     # Sample generated map
```

## Usage

```bash
# Install dependencies
pip install requests pandas matplotlib folium

# 1. Fetch live aircraft data
python fetch_adsb.py

# 2. Run security analysis
python analyze_security.py

# 3. Generate interactive map
python visualize.py

# 4. Run continuous monitoring
python monitor_anomalies.py
```

Open `aircraft_map.html` in a browser to view results. Red markers = anonymous flights. Blue markers = normal.

## Sample Findings

A single capture of 50 live aircraft flagged one anonymous flight (no callsign broadcast) — a real example of the kind of unidentifiable traffic ADS-B's lack of authentication permits.

## Background

ADS-B is the backbone of modern air traffic surveillance, used globally by ATC and aircraft for tracking. Because it broadcasts in the clear, security researchers have repeatedly demonstrated that it is possible to inject fake aircraft, spoof positions, or impersonate existing flights using low-cost SDR hardware. This project is a practical, data-driven look at that exposure.

## Tech Stack

Python, OpenSky Network API, Folium, Pandas

## Author

B Bineesh — ECE Avionics, Central University of Jammu  
TryHackMe: Top 5% | IBM Cybersecurity Analyst (in progress)  
Focus: Aerospace and Drone Cybersecurity | Red Team