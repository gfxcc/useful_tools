#!/bin/bash
# created by YongCao @ 2016-4-9
#
# this script used to automatically backup sql
# datebase everyday.
#

MAX_FILES_NUM=93

filename="/home/ubuntu/sql_auto_backup/$(date +%F_%T).sql"

mysqldump -u root iShare_server > $filename

# delete recodes created three month ago
file_num=`ls /home/ubuntu/sql_auto_backup | wc -l`
while [[ $file_num -gt $MAX_FILES_NUM ]]; do
    rm -f /home/ubuntu/sql_auto_backup/$(ls -t /home/ubuntu/sql_auto_backup | tail -1)
    file_num=$((file_num - 1))
done
