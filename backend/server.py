import sys

from flask import Flask
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)


def error_handler(err):
    ''' Error handler for exceptions '''
    pass


if __name__ == "__main__":
    APP.run(port=int(sys.argv[1]) if len(sys.argv) == 2 else 3000)