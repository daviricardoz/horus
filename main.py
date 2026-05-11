#!/usr/bin/env python3
import requests
import itertools
import threading
import readline
import rlcompleter
import subprocess
import socks
import ssl
import socket
import json
import urllib.request 
import urllib.parse
import time
import cmd
import os
from colored import Fore, Back, Style 
from settings import VT_API_KEY
from datetime import datetime

# Available OSINT tools
osint_list = [
    ["ip_check", "https://www.virustotal.com/api/v3/ip_addresses/"]
]

# Get proxy and ISP IP Address
url_tproxy = "https://httpbin.org/ip"
url_pubcip = "https://ipinfo.io"
# Global variables to handle IP's
proxied = None
public  = None
# Tor session 
tor = None

# Shell and their commands to Horus 
class user_shell(cmd.Cmd):
    prompt = "<O> "

    def __init__(self):
        super().__init__()
        readline.set_completer(rlcompleter.Completer(self.__dict__).complete)
        readline.parse_and_bind("tab complete")

    def do_search_nick(self, arg):
        if os.system(f"proxychains4 -q sherlock {arg} -fo users_search/") != 0:
            print(f"Failed trying to search for users: {arg}")
            
    def do_search_ip(self, arg):
        to_query = osint_list[0][1] + arg
        gsession = tsession()

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(to_query, headers={'X-Apikey': VT_API_KEY})
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9060)
        socket.socket = socks.socksocket

        print(to_query)

        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                data = json.load(resp)
                attr = data.get('data', {}).get('attributes', {})

                last_analysis_stats = attr.get('last_analysis_stats', {})
                last_analysis_date = str({attr.get('last_analysis_date')}).strip("{}")
                last_analysis_date = int(last_analysis_date)
                
                date_formatted = datetime.fromtimestamp(last_analysis_date)
                
                pars = [
                    f"IP: {arg}",
                    f"Owner: {attr.get('as_owner')}",
                    f"ASN: {attr.get('asn')}",
                    f"Continent: {attr.get('continent')}",
                    f"Country: {attr.get('country')}",
                    f"JARM: {attr.get('country')}",
                    f"Last Analysis: {date_formatted}",
                    f"Reputation Score: {attr.get('reputation')}",
                    f"Tags: {', '.join(attr.get('tags', []))}",
                    "Last Analysis Stats:",
                    f" Harmless: {last_analysis_stats.get('harmless', 0)}",
                    f" Malicious: {last_analysis_stats.get('malicious', 0)}",
                    f" Suspicious: {last_analysis_stats.get('suspicious', 0)}",
                    f" Timeout: {last_analysis_stats.get('timeout', 0)}",
                    f" Undected: {last_analysis_stats.get('undected', 0)}",
                    f"Last HTTPS Certification Date: {attr.get('last_https_certificate_date')}",
                    f"Last Modification Date: {attr.get('last_modification_date')}",
                    f"Network: {attr.get('network')}",
                    f"RIR: {attr.get('regional_internet_registry')}",
                    f"WHOIS: {attr.get('whois')}",
                    f"WHOIS Data: {attr.get('whois_data')}",
                ]
                print("\n".join(pars))
        except urllib.error.URLError as e:
            print("[x] Request failed. Check the ip address and the proxy configuration.")
        except Exception as e:
            print("[x] Unexpected error. Debug the system.")

    def do_quit(self, arg):
        os._exit(os.EX_OK)

    def do_exit(self, arg):
        os._exit(os.EX_OK)

    def default(self, line):
        print("[x] Command doesn't exists")
        return

# Get pubip
def mypub_ip():
    global public
    params = {"format": "json"}
    public = (requests.get(url_pubcip, params=params)).json()

# Define proxy
def tsession():
    session = requests.session()
    session.proxies = {'http':   'socks5://127.0.0.1:9060',
                       'https':  'socks5://127.0.0.1:9060',
                       'socks5h': 'socks5h://127.0.0.1:9060'}
    return session

# Get the proxied IP Address
def tproxy(tor):
    global proxied
    params = {"format": "json"}
    proxied = (tor.get(url_tproxy, params=params)).json()

# Main
def main():
    global tor
    tor = tsession()
    t1 = threading.Thread(target=tproxy(tor), daemon=False)
    t2 = threading.Thread(target=mypub_ip(), daemon=False)

    t1.start()
    t2.start()

    color: str = f'{Style.underline}{Fore.cyan}{Back.black}'
    s = ''.join(itertools.repeat("-", 60))

    print(f'{color}{s}{Style.reset}')

    t1.join()
    print("[=] Your TOR public IP: " + proxied['origin'])
    t2.join()
    print("[=] Your ISP public IP: " + public['ip'])

    if proxied['origin'] != public['ip']:
        print("[+] Your proxy is currently working. Going on.")
    else:
        os._exit(os.EX_OK)

    print(f'{color}{s}{Style.reset}')

    user_shell().cmdloop()

# Beginning
if __name__ == "__main__":
    main()
