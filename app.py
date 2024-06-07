from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Define a function to clean and convert currency values to floats

def clean_currency(value):
    if isinstance(value, str):
        return float(value.replace('£', '').replace(',',''))
    return float(value)

# Load and preprocess the data
df = pd.read_csv('expenditure_data/members-expenditure-2023---2024-april-2023---february-2024.csv')

# Remove the total row if it exists
df = df[df['Name'] != 'Total']

# Clean the currency columns
expense_columns = ['Constituency Office Expenses(View constituency office expenses breakdown)', 
                   'Other Expenses(View other expenses breakdown)', 
                   'Allowances(View allowances breakdown)', 
                   'Staff cost(View staff costs breakdown)', 
                   'Total Expenditure']

for col in expense_columns:
    df[col] = df[col].apply(clean_currency)

# Find the largest and least contributors
results = {}
for col in expense_columns:
    max_row = df.loc[df[col].idxmax()]
    min_row = df.loc[df[col].idxmin()]
    results[col] = {
        'max': max_row['Name'],
        'max_value': max_row[col],
        'min': min_row['Name'],
        'min_value': min_row[col]
    }

@app.route('/')
def index():
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
