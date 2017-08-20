Title: Using nmap to find all devices on network listening on a particular port
Date: 2017-08-20 12:00
Category: hint
Slug: hints/nmap_ip_scan
Author: Phil Elson


Finding all IPs listening on a particular port using nmap:

```
nmap -p 80 --open -sV 192.168.1.0/24
```

<!-- PELICAN_END_SUMMARY -->

Refs:
 * http://thoughtsbyclayg.blogspot.co.uk/2008/06/use-nmap-to-scan-for-ssh-servers-on.html
 * https://www.digitalocean.com/community/tutorials/how-to-use-nmap-to-scan-for-open-ports-on-your-vps
 
