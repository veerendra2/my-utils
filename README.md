# Some usefull python scripts and snippets
1.  [changer init script](https://github.com/veerendra2/python-scripts/blob/master/scripts/changer)

    It is an `init` script which changes the MAC address of `wlan0` interface. As I said `init` script, it will run at the time of        system boot and changes the MAC address i.e there is will be new MAC whenever system boots. With simple commands we can restore/change the MAC whenever we want. Read [my blog post](https://networkhop.wordpress.com/2017/03/26/mac-address-scrambling-in-linux/) for more info and how to install
```
  service changer restore (Restores original MAC)
  service changer new (Asigns new MAC)
  service changer show (Shows current MAC)
```

2. [connections_viewer.py script](https://github.com/veerendra2/python-scripts/blob/master/scripts/connections_viewer.py)

    `netstat`/`ss` like tool, which displays the current connections statuses with `pid`. It reads info from `/proc/net/tcp`
    
3. [logger.py script](https://github.com/veerendra2/python-scripts/blob/master/scripts/logger.py)
    
    A simple "logger" snippet. Copy the code and call function `log_it` to log the events in log file

4. [port_scanner.py script](https://github.com/veerendra2/python-scripts/blob/master/scripts/port_scanner.py)

    A simple "localhost" open port scanner script with `socket`

5. [netTools.py script](https://github.com/veerendra2/python-scripts/blob/master/scripts/netTools.py)

   A simple "Domain Tools" like script which retrives location of the specified host and show where you are with "public ip". Below you can see the usage, without arguments `python netTools.py` displays information of your ISP with your public IP and your location
   
   Uses free HTTP APIs 
   * https://ipv4.ipleak.net/json/ (Gets Host info)
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
   
   root@ultron:/# python netTools.py (I have used VPN)
   +--------------------------------------------------------+
   | Your Public IP  138.197.X.X                            |
   | City            Toronto                                |
   | Region          Ontario                                |
   | Country         Canada                                 |
   | Continent       North America                          |
   | ISP Name        Digital Ocean                          |
   | Org. Name       Digital Ocean                          |
   | AS Number       AS394362                               |
   | Net Speed       Corporate                              |
   | User Type       hosting                                |
   | Latitude        43.6555                                |
   | Longitude       -79.3626                               |
   | Time Zone       America/Toronto                        |
   +--------------------------------------------------------+

   ```
