import os

from flask import Flask, request

from main import save, receive

app = Flask(__name__)


@app.route('/save', methods=['POST'])
def gcp_save():
    return save(request)


@app.route('/receive', methods=['POST'])
def gcp_receive():
    return receive(request)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))
