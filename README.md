![banner](https://i.ibb.co/G4Zj8qpZ/unnamed.png)

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


2. Install Python3 & venv (if not already installed)                                  
sudo apt install python3 python3-venv -y
                                    
3. Create a Virtual Environment
You should now see the environment name ((skyscan-env)) in your terminal prompt.                             
python3 -m venv skyscan-env
                                    
4. Activate the Virtual Environment
skyscan-env/bin/activate
                                 
5. Install Required Libraries
This ensures all dependencies used by skyscan.py are installed within the virtual environment.                                 
pip install requests geopy

                                    
Running SkyScan
Place skyscan.py inside your working directory.

Make sure you're in the virtual environment:
yscan-env/bin/activate

                                    
Run the script:                                
python3 skyscan.py

                                    
Follow the CLI prompts to select language, input or auto-detect coordinates, and define search radius. The tool will continuously scan and update results until interrupted (Ctrl+C).

Notes
No OpenSky API key is required for basic functionality, but data may be limited due to rate limits.
Accuracy of aircraft information depends on the quality of OpenSky’s public data feed.
Use responsibly. This tool is for educational and lawful reconnaissance only.

Author:
Discord & Telegram : 0xnoag
