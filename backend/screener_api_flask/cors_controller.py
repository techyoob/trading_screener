


from flask import jsonify, make_response, request
from dotenv import load_dotenv
load_dotenv()



class CorsController:


    def __init__(self):
        self.response = make_response()


    def preflight(self):
        self.response.headers.add("Access-Control-Allow-Origin", "*")
        self.response.headers.add('Access-Control-Allow-Headers', "*")
        self.response.headers.add('Access-Control-Allow-Methods', "*")
        return self.response


    def response_control(self, reply):
        response = jsonify(reply)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response