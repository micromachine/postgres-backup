#!/usr/bin/env python
import os
import time

username = 'postgres'
defaultdb = 'postgres'
sysdb = 'system'
port = '5432'
backupdir='/var/backup/pgdb/'
date = time.strftime('%Y-%m-%d-%H-%M-%S')
get_db_names="psql -U%s -d%s -p%s --tuples-only -c '\l' | awk -F\| '{ print $1 }'|  sed -e '/^\ *$/d' | grep -E -v '(template0|template1^$)'" % (username, defaultdb, port)
def log(string):
    print time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + ": " + str(string)
os.popen("pg_dumpall -p%s -g|gzip -9 -c >  %s/system.%s.gz" % (port, backupdir, date))
for base in os.popen(get_db_names).readlines():
        log("dump rozpoczety dla bazy:%s" % base)
        base = base.strip()
        fulldir = backupdir + base
        if not os.path.exists(fulldir):
                os.mkdir(fulldir)
        filename = "%s/%s-%s.sql" % (fulldir, base, date)
        os.popen("nice -n 19 pg_dump -C -F c -U%s -p%s %s | gzip -9 -c > %s.gz" % (username, port, base, filename))
        log("dump %s zakonczony" % base)
log("Backup zakonczony.")

