import requests 
import logging
import json
import os
import csv

# Grab env vars
TOKEN = os.environ.get("NETSKOPE_TOKEN")
URL = os.environ.get("TENANT_URL")
URLHAUS = "https://urlhaus.abuse.ch/downloads/csv_online/"

# Setup the logger
logging.basicConfig(format='%(asctime)s - %(message)s',
                    filename='../logs/request.log', level=logging.DEBUG)
# Spit logs to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)
logger = logging.getLogger()

def get_urlhaus():
    """Grab the abuse DB and slice off the headings"""
    r = requests.get(URLHAUS)
    with open('urlhaus.csv', "w") as f:
        f.write(r.text)
    with open('urlhaus.csv', "r+") as f1:
        lines = f1.readlines()
        f1.seek(0)
        f1.truncate()
        f1.writelines(lines[8:])

def parse_url_list():
    """Parse the abuse DB and make a list of only the URLs"""
    url_list = []
    with open("urlhaus.csv") as f:
        data = csv.reader(f)
        for row in data:
            # This is real dirty, for production workloads, spend more time parsing the list
            if row[2] != "url" and "^" not in row[2] and ":1636/4" not in row[2]:
                url_list.append(row[2])
    
    return url_list

def post_url_list(list):
    """Post the URL list to your Netskope Tenant"""
    headers = {
        "Accept": "application/json",
        "Netskope-Api-Token": TOKEN,
        "Content-Type": "application/json"
    }

    body = {
        "name": "Test-UrlHaus",
        "data": {
            "urls": list,
            "type": "exact"
        }
    }

    r = requests.post(f"{URL}/api/v2/policy/urllist", headers=headers, data=json.dumps(body))

    return r.text

if __name__ == "__main__":
    logger.info("Populating the Haus URL list")
    get_urlhaus()
    logger.info("Parsing the Haus DB, sanitizing, and returning a list of URLs")
    url_list = parse_url_list()
    logger.info("Posting the URL list to your Netskope Tenant")
    post_to_tenant = post_url_list(url_list)
    logger.info(post_to_tenant)
    
