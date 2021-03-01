from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from app.pvmodel.main import get_params

app = Flask(__name__)
CORS(app, resources=r'/*', headers='Content-Type')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/param_ext", methods=['POST'])
def param_ext():
    data = request.form.to_dict()
    print(data)
    result = get_params(data)
    print(result)
    return result


if __name__ == '__main__':
    app.run()
