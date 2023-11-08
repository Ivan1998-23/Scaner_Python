import argparse, os, sys, netaddr, logging, time
from manuf import manuf
from flask import Flask, render_template
from flask import request
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument("subnet",type=str,help="subnet value to scan")
parser.add_argument("--port","-p",type=int,help="listening port (default 6500)")
parser.add_argument("--logs","-l",type=str,help="saved log file")
parser.add_argument("--seconds","-s",type=int,help="given seconds between scan intervals")
args = parser.parse_args()


def netscan(subnet,app,seconds): # function to scan subnet, and add active hosts to list
    try:
        global finished;finished = False # states if the scan is completed or not
        time.sleep(seconds)
        p = manuf.MacParser(update=True)
        for i in netaddr.IPNetwork(subnet):
            mac = networking.arpback(i)
            if not "None" in str(mac):
                information = {"IP" : i,
                               "MAC" : mac,
                               "OS" : networking.osfetch(i),
                               "MANUF" : p.get_manuf(str(mac))
                               }
                devinfo.append(information)
        finished = True
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    sys.path.append(f'{os.path.abspath(os.getcwd())}/src');import networking

    subnet = args.subnet # subnet value
    lstport = 6500 if not args.port else args.port # 6500 default listening port
    logfile = "logfile.txt" if not args.logs else args.logs # logfile.txt default log file
    seconds = 0 if not args.seconds else args.seconds
    devinfo = [] # contains dictionary information of hosts

    logging.basicConfig(filename=logfile,
                    format='%(asctime)s %(message)s',
                    filemode='w')
    logger = logging.getLogger()

    app = Flask(__name__)

    @app.route("/") # index.html render
    def index():
        return render_template('index.html', devices=devinfo, net=subnet)

    @app.route('/report') # report.html render
    def device():
        return render_template('report.html', devices=len(devinfo), finished=finished)

    @app.route('/logging') # logging.html render
    def logging():
        loglist = open(logfile,"r").read().splitlines()
        return render_template('logging.html', logdata=loglist, logamount=len(loglist))

    @app.route('/about') # about.html render
    def about():
        return render_template('about.html')

    try:   
        thrd = Thread(target=netscan, args=(subnet,app,seconds)) # create thread to scan devices
        thrd.start() # starts thread
        app.run(debug = True, port=lstport) # starts web application
    except KeyboardInterrupt: # if Ctrl + c
        exit()

# Author: Xeonrx
# Source: https://github.com/Xeonrx/deaddrops
