
<p align="center">
  <img src="https://i.ibb.co/G4Zj8qpZ/unnamed.png" alt="banner" width="600"/>
</p>

# SkyScan

SkyScan is a Python3 reconnaissance script that fetches real-time aircraft data from the OpenSky Network API. It supports tracking aircraft within a specified radius of geographic coordinates, either auto-detected or manually entered. Designed for terminal use with Arabic and English interface options, it is ideal for OSINT operations, SIGINT simulations, and aviation research. The tool runs smoothly on penetration testing distros like Kali Linux.

## Features

- Real-time aircraft tracking via OpenSky API  
- IP-based auto-geolocation or manual coordinate input  
- Radius-based aircraft filtering  
- Flight metadata: callsign, altitude, velocity, heading, distance, aircraft type  
- Multilingual terminal interface (Arabic / English)  
- Automatic refresh every 30 seconds  
- ANSI-colored output for better readability

## Installation & Usage

1. **Update your system (optional):**  
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install Python3 & venv (if not already installed):**  
```bash
sudo apt install python3 python3-venv -y
```

3. **Create a Virtual Environment:**  
```bash
python3 -m venv skyscan-env
```

4. **Activate the Virtual Environment:**  
```bash
source skyscan-env/bin/activate
```

5. **Install Required Libraries:**  
```bash
pip install requests geopy
```

6. **Running SkyScan:**  

- Place `skyscan.py` inside your working directory.
- Make sure you're in the virtual environment:  
```bash
source skyscan-env/bin/activate
```
- Run the script:  
```bash
python3 skyscan.py
```
- Follow the CLI prompts to select language, input or auto-detect coordinates, and define search radius.

## Notes

- No API key needed, but rate limits may apply.  
- Data accuracy depends on OpenSky’s public feed.  
- For educational and lawful reconnaissance use only.

## Author

Discord & Telegram: `0xnoag`
