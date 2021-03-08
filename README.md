# collada-http

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

localhost:5000/colladas  
Methods supported:  
GET  - get meta-data for all collada files, in JSON format  
POST - create new collada file from parameters  

localhost:5000/colladas/<colladaId>  
Methods supported:  
GET    - get meta-data for colladaId specified  
PUT	   - update collada file with colladaId specified via query parameters  
DELETE - remove collada file with colladaId specified  
