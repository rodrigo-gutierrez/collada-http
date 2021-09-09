# target-http

## Description

Very basic Python HTTP server implementation using Flask.

## Prerequisites

Python 3.5+

## Setup

It is strongly recommended to use a Python virtual environment. After setting it up:

```sh
pip3 install -r requirements.txt
```

## Usage

```sh
python3 server.py
```

The server will start on port 5000.  
Requests can be made to the following endpoints:  

localhost:5000/targets  
Methods supported:  
GET  - get meta-data for all target files, in JSON format  
POST - create new target file from parameters  

localhost:5000/targets/<targetId>  
Methods supported:  
GET    - get meta-data for targetId specified  
PUT	   - update target file with targetId specified via query parameters  
DELETE - remove target file with targetId specified  

localhost:5000/targets/<targetId>/reservation
Methods supported:  
GET    - TO-DO
POST   - TO-DO
DELETE - TO-DO 
