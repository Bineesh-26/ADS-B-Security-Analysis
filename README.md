# ADS-B Security Analysis

Security analysis tool for ADS-B (Automatic Dependent Surveillance-Broadcast), the protocol modern aircraft use to broadcast position, altitude, and velocity. This project captures live aircraft data, analyzes it for security anomalies, and visualizes findings on an interactive map.

## Why This Matters

ADS-B was designed in the 1990s with no encryption and no authentication. Any aircraft's position, altitude, and identity can be received by anyone with basic SDR hardware, and the protocol has no built-in way to verify that a broadcast is genuine. This makes it a documented attack surface for spoofing and signal injection — a relevant concern in aviation and aerospace cybersecurity.

This project demonstrates that vulnerability practically: capturing real flight data and flagging the kind of anomalies a spoofed or malicious broadcast would produce.

## What It Does

- **Captures live aircraft data** from the OpenSky Network API (real flights, real positions)
- **Analyzes the data for security red flags:**
  - Aircraft broadcasting with no callsign (anonymous/unidentifiable)
  - Duplicate ICAO24 addresses (possible spoofing indicator)
  - Abnormal altitude readings
  - High altitude paired with near-zero velocity (signal anomaly indicator)
- **Visualizes results** on an interactive map, color-coded by risk

## Project Structure

```
├── fetch_adsb.py        # Pulls live aircraft data from OpenSky Network API
├── analyze_security.py  # Runs security checks on captured data
├── visualize.py          # Generates interactive map of aircraft positions
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
```

Open `aircraft_map.html` in a browser to view the result. Red markers indicate anonymous flights (no callsign); blue markers are normal.

## Sample Findings

A single capture of 50 live aircraft flagged one anonymous flight (no callsign broadcast) — a real example of the kind of unidentifiable traffic ADS-B's lack of authentication permits.

## Background

ADS-B is the backbone of modern air traffic surveillance, used globally by ATC and aircraft for tracking. Because it broadcasts in the clear, security researchers have repeatedly demonstrated that it's possible to inject fake aircraft, spoof positions, or impersonate existing flights using low-cost SDR hardware. This project is a practical, data-driven look at that exposure.

## Tech Stack

Python, OpenSky Network API, Folium (mapping), Pandas

## Author

Bineesh Baburajan — ECE (Avionics), Central University of Jammu
