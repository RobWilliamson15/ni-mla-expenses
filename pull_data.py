import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "https://www.niassembly.gov.uk/your-mlas/members-salaries-and-expenses/members-expenditure-2022---2023-april-2022---march-2023/"

# Fetch the page content
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse the HTML
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the data
table = soup.find("table")

# Extract table headers
headers = [header.text for header in table.find_all("th")]

# Extract table rows
rows = []
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    rows.append([cell.text.strip() for cell in cells])

# Create a DataFrame
df = pd.DataFrame(rows, columns=headers)

# Save DataFrame to CSV
df.to_csv("members_expenditure_2022_2023.csv", index=False)

print("Data has been saved to members_expenditure_2022_2023.csv")

