#! /usr/bin/env python3

import os
import subprocess
import json
import sys
import time

seconds = '60'
prefix = "/var/tmp"
filename = "mongotopy.json"

def reformat(data):
    formatted = []
    data = data['totals']
    for dbcoll in data:
        database, coll = dbcoll.split(".",1)
        for op in ["read", "write"]:
            for field in ["time", "count"]:
                if data[dbcoll][op][field]:
                    formatted.append({"database":database, "coll":coll, "op":op, "field": field, "value":data[dbcoll][op][field]})
    return formatted

def saveMongoData():
    mongocall = subprocess.Popen(['mongotop', '--host=localhost', '--json', '--rowcount=1', seconds], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = mongocall.communicate()
    mongodata = reformat(json.loads(stdout.decode("utf-8")))

    with open(prefix + '/' + 'tmpFile', 'w') as f:
        f.write(json.dumps(mongodata))

    os.rename(prefix + '/' + 'tmpFile', prefix + '/' + filename)

while True:
    try:
        saveMongoData()
    except Exception as e:
        sys.stderr.write(e)
        time.sleep(3*60)

