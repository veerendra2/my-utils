# Web Server Sample Configurations

### Docs Links
* [Web Server](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/)
* [Core HTTP in-built variables](https://nginx.org/en/docs/http/ngx_http_core_module.html#variables)

### Configuration Structure
```
http {
  server {
  
    location / {
     
    }
  }
}
```

### Self Signed Certificates Generation
```
$ mkdir /etc/nginx/ssl
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.pem
```