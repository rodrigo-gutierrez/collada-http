from flask import Flask, request, jsonify, abort

from os import listdir, makedirs, remove
from os.path import dirname, exists, isfile, join, splitext

import logging
import uuid
import simplejson as json

colladas = []
relPath = dirname(__file__)
dataPath = join(relPath, "instance")

def generateColladas():
    if not exists(dataPath):
        makedirs(dataPath)

    for f in listdir(dataPath):
        if isfile(join(dataPath, f)):
            res = json.loads(open(join(dataPath, f), "r").read())
            res["id"] = splitext(f)[0]
            res["filename"] = f
            colladas.append(res)
            # TO-DO:
            #
            # OpenRAVE needs to be invoked to parse all Collada files in the data directory.
            # Using openravepy Environment and  classes, extract meta-data from each file to generate
            #   'colladas' object array.
            #
            # At this point, meta-data needs to be reconstructed every time server starts up.
            # Future implementation would serialize meta-data into a cache, and load it on start-up.

app = Flask(__name__)

@app.route("/")
def hello():
    return "Collada Server is running!"

@app.route("/colladas", methods=("GET", "POST"))
def colladasBase():
    if request.method == "GET":
        return jsonify(colladas)
        # TO-DO:
        #
        # It is enough to respond with only meta-data.
        # No OpenRAVE operations required.

    if request.method == "POST":
        name = request.args.get("name")
        id = str(uuid.uuid4())[0:8]
        collada = {"name": name, "id": id, "filename": id + ".dae"}
        with open(join(dataPath, collada["filename"]), "w") as file:
            file.write("{ \"name\": \"" + name + "\" }")
        colladas.append(collada)
        return collada
        # TO-DO:
        #
        # Assuming the user wants to upload a Collada file,
        #   it is enough to parse the request body and save as a Collada file.
        # No OpenRAVE operations required.
        #
        # Future implementation would validate the provided XML with OpenRave,
        #   and reject if invalid.

@app.route("/colladas/<id>", methods=("GET", "PUT", "DELETE"))
def colladaWithID(id):
    if request.method == "GET":
        for collada in colladas:
            if collada["id"] == id:
                return collada
        abort(404)
        # TO-DO:
        #
        # Assuming the user wants to download the Collada file,
        #   it is enough to respond with the Collada file as text.
        # No OpenRAVE operations required.

    if request.method == "PUT":
        name = request.args.get("name")
        for collada in colladas:
            if collada["id"] == id:
                with open(join(dataPath, collada["filename"]), "r") as file:
                    data = file.read()
                data = data.replace(collada["name"], name)
                with open(join(dataPath, collada["filename"]), "w") as file:
                    file.write(data)
                collada["name"] = name
                return collada
        abort(404)
        # TO-DO:
        #
        # import openravepy
        # env = openravepy.Environment()
        # searching meta-data same as above, set pathToColladaFile to collada["filename"] of correct file
        # env.Load(pathToColladaFile)
        # modify loaded object according to query parameters provided
        # env.Save(pathToColladaFile)

    if request.method == "DELETE":
        for collada in list(colladas):
            if collada["id"] == id:
                remove(join(dataPath, collada["filename"]))
                colladas.remove(collada)
                return ("", 204)
        abort(404)
        # TO-DO:
        #
        # It is enough to delete Collada file and update meta-data.
        # No OpenRAVE operations required.

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generateColladas()
    app.run(debug=True)
