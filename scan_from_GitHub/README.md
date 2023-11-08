![sample](https://github.com/Xeonrx/deaddrops/blob/main/img/sample.png)

Discover active hosts on your local network, with a slick UI to come along with it :)

Deaddrops was a python project developed using Flask, for mainly offensive pentesting host discovery. <br />
This is a project in development, and will receive updates & fixes in the future.

# Features
- Scan for active hosts
- Retreive mac address and mac vendor
- Windows & Linux identification
- Stealth configurable
- Logfile & reports page

![osinfo](https://github.com/Xeonrx/deaddrops/blob/main/img/OSinfo.png) <br />
*Don't rely on OS detection to be 100% accurate.*

# Installation
- Clone the git repo
- cd into directory
- Install the needed py modules via pip: `pip install flask python-nmap manuf netaddr scapy`
- `python3 deaddrops.py -h`

**Note: This script has only been officially tested on Linux.**

# Usage
`python3 deaddrops.py {SUBNET VALUE}` (ex. `python3 deaddrops.py 10.0.0.1/24`)

### Optional Usage
`-p --port` change listening port (default 6500) <br />
`-s --seconds` seconds between scan interval (default 0) <br />
`-l --logs` saved logfile (default logfile.txt)

**After running the script, you can open the webapp via browser. The scan will start automacially.**

# Future Plans
- Port scanning & service enumeration
- Customizeable color pallets
- Mac and mobile detection
- Dynamic charts for report.html
