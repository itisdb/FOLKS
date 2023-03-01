from ascii.ipfs_pinata.pinataAPI import PinataPy
from ascii.ipfs_pinata.PinataAPIKey import keys


def addImg(imgPath):
    API_KEY = keys()["api_key"]
    SECRET_API_KEY = keys()["api_secret"]
    JWT_TOKEN = keys()["jwt_token"]
    pinata = PinataPy(API_KEY, SECRET_API_KEY)
    return pinata.pin_file_to_ipfs(imgPath)

def removeFile(fileHash):
    API_KEY = keys()["api_key"]
    SECRET_API_KEY = keys()["api_secret"]
    JWT_TOKEN = keys()["jwt_token"]
    pinata = PinataPy(API_KEY, SECRET_API_KEY)
    return pinata.remove_pin_from_ipfs(fileHash)

def addJson(jsonPath):
    API_KEY = keys()["api_key"]
    SECRET_API_KEY = keys()["api_secret"]
    JWT_TOKEN = keys()["jwt_token"]
    pinata = PinataPy(API_KEY, SECRET_API_KEY)
    return pinata.pin_file_to_ipfs(jsonPath)