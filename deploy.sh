#!/bin/sh

# requires SSH agent forwarding
servers="dirac gauss erdos euler"
for server in $servers; do
  echo $server
  ssh root@$server.lichess.ovh "cd /home/mongotopy && git pull origin master && systemctl restart mongotopy"
done
