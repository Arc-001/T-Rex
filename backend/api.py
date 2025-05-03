from flask import Flask, jsonify, request

app = Flask(__name__)


api = app.blueprint('api', __name__)


