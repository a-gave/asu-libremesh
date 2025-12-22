#!/bin/bash

tail -F /var/log/squid/access.log 2>/dev/null &
tail -F /var/log/squid/error.log 2>/dev/null &
tail -F /var/log/squid/store.log 2>/dev/null &
tail -F /var/log/squid/cache.log 2>/dev/null &
# create missing cache directories and exit

CFG=/etc/squid/squid.conf

if ! test -f "$CFG"; then
    echo "Config file /etc/squid/squid.conf does not exist, using defaults."
    chown -R 31:31 /var/spool/squid
    if ! test -f /var/spool/squid/00; then
       echo "Creating cache directory structure"
        squid -z
        sleep 10
    fi
    squid -N -f /defaults/squid/squid.conf
else
    chown -R 31:31 /var/spool/squid
    if ! test -f /var/spool/squid/00; then
       echo "Creating cache directory structure"
        squid -z
        sleep 10
    fi
    squid -N -f /etc/squid/squid.conf
fi

# /usr/sbin/squid -Nz
/usr/sbin/squid "$@"
