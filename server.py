from flask import Flask, request, jsonify, abort

from os import listdir, makedirs, remove
from os.path import dirname, exists, isfile, join, splitext

import logging
import uuid
import simplejson as json

robots = []
relPath = dirname(__file__)
dataPath = join(relPath, "instance")

def generateRobots():
    if not exists(dataPath):
        makedirs(dataPath)

    for f in listdir(dataPath):
        if isfile(join(dataPath, f)):
            res = json.loads(open(join(dataPath, f), "r").read())
            res["id"] = splitext(f)[0]
            res["filename"] = f
            robots.append(res)
            # TO-DO:
            #
            # OpenRAVE needs to be invoked to parse all Collada files in the data directory.
            # Using openravepy Environment and  classes, extract meta-data from each file to generate
            #   'robots' object array.
            #
            # At this point, meta-data needs to be reconstructed every time server starts up.
            # Future implementation would serialize meta-data into a cache, and load it on start-up.

app = Flask(__name__)

@app.route("/")
def hello():
    return "Collada Server is running!"

@app.route("/robots", methods=("GET", "POST"))
def robotsBase():
    if request.method == "GET":
        return jsonify(robots)
        # It is enough to respond with only meta-data. No OpenRAVE operations required.

    if request.method == "POST":
        name = request.args.get("name")
        id = str(uuid.uuid4())[0:8]
        robot = {"name": name, "id": id, "filename": id + ".robot"}
        with open(join(dataPath, robot["filename"]), "w") as file:
            file.write("{ \"name\": \"" + name + "\" }")
        robots.append(robot)
        return robot
        # TO-DO:
        #
        #

@app.route("/robots/<id>", methods=("GET", "PUT", "DELETE"))
def robotsWithID(id):
    if request.method == "GET":
        for robot in robots:
            if robot["id"] == id:
                return robot
        abort(404)
        # TO-DO:
        #
        #

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
        # TO-DO:
        #
        #

    if request.method == "DELETE":
        for robot in list(robots):
            if robot["id"] == id:
                remove(join(dataPath, robot["filename"]))
                robots.remove(robot)
                return ("", 204)
        abort(404)
        # It is enough to simply delete Collada file and update meta-data. No OpenRAVE operations required.

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generateRobots()
    app.run(debug=True)
