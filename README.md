# Some usefull python scripts and snippets

#### Repo Website - https://veerendra2.github.io/useless-scripts/

## 1. [changer init script](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/changer)
   It is an `init` script which changes the MAC address of `wlan0` interface. As I said `init` script, it will run at the time of system boot and changes the MAC address i.e there is will be new MAC whenever system boots. With simple commands we can restore/change the MAC whenever we want. Read [my blog post](https://networkhop.wordpress.com/2017/03/26/mac-address-scrambling-in-linux/) for more info and how to install
```
  service changer restore (Restores original MAC)
  service changer new (Asigns new MAC)
  service changer show (Shows current MAC)
```

## 2. [connections_viewer.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/connections_viewer.py)
[`netstat`](http://manpages.ubuntu.com/manpages/trusty/man8/netstat.8.html)/[`ss`](http://manpages.ubuntu.com/manpages/trusty/en/man8/ss.8.html) like tool, which displays the current connections statuses with `pid`. Reads info from `/proc/net/tcp`
   
## 3. [port_scanner.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/port_scanner.py)
A simple "localhost" open port scanner script with `socket`

## 4. [netTools.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/netTools.py)
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
## 5. [dsncrypt.py](https://github.com/veerendra2/useless-scripts/blob/master/scripts/dnscrypt.py)
   Uses `dnscrypt-proxy` tool to setup DSNCrypt in machine. Check installation steps [here](http://www.webupd8.org/2014/08/encrypt-dns-traffic-in-ubuntu-with.html)
   
   * #### What is [DNSCrypt](https://dnscrypt.org/) and Why?

     *DNSCrypt is a protocol that authenticates communications between a DNS client and a DNS resolver. It prevents DNS spoofing.      It uses cryptographic signatures to verify that responses originate from the chosen DNS resolver and haven't been tampered with.*

     *It is an open specification, with free and opensource reference implementations, and it is not affiliated with any company    nor organization.*

    * Shows available  servers by downloading .csv file from offical repo. No need to specify manually
    * Daemonize the process
```
###NOTE: If you run without arguments, it will display DNSCrypt servers to choose

root@ultron:/# python dnscrypt.py -h
usage: dnscrypt.py [-h] [-H HOST] [-d] [-v]

dnscrypt

optional arguments:
  -h, --help  show this help message and exit
  -H HOST     Connect to this DNS server
  -d          Download DNS server list(/opt/dnscrypt-resolvers.csv) and
              display
  -v          show program's version number and exit
```
   * ### [encryptdns](https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/encryptdns)
     * An `init` script runs `dnscrypt-proxy` on startup
     * Specify `csv_file` location and `resolver_name` in the script. (You get this info from `python dsncrypt.py -d`)
     ```
     sudo wget -O /etc/init.d/encryptdns https://goo.gl/opZ78J
     sudo chmod +x /etc/init.d/encryptdns
     sudo update-rc.d encryptdns defaults
     ```
   `DNSCrypt` runs on localhost(127.0.0.1) port 53. After running the script(if everything is ok) please change the DNS IP in network settings like below
   
   ![Network Setting](https://ibin.co/3a9HBNJosot1.jpg)
   

## 6. [ssid_list.py](https://raw.githubusercontent.com/veerendra2/scripts/master/scripts/ssid_list.py)
   Displays wifi hotspots near to you. Uses the command `iwlist`. Option `-j` will diplays json format with more info. Similar command `nmcli d wifi list`
```
root@android:/opt/scripts# python ssid_list.py -h
usage: ssid_list.py [-h] [-j] [-v]

Displays wifi hotspots info near to you. [Coded by VEERENDRA KAKUMANU]

optional arguments:
  -h, --help  show this help message and exit
  -j          Dumps in json format
  -v          show program's version number and exit
```
```
root@android:/opt/scripts# python ssid_list.py 
+----+---------------------+-------------------+---------+-----------+--------------+
| ID |        ESSID        |    MAC Address    | Channel | Frequency | Singal Level |
+----+---------------------+-------------------+---------+-----------+--------------+
| 01 | Iron                | AA:AA:AA:47:9C:36 | 3       | 2.422 GHz | -51 dBm      |
| 02 | DDDDD XXXXX         | AA:AA:AA:10:D8:10 | 1       | 2.412 GHz | -80 dBm      |
| 03 | XXXXXXXXXXX         | AA:AA:20:7C:58:77 | 1       | 2.412 GHz | -78 dBm      |
| 04 | YYY                 | AA:12:AA:00:61:32 | 1       | 2.412 GHz | -89 dBm      |
| 05 | WWWWWWW             | AA:AA:AA:CF:0B:45 | 2       | 2.417 GHz | -85 dBm      |
| 06 | XXXXXX              | 66:AA:AA:30:AA:86 | 5       | 2.432 GHz | -86 dBm      |
| 07 | Wolverine           | 98:FC:11:AA:44:F2 | 6       | 2.437 GHz | -88 dBm      |
| 08 | NNNN                | 0C:AA:B5:AA:B7:D4 | 9       | 2.452 GHz | -76 dBm      |
| 09 | TTTTTT              | 6C:AA:AA:FC:AA:1B | 11      | 2.462 GHz | -85 dBm      |
| 10 | AAAAAAAAAAAA        | 48:AA:33:AA:D2:95 | 11      | 2.462 GHz | -87 dBm      |
| 11 | GGGGGGGGG           | DC:EF:AA:12:AA:5C | 13      | 2.472 GHz | -84 dBm      |
| 12 | EEEEEE              | AA:3A:AA:1B:9E:30 | 10      | 2.457 GHz | -86 dBm      |
| 13 | RRRRRR              | 1C:AA:2B:61:AA:A7 | 13      | 2.472 GHz | -85 dBm      |
+----+---------------------+-------------------+---------+-----------+--------------+
```
## 7. [pastebin.py](https://goo.gl/g4NGwD)
   A simple `pastebin` tool, sends data to [pastebin.com](https://pastebin.com/) and retrieves ternding pastes.
   
   Usefull when we need to capture huge logs or some output from command. Just have to pipe the output to the script `cat apache.logs | pastebin`
```
root@shadows:/opt# python pastebin.py -h
usage: pastebin.py [-h] [-t] [-p] [-f PFORMAT] [-n PNAME]

Sends data to pastebin.com
[*]PIPE the ouput to the script.                                
Example: echo 'Test' | python pastebin.py

optional arguments:
  -h, --help  show this help message and exit
  -t          Gets trending paste
  -p          Public Paste
  -f PFORMAT  Format of the text(Optional). Please refer formats https://pastebin.com/api#5
  -n PNAME    Name of the past(Optional)
```
   #### How to run the script from any where?
   1. Get the script 
   
      `wget -qO pastebin https://goo.gl/g4NGwD`
   2. Give executable permissions
   
      `chmod +x pastebin`
   3. Copy the script to `/usr/local/bin` directory
   
      `cp pastebin /usr/local/bin`
   
  If every thing is ok, it will shows the pastebin url like below
   ```
   root@shadows:~# echo "Huge output from logs that we need to share." | pastebin -n "pastebin-tool-test"
   https://pastebin.com/UB8M6GBb
   ```

## 8.[wipedisk.sh](https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/wipedisk.sh)
   A simple shell script that fills zeros in empty space. Please refer [stackoverflow](https://superuser.com/questions/19326/how-to-wipe-free-disk-space-in-linux) question for more info
   ```
   ./wipedisk.sh fast shutdown  # Fast wipe and shutdowns
   ./wipedisk.sh fast reboot  # Fast wipe and restart
   ```
   * Avaiable wipes (Arguments)
     * `fast`
     * `med`
     * `slow`

## 9.[httpserver](https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/httpserver.py)
   Simple HTTP server. You can share your directory in LAN
   
   Download: `wget -qO httpserver.py https://goo.gl/fTHcxR && python httpserver.py`
   ```
   veeru@ultron:~/$ python httpserver.py -h
   usage: httpserver.py [-h] [-H HOST] [-p PORT] [-d WEB_DIR]

   Simple HTTP Server

   optional arguments:
     -h, --help  show this help message and exit
     -H HOST     Host IP. Default: 0.0.0.0
     -p PORT     Port. Default: 8001
     -d WEB_DIR  Web Directory. Default: pwd
   ```
   * Run the script from anywhere
   ```
   wget -qO httpserver https://goo.gl/fTHcxR
   sudo chmod +x httpserver
   mv httpserver /usr/local/bin/
   ```
