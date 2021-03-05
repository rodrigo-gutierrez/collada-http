from flask import Flask, request, jsonify, abort

from os import listdir
from os.path import dirname, isfile, join, splitext

import logging
import simplejson as json

robots = []

def generateRobots():
    relPath = dirname(__file__)
    mypath = join(relPath, "instance")
    for f in listdir(mypath):
        if isfile(join(mypath, f)):
            res = json.loads(open(join(mypath, f), "r").read())
            res["id"] = int(splitext(f)[0])
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generateRobots()
    app.run(debug=True)
