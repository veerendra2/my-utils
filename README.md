# Some usefull python scripts and snippets

## 1. [changer init script](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/changer)
   It is an `init` script which changes the MAC address of `wlan0` interface. As I said `init` script, it will run at the time of system boot and changes the MAC address i.e there is will be new MAC whenever system boots. With simple commands we can restore/change the MAC whenever we want. Read [my blog post](https://networkhop.wordpress.com/2017/03/26/mac-address-scrambling-in-linux/) for more info and how to install
```
  service changer restore (Restores original MAC)
  service changer new (Asigns new MAC)
  service changer show (Shows current MAC)
```

## 2. [connections_viewer.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/connections_viewer.py)
`netstat`/`ss` like tool, which displays the current connections statuses with `pid`. It reads info from `/proc/net/tcp`
    
## 3. [logger.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/logger.py) 
A simple "logger" snippet. Copy the code and call function `log_it` to log the events in log file

## 4. [port_scanner.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/port_scanner.py)
A simple "localhost" open port scanner script with `socket`

## 5. [netTools.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/netTools.py)
A simple "Domain Tools" like script which retrives location of the specified host and show where you are with "public ip". Below you can see the usage, without arguments `python netTools.py` displays information of your ISP with your public IP and your location 
   Uses free HTTP APIs 
   * http://ip-api.com/json/ (Gets Host info)
   * http://whatismyip.akamai.com/ (Gets public IP)
   
```
   root@ultron:/# python netTools.py -h
   usage: netTools.py [-h] [-m] [-H HOST] [-v]

   Net Tools

   optional arguments:
      -h, --help  show this help message and exit
      -m          shows public IP
      -H HOST     shows domain info of the host
      -v          show program's version number and exit
   
root@ultron:/opt/scripts# python netTools.py -m
YOUR PUBLIC IP ADDRESS: 45.XX.XX.XX

root@ultron:/opt/scripts# python netTools.py 
+----------------------------------------------------------+
| Host            CtrlS XXXXXXXXXXX                        |
| Your Public IP  45.XXX.XX.XXX                            |
| ISP             E XXX Entertainment Pvt                  |
| AS              AS182XX CtrlS XXXXXXXXXXX Ltd.           |
| City            GuXXXX                                   |
| Region          AnXXXX XrXXXXX                           |
| Country         India                                    |
| Latitude        XX.3                                     |
| Longitude       XX.45                                    |
| Time Zone       Asia/Kolkata                             |
| ZIP             XXX002                                   |
+----------------------------------------------------------+

   ```
## 5. [dsncrypt-auto.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/dsncrypt-auto.py)
   Uses `dnscrypt-proxy` tool to setup DSNCrypt in machine.
   
   * #### What is [DNSCrypt](https://dnscrypt.org/) and Why?

     *DNSCrypt is a protocol that authenticates communications between a DNS client and a DNS resolver. It prevents DNS spoofing.      It uses cryptographic signatures to verify that responses originate from the chosen DNS resolver and haven't been tampered with.*

     *It is an open specification, with free and opensource reference implementations, and it is not affiliated with any company    nor organization.*

    * Shows available  servers by downloading .csv file from offical repo. No need to specify manually
    * Daemonize the process
   
   DNSCrypt run on localhost(127.0.0.1) port 53. After running the script(if everything is ok) please change the DNS IP in network settings like below
   
   ![Network Setting](https://ibin.co/3NSgLh4fO5Yg.jpg)
   
