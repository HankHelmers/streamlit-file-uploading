import streamlit as st
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import SequencePacking


# Title and info
st.title("Data Explorer :crystal_ball:")
# st.info("The DataExplorer is an interactive web application designed to empower users to perform Exploratory Data Analysis (EDA) with ease and efficiency. With this intuitive tool, users can upload their datasets in CSV format, and the application will swiftly process and visualize the data to gain valuable insights.")


# 1. Loading the data
def load_data():
    uploaded_file = st.file_uploader("1. Upload a CSV file", type=["csv","exl"])

    if uploaded_file is not None:
        try:
            # Try reading the CSV file
            data = pd.read_csv(uploaded_file)
            return data
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            return None
        
data = load_data()


# 2. Data Verification
if data is not None:
    st.header("2. Data loaded successfully! :sunglasses:")
    st.dataframe(data)
    st.write("We can now go through and collect all CDS sequences for each BLAST result!")

## SCRAPING -------------------------------------------------------------------------------------------

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
        st.write("Starting Automator...")
        driver = webdriver.Chrome(options=options)
        st.write("Automator started successfully.")
    except Exception as e:
        st.write(f"Error starting Automator: {e}")
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



# 3. Do Operation
    #for i in range(len(urls)): # length of URLS
if data is not None:
    urls = getURLsFromDatabase(data)

    startWebDriver()
    
    sequence_objs = []
    sequence_errors = []

    organism = "Wheat"
    description = "CPS4"  
    dataset = "Triticum aestivum cv. Chinese Spring v2.1"
    #getGeneData(urls[2], description, organism, dataset)

# PARSING THE DATA
# Extract data from the sequence_obj array
#     data = [
#         {
#             'URL': gene.url,
#             'Name': gene.name,
#             'Description': gene.description,
#             'Organism': gene.organism,
#             'Dataset': gene.dataset,
#             'Sequence': gene.sequence
#         }
#         for gene in sequence_obj
#     ]

#     # Print list of arrays at end
#     print("Final errors noted: ")
#     for error in gene_errors:
#         print("Error at " + str(error))

#     # Create a DataFrame from the data
#     df = pd.DataFrame(data)

#     # Save the DataFrame to a CSV file
#     df.to_csv('output.csv', index=False)

#     print("CSV file 'output.csv' has been created successfully.")

# progress_text = "Operation in progress. Please wait."
# my_bar = st.progress(0, text=progress_text)

# for percent_complete in range(100):
#     time.sleep(0.01)
#     my_bar.progress(percent_complete + 1, text=progress_text)
# time.sleep(1)
# my_bar.empty()

# st.button("Rerun")

