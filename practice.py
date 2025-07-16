from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, Flask API Harman!'})


@app.route('/mult', methods=['POST'])
def add_numbers():
    data = request.get_json()
    result = data['a'] * data['b']
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True,port = 8080, host = '0.0.0.0')