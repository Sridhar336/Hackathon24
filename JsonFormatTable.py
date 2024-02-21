import tabula
import json
import pandas as pd
import fitz
import  warnings
# Path to your pdf file
pdf_path = r"MonitoringReportClient.pdf"

from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

 
# Get the number of pages in the PDF
num_pages = fitz.open(pdf_path)
 
# Create a list to store the table data
table_data = []
 
# Declare variable for counting of table
l = 1
 
# Ittrate tables from each page of pdf file with required format
for i in range(1, num_pages.page_count+1):
   
    # Specify the page you want to extract tables from
    page_number = i
   
    # Extract tables from the specific page
    tables = tabula.read_pdf(pdf_path, pages=i)
 
    # Filter out tables with zero rows
    tables = [table for table in tables if len(table) > 0]
   
    # Replace "Unnamed" in column names with a space
    tables = [table.rename(columns=lambda x: x.replace('Unnamed', '')) for table in tables]
   
    # Fill "NaN" in column data with a space
    tables = [table.fillna('') for table in tables]
   
    # Add the data for each table to the list
    for j, table in enumerate(tables):
        table_data.append({
            "tableName": f"Table {l}",
            "tableIndex": l,
            "pageNo.": page_number,
            "totalRows": len(table),
            "totalColumns": len(table.columns),
            "tableData": table.to_dict(orient='records')
           
        })
       
        l = l+1
       
# Convert the table data to JSON
table_data_json = json.dumps(table_data)
 
# Print the JSON data
print(table_data_json)