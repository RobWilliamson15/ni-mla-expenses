import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Base URL of the website
base_url = "https://www.niassembly.gov.uk"

# URL of the main page with links to different expenditure pages
main_url = f"{base_url}/your-mlas/members-salaries-and-expenses/"

# Fetch the main page content
response = requests.get(main_url)
response.raise_for_status()

# Parse the HTML of the main page
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links to expenditure pages
links = soup.find_all("a", href=True)

# Filter the relevant expenditure links
expenditure_links = [link['href'] for link in links if 'members-expenditure' in link['href']]

# Function to scrape data from a given URL and save to CSV
def scrape_and_save(url, filename):
    full_url = f"{base_url}{url}"
    response = requests.get(full_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    
    headers = [header.text for header in table.find_all("th")]
    rows = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        rows.append([cell.text.strip() for cell in cells])
    
    df = pd.DataFrame(rows, columns=headers)
    df.to_csv(filename, index=False)
    print(f"Data has been saved to {filename}")

# Create a directory to store the CSV files
os.makedirs("expenditure_data", exist_ok=True)

# Scrape each expenditure page and save data to CSV
for link in expenditure_links:
    filename = os.path.join("expenditure_data", link.split('/')[-2] + ".csv")
    scrape_and_save(link, filename)

