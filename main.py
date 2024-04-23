import csv
import pdfplumber

# Define the write_to_csv function
def write_to_csv(file_name, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def extract_data_above_table(pdf_file):
    above_table_data = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if "Number :" in text:
                above_table_data += text.split("Number :")[0].strip() + "\n"  # Extract text above the table
            elif above_table_data:  # Stop extraction if above_table_data is not empty
                break
    return above_table_data

def extract_table_from_pdf(pdf_file):
    table_data = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                table_data.extend(table)
            elif table_data:  # Stop extraction if table_data is not empty
                break
    return table_data

def transpose_table(table_data):
    transposed_table = list(map(list, zip(*table_data)))
    return transposed_table

def table_to_key_value_pairs(table):
    if not table or not table[0]:  # Check if the table is empty or if the first row is None
        return {}

    key_value_pairs = {}
    headings = table[0]  # Extract the first row as headings
    if not all(headings):  # Check if all elements in headings are None
        return {}

    for row in table[1:]:
        if row is not None and row[0] is not None:  
            for index, value in enumerate(row):
                if index < len(headings):
                    key = headings[index].strip()
                    value = value.strip() if value is not None else ""
                    key_value_pairs[key] = value
    return key_value_pairs


def main(pdf_file):
    # Extract data above the table
    above_table_data = extract_data_above_table(pdf_file)
    
    # Extract table data
    table = extract_table_from_pdf(pdf_file)
    
    # Transpose the table data
    transposed_table = transpose_table(table)
    
    # Print extracted table data
    print("Extracted Table Data:")
    for row in transposed_table:
        print(row)
    
    # Convert table data to key-value pairs
    table_data_key_value = table_to_key_value_pairs(table)
    
    # Print the key-value pairs
    print("Key-Value Pairs:")
    for key, value in table_data_key_value.items():
        print(f"{key}: {value}")

    # Write transposed table data to a CSV file
    write_to_csv('table_data.csv', transposed_table)

if __name__ == "__main__":
    input_pdf_file = 'input.pdf'  # Change this to your input file name
    main(input_pdf_file)