from flask import Flask, send_from_directory, request, make_response, Response
from Analysis import analyze_search_string
import os
import json

app = Flask(__name__)


@app.route("/")
def send_page():
    return send_from_directory("./build", path="index.html")


@app.route("/<path:filename>")
def index(filename):
    return send_from_directory("", filename)


@app.route("/data", methods=["POST"])
def get_data():
    search = request.json["search"]
    result = analyze_search_string(search)
    try:
        # result = analyze_search_string(search)
        return Response(json.dumps(result, default=str), mimetype="application/json")

    except Exception as err:
        return (
            f"Unexpected {err=}, {type(err)=}, {os.listdir()} {result}, {type(result)}"
        )

    # return jsonify(result, status=200, mimetype="application/json")


def generateMetrics():
    return "hello world"


@app.route("/metrics")
def metrics():
    response = make_response(generateMetrics(), 200)
    response.mimetype = "text/plain"
    return response


if __name__ == "__main__":
    app.run()
