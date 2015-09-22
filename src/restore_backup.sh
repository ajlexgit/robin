#!/bin/sh
# Example: ./restore_backup.sh ../backup/18_09_2015.zip

archive=$1
directory=$2

if [[ -z "$directory" ]]
then
    directory=..
fi

rm -rf $directory/media
unzip -o $archive media/* -d $directory/
unzip $archive dump.json
python3 manage.py loaddata dump.json
rm dump.json