# iptables_block

Service program to check recurrently the journalctl attempting connections to our server and blocking ip with ipset and iptables in linux.

## Neccesary libraries and programs
- Python 3
- Libraries: os, time
- iptables
- iptables-persistent
- ipset
- screen

## Start configuration:

* Install iptables and ipset
```
  yum install ipset iptables iptables-persistent screen
or
  apt-get install ipset iptables iptables-persistent screen
```
* Create a blacklist
```
  ipset create blacklist hash:ip hashsize 4096
```
* Add rule to iptables
```
  iptables -I INPUT -m set --match-set blacklist src -j DROP
  iptables -I FORWARD -m set --match-set blacklist src -j DROP
```
* Activate rules on reboot

To save and restore iptables rules, use the package iptables-persistent. As the name implies, this makes the iptables rules persistent across reboots.

* Create file (/etc/systemd/system/save-ipset-rules.service)
```
  [Unit]
  Description=ipset persistent rule service
  Before=netfilter-persistent.service
  ConditionFileNotEmpty=/etc/iptables/ipset

  [Service]
  Type=oneshot
  RemainAfterExit=yes
  ExecStart=/sbin/ipset -exist -file /etc/iptables/ipset restore
  ExecStop=/sbin/ipset -file /etc/iptables/ipset save

  [Install]
  WantedBy=multi-user.target
```
And create iptables save file the first time with:
```
  /sbin/ipset -file /etc/iptables/ipset save
```

* Python3
```
  import os
  import sys
```

* Screen
If you want runs the service

## Running program

You can script the service-program to start with your crontab, making a service in systemctl or launching manually.
To run the service in background you can made an .sh whit:
```
  screen -S Block_ip_service -d -m python3 iptables_block.py
```

<a href="https://www.buymeacoffee.com/BTRpGQmXq" target="_blank"><img src="https://i1.wp.com/www.buymeacoffee.com/assets/img/custom_images/orange_img.png?w=2560&ssl=1" alt="Buy Me A Coffee" style="height: 5px !important;width: 74px !important;" ></a>
