from flask import Flask, request, jsonify, abort

from os import listdir, makedirs, remove
from os.path import dirname, exists, isfile, join, splitext

import logging
import uuid
import simplejson as json
import pickledb
import time

targets = []
relPath = dirname(__file__)
dataPath = join(relPath, "instance")
reservations = None

def generateTargets():
    if not exists(dataPath):
        makedirs(dataPath)

    for f in listdir(dataPath):
        if isfile(join(dataPath, f)):
            res = json.loads(open(join(dataPath, f), "r").read())
            targets.append(res)
            # TO-DO:
            #
            # At this point, meta-data needs to be reconstructed every time server starts up.
            # Future implementation would serialize meta-data into a cache, and load it on start-up.

app = Flask(__name__)

@app.route("/")
def hello():
    return "Reservation Server is running!"

@app.route("/targets", methods=("GET", "POST"))
def targetsBase():
    if request.method == "GET":
        return jsonify(targets)
        # TO-DO:
        #
        # It is enough to respond with only meta-data.

    if request.method == "POST":
        ip = request.args.get("ip")
        model = request.args.get("model")
        name = request.args.get("name")

        id = str(uuid.uuid4())[0:8]
        filename = id + ".json"
        target = { "id": id, "ip": ip, "model": model, "name": name }
        with open(join(dataPath, filename), "w") as file:
            json.dump(target, file)
        targets.append(target)
        return target
        # TO-DO:
        #
        # Assuming the user wants to upload target file,
        #   it is enough to parse the request body and save as a target file.
        #
        # Future implementation would validate the provided XML,
        #   and reject if invalid.

@app.route("/targets/<id>", methods=("GET", "PUT", "DELETE"))
def targetByID(id):
    if request.method == "GET":
        for target in targets:
            if target["id"] == id:
                return target
        abort(404)
        # TO-DO:
        #
        # Assuming the user wants to download the target file,
        #   it is enough to respond with the target file as text.

    if request.method == "PUT":
        ip = request.args.get("ip")
        for target in targets:
            if target["id"] == id:
                filename = id + ".json"
                with open(join(dataPath, filename), "r") as file:
                    data = file.read()
                data = data.replace(target["ip"], ip)
                with open(join(dataPath, filename), "w") as file:
                    file.write(data)
                target["ip"] = ip
                return target
        abort(404)
        # TO-DO:
        #
        # Expand function to modify other fields.

    if request.method == "DELETE":
        for target in list(targets):
            if target["id"] == id:
                remove(join(dataPath, target["filename"]))
                targets.remove(target)
                return ("Deleted", 200)
        abort(404)
        # TO-DO:
        #
        # It is enough to delete target file and update meta-data.
    
@app.route("/targets/<id>/reservation", methods=("GET", "POST", "DELETE"))
def targetReservationByID(id):
        if request.method == "GET":
            for target in targets:
                if target["id"] == id:
                    reservation = reservations.get(id)
                    if reservation:
                        now = int(time.time())
                        available = int(reservation) < now
                        if available:
                            return ("", 204)
                        else:
                            return reservation
                    else:
                        return ("", 204)
            abort(404)
        
        if request.method == "POST":
            for target in targets:
                if target["id"] == id:
                    reservation = reservations.get(id)
                    now = int(time.time())
                    if reservation:
                        available = int(reservation) < now
                        if available:
                            duration = int(request.args.get("duration"))
                            reservations.set(id, str(now + duration))
                            return (reservations.get(id), 201)
                        else:
                            return reservation
                    else:
                        duration = int(request.args.get("duration"))
                        reservations.set(id, str(now + duration))
                        return (reservations.get(id), 201)
            abort(404)
            
        if request.method == "DELETE":
            for target in targets:
                if target["id"] == id:
                    reservation = reservations.get(id)
                    if reservation:
                        reservations.rem(id)
                        return ("Deleted", 200)
                    else:
                        return ("", 204)
            abort(404)

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    generateTargets()
    reservations = pickledb.load(join(dataPath, "db", "reservations.db"), False)
    #reservations.set("559051d3", str(int(time.time()) + 600))
    #reservations.dump()
    app.run(debug = True)
