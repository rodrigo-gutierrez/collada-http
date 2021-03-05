from flask import Flask, request, jsonify, abort

from os import listdir
from os.path import dirname, isfile, join, splitext

import logging
import simplejson as json

robots = []
relPath = dirname(__file__)
dataPath = join(relPath, "instance")

def generateRobots():
    for f in listdir(dataPath):
        if isfile(join(dataPath, f)):
            res = json.loads(open(join(dataPath, f), "r").read())
            res["id"] = int(splitext(f)[0])
            res["filename"] = f
            robots.append(res)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Collada Server is running!"

@app.route("/robots", methods=("GET", "POST"))
def robotsBase():
    if request.method == "GET":
        return jsonify(robots)

    if request.method == "POST":
        name = request.args.get("name")
        size = len(robots)
        robot = {"name": name, "id": size + 1}
        robots.append(robot)
        return robot

@app.route("/robots/<int:id>", methods=("GET", "PUT", "DELETE"))
def robotsWithID(id):
    if request.method == "GET":
        for robot in robots:
            if robot["id"] == id:
                return robot
        abort(404)

    if request.method == "PUT":
        name = request.args.get("name")
        for robot in robots:
            if robot["id"] == id:
                with open(join(dataPath, robot["filename"]), "r") as file:
                    data = file.read()
                data = data.replace(robot["name"], name)
                with open(join(dataPath, robot["filename"]), "w") as file:
                    file.write(data)
                robot["name"] = name
                return robot
        abort(404)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generateRobots()
    app.run(debug=True)
