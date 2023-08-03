import requests
from tabulate import tabulate
import time
from datetime import datetime
import json
import os

# Function For Check The Subdomain Status Is Up Or Down
def check_subdomain_status(domain,subDomains):

    result = []
    for subDomain in subDomains:
        try:
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            response = requests.get(domain,timeout=30)

            status_code = response.status_code
            if status_code == 200:
               status = "Up"
            else:
               status = "Down"
        except requests.RequestException:
            status_code = 500
            status ="Down"
        
        result.append((domain,subDomain,status_code,status,current_time))
    return result

# Function for validate the Configration File 
def file_validation(file_path):
    message=""
    try:
        if not os.path.exists(file_path):
            message ="Failed File not found"
            return message, False

        _, file_extension = os.path.splitext(file_path)

        if not file_extension:
            message ="Failed Invalid file format. Only .json files are allowed"
            return message,False
    except Exception as e:
        message = f"Error while checking the configuration file: {str(e)}"
        return message,False
    
    return file_path,True

# Function to Read the Configration File
def read_config_file(file_path):
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
    except Exception as e:
       return str(e),False
    return config,True

# Main Method
if __name__ == "__main__":

    file_path = "configration.json"
    config_file_path,file_result = file_validation(file_path)

    if file_result:

        config_data,config_result = read_config_file(config_file_path)

        if config_result:

            headers = ["Domain", "SubDomain", "Status Code", "Status", "Status checked at"]
            sleep_time = config_data["Configuration"]["SleepTime"]
            try:
                while True:
                    results= []
                    for domain_data in config_data["Configuration"]["Domains"]:
                        domain = domain_data["Domain"]
                        subDomains = domain_data["SubDomains"]
                        result = check_subdomain_status(domain,subDomains)
                        results.extend(result)
                        
                    print(tabulate(results, headers=headers, tablefmt="grid"))

                    time.sleep(sleep_time)
            except KeyboardInterrupt:
                print("Check subdomain status program stopped.")
        else:
            print(config_data)
            print("Pleas fix the configration file")
    else:
        print(config_file_path)