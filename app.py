from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge= request.args.get('hub.challenge')
        if token == 'secret':
            return str(challenge)
        return '400'
