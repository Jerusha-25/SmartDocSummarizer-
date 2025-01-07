from flask import Flask, jsonify
import logging

app = Flask(__name__)

@app.route('/')
def home():
    app.logger.info("Home route accessed!")
    return jsonify(message="Hello, World!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)



