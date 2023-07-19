from flask import Flask, jsonify,request
import configparser
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['configuration']
config_collection = db['configuration_details']

# API STATUS
class ApiStatus:
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    
# Commmn Respone For API's
# With two function common api response and common response api with data
class CommonResponse:
    def __init__(self, message, status_code, is_success=True,data=None):
        self.message = message
        self.status_code = status_code
        self.is_success = is_success
        self.data = data

    def common_api_response(self):
        return {'message': self.message, 'status_code': self.status_code, 'is_success': self.is_success}
    def common_api_response_with_data(self):
        return {'message': self.message, 'status_code': self.status_code, 'is_success': self.is_success,'data': self.data}

# parse config file using ConfigParser
def parse_configuration_file(file):
    config = configparser.ConfigParser()
    try:
        config.read_string(file.stream.read().decode('utf-8'))
    except Exception as e:
        message = f"Error while parseing configuration file: {str(e)}"
        response = CommonResponse(message, ApiStatus.BAD_REQUEST, False)
        return jsonify(response.common_api_response()),True
    config_dict = {section: dict(config[section]) for section in config.sections()}
    return config_dict, False

# extract config file data
def extract_configuration(file_data):
    if not file_data:
        return None
    try:
        result = {}
        for section, section_data in file_data.items():
            result[section] = {}
            for key, value in section_data.items():
                result[section][key] = value
    except Exception as e:
        message = f"Error while extracting data from configuration file: {str(e)}"
        response = CommonResponse(message, ApiStatus.BAD_REQUEST, False)
        return jsonify(response.common_api_response()),True
    return result,False

# saving json file into mongodb
def save_in_database(config_json_data):

    try:
        config_collection.insert_one(config_json_data)
    except Exception as e:
        message = f"Error while saving in database data : {str(e)}"
        response = CommonResponse(message, ApiStatus.BAD_REQUEST, False)
        return jsonify(response.common_api_response()),True
    
    config_json_data.pop('_id', None)
    return None, False

app = Flask(__name__)

# API for upload config file POST Method
@app.route('/api/upload_configration_file',methods=['POST'])
def file_upload():
    uploaded_file = request.files
    try:
        if 'file' not in uploaded_file:
            response = CommonResponse("No file in the request", ApiStatus.BAD_REQUEST, False)
            return jsonify(response.common_api_response()), ApiStatus.BAD_REQUEST

        file = uploaded_file['file']

        if file.filename == '':
            response = CommonResponse("No selected file", ApiStatus.BAD_REQUEST, False)
            return jsonify(response.common_api_response()), ApiStatus.BAD_REQUEST
        
        if not file.filename.endswith('.txt'):
            response = CommonResponse("Invalid file format. Only .txt files are allowed.", ApiStatus.BAD_REQUEST, False)
            return jsonify(response.common_api_response()), ApiStatus.BAD_REQUEST
    
        config, parse_error_response = parse_configuration_file(file)
        if parse_error_response:
            return config
        
        config_data,extract_error_response = extract_configuration(config)
        if extract_error_response:
            return config_data
        
        save_data,save_error_response = save_in_database(config_data)
        if save_error_response:
            return save_data

        response = CommonResponse("File uploaded successfully", ApiStatus.OK,data=config_data)
        return jsonify(response.common_api_response_with_data()), ApiStatus.OK
    except Exception as e:
        message = f"Error while uploading file : {str(e)}"
        response = CommonResponse(message, ApiStatus.INTERNAL_SERVER_ERROR, False)
        return jsonify(response.common_api_response()),ApiStatus.INTERNAL_SERVER_ERROR 

# API to Get Uploaded File Data In Json. GET Method
@app.route('/api/configuration', methods=['GET'])
def get_configuration():

    try:

        config_data = list(config_collection.find({}, {'_id': 0}))

        if len(config_data) > 0:
            response = CommonResponse("Data retrieved successfully", ApiStatus.OK,data=config_data)
            return jsonify(response.common_api_response_with_data()), ApiStatus.OK
        else:
            response = CommonResponse("No Data exist", ApiStatus.OK)
            return jsonify(response.common_api_response()), ApiStatus.OK
    except Exception as e:
        message = f"Error while getting config data from database : {str(e)}"
        response = CommonResponse(message, ApiStatus.INTERNAL_SERVER_ERROR, False)
        return jsonify(response.common_api_response()),ApiStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)

