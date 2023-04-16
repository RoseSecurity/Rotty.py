#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Back, Style
from crontab import CronTab
from getpass import getpass
import platform
import time
import sys
import os

# Ensure you run with administrative privileges

# Nmap variables (these can be configured for your needs)

Options = "-sS -F -T4 -n -vv"

# System variables

OS = platform.system()
Home = str(Path.home())
Date = datetime.today().strftime('%Y-%m-%d')
WindowsPath = r"C:\Users\HomeNetworkMonitoring"
POSIXPath = r"/tmp/HomeNetworkMonitoring"
WindowsDirectoryPath = os.path.isdir(WindowsPath)
POSIXDirectoryPath = os.path.isdir(POSIXPath)

def Banner():
    time.sleep(0.5)
    Rotty = """\n   / \__
  (    @\___
  /         O
 /   (_____/
/_____/   U"""
    
    print (Fore.BLUE + Rotty)
    time.sleep(2.5)
    Title = """______      _   _         
| ___ \    | | | |        
| |_/ /___ | |_| |_ _   _ 
|    // _ \| __| __| | | |
| |\ \ (_) | |_| |_| |_| |
\_| \_\___/ \__|\__|\__, |
                     __/ |
                    |___/ \n"""
    print (Fore.RED + Title)
    time.sleep(2)
    print(Style.RESET_ALL)
    print("Welcome to Rotty.py, a home network monitoring solution that provides insight and visibility into the dynamic and changing nature of your personal network. To use the tool, we have a few questions for you to answer so that we can begin!\n")
    time.sleep(3)

def SetUp(): 
    time.sleep(1)
    global Network
    global Email
    global EmailPassword
    Network = input("Enter the IP Address and CIDR of your home network (Example: 10.0.0.0\\8, 192.168.1.0\\16, 172.16.0.0\\12)\n:")
    Email = input("\nEnter the email address for generated alerts\n:")
    EmailPassword = getpass("\nEnter your email address password\n:")

    if OS == "Windows":
        os.mkdir(WindowsPath)
        os.chdir(WindowsPath)
        OGState = sys.stdout
        with open(r"C:\Users\HomeNetworkMonitoring\Baseline_NetworkScan", "w+") as WindowsScan:
            sys.stdout = WindowsScan
            Mapper = nmap.PortScanner()
            Mapper.scan(Network, arguments=Options)
            print(Mapper.csv())
            sys.stdout = OGState
    else:
        os.mkdir(POSIXPath)
        os.chdir(POSIXPath)
        OGState = sys.stdout
        with open(r"/tmp/HomeNetworkMonitoring/Baseline_NetworkScan", "w+") as LinuxScan:
            sys.stdout = LinuxScan
            Mapper = nmap.PortScanner()
            Mapper.scan(Network, arguments=Options)
            print(Mapper.csv())
            sys.stdout = OGState
    print(Fore.GREEN + "Network Baseline has been generated!")
    print(Style.RESET_ALL)

def NmapScan():

# Windows Scan

    if WindowsDirectoryPath == True:
            OGState = sys.stdout
            with open("C:\\Users\HomeNetworkMonitoring\\{}_NetworkScan".format(Date), "w+") as WindowsScan:
                sys.stdout = WindowsScan
                Mapper = nmap.PortScanner()
                Mapper.scan(Network, arguments=Options)
                print(Mapper.csv())
                sys.stdout = OGState

# POSIX Scan

    else:
            OGState = sys.stdout
            with open("/tmp/HomeNetworkMonitoring/{}_NetworkScan".format(Date), "w+") as LinuxScan:
                sys.stdout = LinuxScan
                Mapper = nmap.PortScanner()
                Mapper.scan(Network, arguments=Options)
                print(Mapper.csv())
                sys.stdout = OGState
    
def CompareScans():
    
    if OS == "Windows":
        with open(r"C:\Users\HomeNetworkMonitoring\Baseline_NetworkScan", 'r') as Baseline, open("C:\\Users\HomeNetworkMonitoring\\{}_NetworkScan".format(Date), 'r') as NewScan:
            Baseline = Baseline.readlines()
            NewScan = NewScan.readlines()

        with open(r"C:\Users\HomeNetworkMonitoring\Modified_Network_Alert", 'w') as outFile:
            for line in NewScan:
                if line not in Baseline:
                    outFile.write(line)
    else:
        with open(r"/tmp/HomeNetworkMonitoring/Baseline_NetworkScan", 'r') as Baseline, open("/tmp/HomeNetworkMonitoring/{}_NetworkScan".format(Date), 'r') as NewScan:
            Baseline = Baseline.readlines()
            NewScan = NewScan.readlines()

        with open(r"/tmp/HomeNetworkMonitoring/Modified_Network_Alert", 'w') as outFile:
            for line in NewScan:
                if line not in Baseline:
                    outFile.write(line)

def EmailAlert():
    
    if OS == "Windows":
        Subject = "Home Network Monitoring Alert"
        Body = "Your home network has generated a new alert; the attached file will provide you with information on which activity has deviated from your network baseline."
        
        message = MIMEMultipart()
        message["From"] = Email
        message["To"] = Email
        message["Subject"] = Subject
        message.attach(MIMEText(Body, "plain"))

        NetworkAlert = r"C:\Users\HomeNetworkMonitoring\Modified_Network_Alert"  

        with open(NetworkAlert, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {NetworkAlert}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(Email, EmailPassword)
            server.sendmail(Email, Email, text)
    else:
        Subject = "Home Network Monitoring Alert"
        Body = "Your home network has generated a new alert; the attached file will provide you with information on which activity has deviated from your network baseline."
        
        message = MIMEMultipart()
        message["From"] = Email
        message["To"] = Email
        message["Subject"] = Subject
        message.attach(MIMEText(Body, "plain"))

        NetworkAlert = r"/tmp/HomeNetworkMonitoring/Modified_Network_Alert"  

        with open(NetworkAlert, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {NetworkAlert}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(Email, EmailPassword)
            server.sendmail(Email, Email, text)

def DeleteAlert():
    if OS == "Windows":
        os.remove(r"C:\Users\HomeNetworkMonitoring\Modified_Network_Alert")
    else:
        os.remove(r"/tmp/HomeNetworkMonitoring/Modified_Network_Alert")

if POSIXDirectoryPath == False:
    Banner()
    SetUp()
elif WindowsDirectoryPath == False:
    Banner()
    SetUp()
elif POSIXDirectoryPath == True:
    NmapScan()
    CompareScans()
    EmailAlert()
    DeleteAlert()
elif WindowsDirectoryPath == True:
    NmapScan()
    CompareScans()
    EmailAlert()
    DeleteAlert()
