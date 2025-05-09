# Code for ETL operations on Country-GDP data

# Importing the required libraries
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
import requests

log_file = "code_log.txt"
output_path = "Largest_banks_data.csv"
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

table_attributes_url = ["Name", "MC_USD_Billion"]
table_attributes_final = ["Name", "MC_USD_Billion", "MC_GBP_Billion", "MC_EUR_Billion", "MC_INR_Billion"]
db_name = "Banks.db"
table_name = "Largest_banks"
csv_path = "exchange_rate.csv"

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + ":" + message + "\n")

def extract(url, table_attributes_url):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    df = pd.DataFrame(columns=table_attributes_url)
    html_data = requests.get(url).text
    data = BeautifulSoup(html_data, "html.parser")
    tables = data.find_all("tbody")
    rows = tables[0].find_all("tr")
    for row in rows:
        col = row.find_all("td")
        if len(col) != 0 :
            try:
                Name = col[1].text.strip().replace('\n', '')
                MC_USD_Billion= float(col[2].text.strip().replace('\n', ''))
                dic_data = {"Name" : Name, "MC_USD_Billion" : MC_USD_Billion}
                df1 = pd.DataFrame(dic_data, index=[0])
                df = pd.concat([df, df1], ignore_index=True)
            except Exception:
                continue
    return df

log_progress("Preliminaries complete. Initiating ETL process.")
df = extract(url, table_attributes_url)

log_progress("Data extraction complete. Initiating Transformation process.")


def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    df_exchange_rate = pd.read_csv(csv_path)
    dict_df = df_exchange_rate.set_index("Currency").to_dict()["Rate"]
    df['MC_GBP_Billion'] = [np.round(x*dict_df['GBP'],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*dict_df['EUR'],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*dict_df['INR'],2) for x in df['MC_USD_Billion']]
    return df

df = transform(df, csv_path)
log_progress("Data transformation complete. Initiating loading process.")


def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    df.to_csv(output_path)

load_to_csv(df, output_path)
log_progress("Data saved to CSV file.")


sql_connection = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists = "replace", index = False)

load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query')

    

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    quer_output = pd.read_sql(query_statement, sql_connection)
    print(quer_output)

run_query(f"SELECT * FROM {table_name}", sql_connection)
run_query(f"SELECT AVG(MC_GBP_Billion) FROM {table_name}", sql_connection)
run_query(f"SELECT Name from {table_name} LIMIT 5", sql_connection)


log_progress('Process Complete.')
sql_connection.close()

