import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/riskassessment'
    MISP_URL = os.environ.get('MISP_URL') or 'https://192.168.100.76'
    MISP_KEY = os.environ.get('MISP_KEY') or 'vKw9eWvfCil5HcSt0Q5nsJs0fOpmTCt5modKEsUp'

    MISP_VERIFYCERT = False
 
