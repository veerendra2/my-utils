# Load Balancing Sample Configurations
### Docs Links
* [HTTP Docs](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)

## build docker image quick test the config
[nginx docker image](https://hub.docker.com/_/nginx)
```
$ sudo docker build my-nginx .
$ sudo docker run -d -p 8080:80 my-nginx
```

## HTTP Load Balancing
#### Load Balancer Method
* `least_conn;` - Least Connections:  A request is sent to the server with the least number of active connections, again with `server weights` taken into consideration
* `ip_hash;` - IP Hash: The server to which a request is sent is determined from the client IP address. In this case, either the first three octets of the IPv4 address or the whole IPv6 address are used to calculate the hash value
* `hash` - Generic Hash: 

#### Session Persistence
*Nginx PLUS Only
Supports 3 session persistence methods with `sticky` directive.
* `sticky cookie` - Adds a session cookie to the first response from the upstream group and identifies the server that sent the response.
* `sticky route` - Assigns a `route` to the client when it receives the first request. All subsequent requests are compared with `route` and forwards to same server
* `sticky learn` - 

- Open source module: [https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/src/master/](https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/src/master/)

#### Sharing Data with Multiple Worker Processes
Each worker process keeps its own copy of the server group configuration and maintains its own set of related counters.

When the zone directive is included in an upstream block, the configuration of the upstream group is kept in a memory area shared among all worker processes. This scenario is dynamically configurable, because the worker processes access the same copy of the group configuration and utilize the same related counters.

## TCP and UDP Load Balancing
_*Prerequisites: NGINX Plus or NGINX Open Source built with the `--with-stream` configuration flag_

NOTE: This configuration is not to be added to the `conf.d` folder as that folder is included within an `http` block; instead, you should create another folder named `stream.conf.d`, open the `stream` block in the `nginx.conf` file, and include the new folder for stream configurations.


## Health Checks
#### Passive Checks

`fail_timeout`- Sets the time during which a number of failed attempts must happen for the server to be marked unavailable, and also the time for which the server is marked unavailable (default is 10 seconds).
`max_fails` - Sets the number of failed attempts that must occur during the fail_timeout period for the server to be marked unavailable (default is 1 attempt).

Example:
```
upstream backend {
    server backend1.example.com;
    server backend2.example.com max_fails=3 fail_timeout=30s;
}
```
#### Active Checks
_*Nginx Plus Only_

```
server {
    location / {
        proxy_pass http://backend;
        health_check;
    }
}
```
