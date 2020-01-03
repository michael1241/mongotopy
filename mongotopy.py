#! /usr/bin/env python3

import os
import subprocess
import json

seconds = '1'
filename = "mongodataforlukhas"

def reformat(data):
    formatted = []
    data = data['totals']
    for dbcoll in data:
        database, coll = dbcoll.split(".",1)
        for op in ["read", "write"]:
            for field in ["time", "count"]:
                formatted.append({"database":database, "coll":coll, "op":op, "field": field, "value":data[dbcoll][op][field]})
    return formatted

def saveMongoData():
    mongocall = subprocess.Popen(['mongotop', '--json', '--rowcount=1', seconds], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = mongocall.communicate()

    mongodata = reformat(json.loads(stdout.decode("utf-8")))

    with open('tmpFile', 'w') as f:
        f.write(str(mongodata))

    os.rename('tmpFile', filename)

while True:
    saveMongoData()
