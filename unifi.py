import logging
import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from pushsafer import init, Client
from time import sleep

init(os.environ.get("PRIVATE_KEY"))
pushClient = Client("iPhone")

url = "https://store.ui.com/collections/unifi-protect-cameras/products/uvc-g4-doorbell"
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



def check_inventory():
    resp = requests.get(url)
    if resp.status_code != 200:
        logger.info("Did not get a valid response from unifi")
        pushClient.send_message("Cannot reach Unifi Website!", "Unifi Doorbell Inventory Check", os.environ.get("CLIENT_ID"),"1", "", "2", url, "Open UI Store", "0", "1", "120", "1200", "0", "", "", "")
        return
    soup = BeautifulSoup(resp.text, "html.parser")

    pattern = re.compile('"inventory_quantity":[0-999999]')

    script = soup.find("script", text=pattern)
    if script:
        match = pattern.search(str(script))
        if match:
            match_ob = match.group()
            if match_ob[-1].strip() == "0":
                logger.info("No inventory, checking again in 30 seconds")
                sleep(30)
                return check_inventory()
            else:
                logger.info(f"Quantity available: {match_ob[-1]}")
                pushClient.send_message("Doorbell available!", "Unifi Doorbell Inventory Check", os.environ.get("CLIENT_ID"),"1", "", "2", url, "Open UI Store", "0", "1", "120", "1200", "0", "", "", "")
                return

logger.info("Starting service")
try:
    check_inventory()
except KeyboardInterrupt:
    # quit
    logger.info("Interrupt received, shutting down")
    sys.exit()
