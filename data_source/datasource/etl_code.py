import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

log_file = "log_file.txt"
target_file = "transformed_data.csv"

#function to extract from csv file
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

#function to extract from JSON file
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process)
    return dataframe

#function to extract from XML file
def extract_from_xml(file_to_process):
    data = []  # Use a list to store extracted rows
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for car in root:
        car_model = car.find("car_model").text
        year_of_manufacture = car.find("year_of_manufacture").text
        price = float(car.find("price").text)  # Convert price to float
        fuel = car.find("fuel").text
        data.append({"car_model": car_model, "year_of_manufacture": year_of_manufacture, "price": price, "fuel": fuel})
    
    return pd.DataFrame(data)  # Create DataFrame only once

#fucntion to extract
def extract():
    extracted_data = pd.DataFrame(columns=["car_model", "year_of_manufacture", "price", "fuel"])

    # Process all CSV files
    for csvfile in glob.glob("*.csv"):
        extracted_data = pd.concat([extracted_data, extract_from_csv(csvfile)], ignore_index=True)

    # Process all JSON files
    for jsonfile in glob.glob("*.json"):
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)

    # Process all XML files
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)

    return extracted_data


#Function for transforming data
def transform(data):
    # Convert price from USD to Euro (1 USD = 0.96 EUR) and round to 2 decimals
    data['price'] = data['price'].apply(lambda x: round(x * 0.96, 2))
    return data


#fucntion to load data
def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

#logging
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 
  
# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
  
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
  
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
  
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
  
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
  
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
  
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
  
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 