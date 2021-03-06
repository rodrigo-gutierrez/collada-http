# collada-http

## Description

Very basic Python HTTP server implementation using Flask.

## Prerequisites

Python 3.5+

## Setup

```sh
pip install -r requirements.txt
```

## Usage

```sh
python server.py
```

The server will start on port 5000.  
Requests can be made to the following endpoints:  

localhost:5000/robots
Methods supported:
GET		- get meta-data for all robots, in JSON format
POST	- create new robot from parameters

localhost:5000/robots/<robotId>
Methods supported:
GET		- get meta-data for robotId specified
PUT		- update robot with robotId specified via query parameters
DELETE	- remove robot with robotId specified
