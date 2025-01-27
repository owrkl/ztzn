import os
from flask import Flask
app = Flask(__name__)
port = int(os.environ.get("PORT",10000))

@app.route('/')
def hello_world():
    return 'This is ZThon'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
