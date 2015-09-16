#!/bin/sh

rm -r ../media
unzip -o $1 media/* -d ../
unzip $1 dump.json
python3 manage.py loaddata dump.json
rm dump.json