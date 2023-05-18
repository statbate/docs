<p align="center"> 
<img src="https://raw.githubusercontent.com/poiuty/statbate/master/www/img/github.jpg">
</p>

Statbate is running on the <a href="https://www.hetzner.com/dedicated-rootserver/ax102">AX102 Hetzner server</a>.<br/>
CPU 7950X3D, 128 GB DDR5 ECC, 2 x1.92 TB NVMe (KIOXIA KCD81RUG1T92), 1 GBit/s network.

I am using ext4 file system. <a href="https://clickhouse.com/docs/ru/operations/tips#file-system">Clickhouse</a> and <a href="https://mariadb.com/kb/en/filesystem-optimizations/">Mariadb</a> work better with `noatime`
```
# nano /etc/fstab
UUID=xxx / ext4 defaults,noatime 0 0

# after that you can do a remount or reboot
# mount -o remount,noatime /

# check changes
# mount
/dev/md1 on / type ext4 (rw,noatime)
```

CPU Scaling Governor. Always use the performance scaling governor.
```
# let's check
# cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
schedutil

# now let's change
# apt-get install cpufrequtils
# nano /etc/default/cpufrequtils
ENABLE="true"
GOVERNOR="performance"
MAX_SPEED="0"
MIN_SPEED="0"

# systemctl restart cpufrequtils.service
# and check again
# cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
performance
```

After installing OS Debian 11, I need to update and install packages and change config files.

```
apt-get update
apt-get upgrade
apt-get install htop bwm-ng strace lsof iotop git build-essential screen
```

1. <a href="https://github.com/poiuty/statbate/blob/master/install/mariadb.md">Mariadb</a><br/>
2. <a href="https://github.com/poiuty/statbate/blob/master/install/clickhouse.md">ClickHouse</a><br/>
3. <a href="https://github.com/poiuty/statbate/blob/master/install/nginx.md">Nginx</a><br/>
4. <a href="https://github.com/poiuty/statbate/blob/master/install/php.md">PHP</a><br/>
5. <a href="https://github.com/poiuty/statbate/blob/master/install/python.md">Python</a><br/>
6. <a href="https://github.com/poiuty/statbate/blob/master/install/redis.md">Redis</a><br/>
7. <a href="https://github.com/poiuty/statbate/blob/master/install/app.md">App</a>
8. Add <a href="https://github.com/poiuty/statbate/blob/master/install/conf/cron">cron</a>

