# Title: Extract Genes from URLs Script
# Date: June 5th, 2024  
# Author: Hank Helmers, Fungal Genomics & Comp. Biology REU Participant
#
# Description:
# * Input BLAST output csv, including the URLs in the first column
# * Opens each URL, extracts the gene name and sequence from the website
# * Saves them all into an outputted CSV
# * If an error occurs, it is also saved in the CSV with name "Error"
#   the URLs are included in the output, so each error can be inspected. 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

import SequencePacking

# Get URLs as Array from CSV database
# 
# Inputs:
# * filename - name of local file which contains the URLs to extract from in FIRST column
#
# Returns:
# * result - array of the urls in the FIRST column on inputted CSV
def getURLsFromDatabase(data):
    # Get the first column
    first_column = data.iloc[:, 0]

    # Find the index of the first blank cell
    blank_index = first_column[first_column.isnull() | (first_column == '')].index[0]
    # Extract strings up to the blank cell
    result = first_column[:blank_index].tolist()

    return result


def getGeneData(url, description, organism, dataset):
    # try:
    sequence_obj = getCDSfromURL(url, description, organism, dataset)
    return sequence_obj

    # If there is an error:
    # * An error gene object will be added to the output
    # * A list will be held of error indexes
    # except Exception as e: 
    #     #sequence_obj.append(SequencePacking('https://'+urls[i], "Error", description, organism, "Empty?", dataset))
    #     #gene_errors.append(i)
    #     print("Error)


## Returns the SequencePacking from a single URL
def getCDSfromURL(url, description, organism, dataset):
    startWebDriver()
    clickTranscriptDNA(url)
    geneName = getGeneName()
    cdsText = getCDS()
    print(geneName)
    print(cdsText)
    return SequencePacking(url, geneName, description, organism, dataset, cdsText)

def startWebDriver():
    global driver
    options = Options()
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode
    options.add_argument("--no-sandbox")  # Required in some environments (e.g., Docker)
    options.add_argument("--disable-dev-shm-usage")  # Avoids issues with shared memory in Docker
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (optional)
    options.add_argument("--remote-debugging-port=9222")  # Enable debugging
    options.add_argument("--disable-software-rasterizer")  # Optional, to further disable software rendering
    
    try:
        print("Starting Automator...")
        driver = webdriver.Chrome(options=options)
        print("Automator started successfully.")
    except Exception as e:
        print(f"Error starting Automator: {e}")
        raise e

def getGeneName():
    global driver
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/dl/dd[1]'))
    )
    print(element.text)

    name = element.text
    print(name.split("\n"))  # Splits into an array of elements each split where there was an '\n', in this case [header], [sequence]
    return name.split("\n")[0]

## Click transcriptDNA taking to full info page
def clickTranscriptDNA(url):
    global driver
    driver.get(url)
    
    # Wait for page to load
    time.sleep(10)

    print('Page Loaded!')

    # Look for element
    element = driver.find_element(By.XPATH, '//*[@id="track_Transcripts"]/canvas')
    element.click()
    print(driver.current_url)

def getCDS():
    global driver
    ## Click button to go to Blast
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[4]/div[4]/label/div/div/a/button/span'))
    )
    element.click()
    
    element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div/div/form/fieldset/textarea'))
    )
    sequence = element.text
    return sequence.split("\n")[1]