#!/bin/bash
if [ $# -lt 1 ] 
then
    echo "Dump django project database in a file"
    echo "USAGE : $0 path_to_django"
    exit 1
fi

if [ ! -d $1 ]
then
    echo "Error, cannot find folder $1"
    exit 2
fi

if [ ! -f $1/manage.py ]
then
    echo "Error, this folder is not a django project"
    exit 3
fi

BACKUP_FILENAME=$(date +"backup_%Y_%m_%d_%k_%M" )
cd $1
python manage.py dumpdata inventory auth --indent 4 > ${BACKUP_FILENAME}.json 
tar czf ${BACKUP_FILENAME}.tgz ${BACKUP_FILENAME}.json && rm ${BACKUP_FILENAME}.json
