#!/bin/bash
# created by YongCao @ 2016-4-9
#
# this script used to automatically backup sql
# datebase everyday.
#

MAX_FILES_NUM=93

filename="/home/ubuntu/sql_auto_backup/"`date +%F_%T`".sql"

mysqldump -u root iShare_server > $filename &>/dev/null

# delete recodes created three month ago
file_num=`ls /home/ubuntu/sql_auto_backup | wc -l`
if [[ $file_num -gt $MAX_FILES_NUM ]]; then
    need_delete_num=`expr $file_num - $MAX_FILES_NUM`
    rm -f $(ls -t /home/ubuntu/sql_auto_backup | tail -$need_delete_num)
fi
