#!/bin/sh
# Example: ./restore_backup.sh ../backup/18_09_2015.zip
rm -rf ../media
unzip -o $1 media/* -d ../
unzip $1 dump.json
python3 manage.py loaddata dump.json
rm dump.json