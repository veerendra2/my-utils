# Some usefull python scripts and snippets
1. [changer init script](https://github.com/veerendra2/python-scripts/blob/master/scripts/changer)

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
