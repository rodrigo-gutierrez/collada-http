from flask import Flask, request

import logging
import simplejson as json

robots = [
    {"name": "Bahamut", "id": 1},
    {"name": "Shiva", "id": 2},
    {"name": "Ifrit", "id": 3}]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Collada Server is running!"

@app.route("/robots", methods=("GET", "POST"))
def robotsBase():
    if request.method == "GET":
        return json.dumps(robots)

    if request.method == "POST":
        name = request.args.get("name")
        size = len(robots)
        robot = {"name": name, "id": size + 1}
        robots.append(robot)
        return json.dumps(robot)

@app.route("/robots/<int:id>", methods=("GET", "PUT", "DELETE"))
def robotsWithID(id):
    if request.method == "GET":
        for robot in robots:
            if robot["id"] == id:
                return robot
        return ""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
