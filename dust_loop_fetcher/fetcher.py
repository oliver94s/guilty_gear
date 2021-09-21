import copy
import json
import logging 
import os
import socket
import sys

socket.setdefaulttimeout(3)

logging.basicConfig(filename='fetcher.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import Image


characters = [
    "Anji_Mito",
    "Axl_Low",
    "Chipp_Zanuff",
    "Faust",
    "Giovanna",
    "Goldlewis_Dickinson",
    "I-No",
    "Jack-O",
    "Ky_Kiske",
    "Leo_Whitefang",
    "May",
    "Millia_Rage",
    "Nagoriyuki",
    "Potemkin",
    "Ramlethal_Valentine",
    "Sol_Badguy",
    "Zato-1"
]

DUSTLOOP_COM = "https://www.dustloop.com/wiki/index.php?title=GGST/{}/Frame_Data"

def fetch_char_frame_data(character):
    logging.info("Fetching data for %s" % character)
    try:
        with urlopen(DUSTLOOP_COM.format(character), timeout=5) as f:
            myfile = f.read()
            soup = BeautifulSoup(myfile, 'html.parser')
    except:
        print('failed to collect data for character: %s' % character)
        logging.error("Ran into Error: %s" % sys.exc_info()[0].message)
        logging.error("Failed to fetch data for character: %s" % character)
        return 
    
    frame_data = []

    tables = soup.find_all("table", class_="cargoDynamicTable display")    
    for table in tables:
        t_header = table.find('thead')
        rows = t_header.find_all('tr')
        headers = {}
        for row in rows:
            header_cols = row.find_all('th')
            header_cols = [ele.text.strip() for ele in header_cols]
            # should try to get rid of the first columns
            for col in header_cols:
                if col not in headers:
                    headers[col] = None

        t_body = table.find('tbody')
        rows = t_body.find_all('tr')
        for row in rows:
            temp_headers = copy.deepcopy(headers)
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            for idx in range(len(header_cols)):
                temp_headers[header_cols[idx]] = cols[idx]
            
            frame_data.append(temp_headers)
    
    output_dir = os.path.join("frame_data")
    frame_data_json = os.path.join(output_dir, "%s.json" % character)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(frame_data_json, 'w') as f:
        json.dump(frame_data, f, indent=4)
    
    logging.info("Successfully fetched data for %s" % character)

DUSTLOOP_GUILTY_GEAR_STRIVE_INDEX = "https://dustloop.com/wiki/index.php?title=Guilty_Gear_-Strive-"
DUSTLOOP = "https://dustloop.com"

def fetch_char_icons(character):
    try:
        with urlopen(DUSTLOOP_GUILTY_GEAR_STRIVE_INDEX, timeout=5) as f:
            myfile = f.read()
            soup = BeautifulSoup(myfile, 'html.parser')
    except:
        print('failed to collect data for character: %s' % character)
        logging.error("Ran into Error: %s" % sys.exc_info()[0].message)
        logging.error("Failed to fetch data for character: %s" % character)
        return

    hrefs = soup.find_all("a", href="/wiki/index.php?title=GGST/%s" % character)
    for href in hrefs:
        logging.info("looking character icon %s" % character)
        url = "%s%s" % (DUSTLOOP, href.contents[0]['src'])
        icon_dir = os.path.join('icons')
        output_png = os.path.join(icon_dir, "%s.png" % character)
        if not os.path.exists(icon_dir):
            os.makedirs(icon_dir)
        
        retry_count = 5
        while retry_count < 5:
            try:
                urllib.request.urlretrieve(url, output_png)
            except urllib.error.URLError:
                logging.error("Failed to fetch data for character: %s. Retry attempt %d out of %d" % (character, retry_count, 5))
        
        return
    logging.info("Successfully got icon for %s" % character)

if __name__ == "__main__":
    for character in characters:
        fetch_char_frame_data(character)
        fetch_char_icons(character)
