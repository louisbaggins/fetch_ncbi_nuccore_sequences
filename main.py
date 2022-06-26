from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

#  set search database type to nucleotide (nuccore)
def set_nucleotide():
    select = Select(browser.find_element(value='database'))
    browser.find_element(value='database').click()
    select.select_by_value('nuccore')

# download FASTA file by sequence id
def download_sequence(sequence_id: str):
    # click on search bar and input sequence id
    browser.find_element(value='term').click()
    input_sequence = browser.find_element(value='term')
    input_sequence.send_keys(sequence_id)

    # click on send to element
    browser.find_element(value='search').click()
    browser.find_element(value='seqsendto').click()
    time.sleep(2)
    browser.find_element(By.XPATH, value='//*[@id="dest_File"]').click()

    # define file format
    time.sleep(1)
    browser.find_element(value='file_format').click()                  
    file_format_select = Select(browser.find_element(value='file_format'))
    file_format_select.select_by_value('fasta')

    # click download file
    browser.find_element(by=By.XPATH, value='//*[@id="submenu_File"]/button').click()
    time.sleep(1)    


if __name__ == '__main__':
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # define file name, get desired col and casts into list
    sequences_file = 'sequences.xlsx'
    sequences = pd.read_excel('./sequences.xlsx', usecols='A')
    sequences = sequences.values.reshape(1, -1).ravel().tolist()

    # open ncbi site     
    browser = webdriver.Chrome()
    browser.get('https://www.ncbi.nlm.nih.gov/')
    set_nucleotide()
    for sequence in sequences:
        download_sequence(sequence)
    browser.close()
