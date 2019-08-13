Description
===========

This Step-by-Step instruction, of how to install Geoip2 module to nginx and configure Geo balancing.

**ngx_http_geoip2_module** - creates variables with values from the maxmind geoip2 databases based on the client IP (default) or from a specific variable (supports both IPv4 and IPv6)

The module now supports nginx streams and can be used in the same way the http module can be used.

This instruction tested on Debian 9, but most likely will work on any ubuntu
Used nginx versiont 1.14.1, but will work on nginx 1.9.11+
If you decide to use nginx 1.14.1 you may omit compilation step 3, and take compiled module from this repo.

#### 1. Install dependecies
For maxminddb:

```
$sudo apt install libmaxminddb0 libmaxminddb-dev mmdb-bin
```

For nginx compilation:
```
$sudo apt install nginx libxslt-dev libxslt1-dev libgeoip-dev libgd-dev libpcre++-dev libpcre++0v5 zlib1g zlib1g-dev libssl-dev
```

#### 2. Get geoip2 module

Its official repository of geoip2 module

```
git clone https://github.com/leev/ngx_http_geoip2_module
```

#### 3. Compile nginx.
First of all lets check current nginx version

```
$nginx -v
```
Get souces of intalled version
```
wget http://nginx.org/download/nginx-VERSION.tar.gz
tar zxvf nginx-VERSION.tar.gz
cd nginx-VERSION
```

Now we need to find all flags that used to complile our nginx version:


```
$nginx -V
nginx version: nginx/1.14.1
built with OpenSSL 1.1.0f  25 May 2017 (running with OpenSSL 1.1.0j  20 Nov 2018)
TLS SNI support enabled
configure arguments: --with-cc-opt='-g -O2 -fdebug-prefix-map=/build/nginx-jqo7Nx/nginx-1.14.1=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --modules-path=/usr/lib/nginx/modules --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-debug --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --with-http_addition_module --with-http_geoip_module=dynamic --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_xslt_module=dynamic --with-stream=dynamic --with-stream_ssl_module --with-stream_ssl_preread_module --with-mail=dynamic --with-mail_ssl_module --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-auth-pam --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-dav-ext --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-echo --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-upstream-fair --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-subs-filter

```

Than remove all "--add-dynamic-module=" from arguments and add geoip module --add-dynamic-module=/path/to/ngx_http_geoip2_module (set your path)

Now compile nginx:

```
./configure --add-dynamic-module=/path/to/ngx_http_geoip2_module   --with-cc-opt='-g -O2 -fdebug-prefix-map=/build/nginx-jqo7Nx/nginx-1.14.1=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --modules-path=/usr/lib/nginx/modules --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-debug --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --with-http_addition_module --with-http_geoip_module=dynamic --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_xslt_module=dynamic --with-stream=dynamic --with-stream_ssl_module --with-stream_ssl_preread_module --with-mail=dynamic --with-mail_ssl_module

make
```
After make finish, we will have compiled module in obj/ngx_http_geoip2_module.so

Now copy it to nginx directory

#### 4.Preparing nginx configuration

Copy geoip2 module to nginx modules directory
```
cp obj/ngx_http_geoip2_module.so /usr/share/nginx/modules/ngx_http_geoip2_module.so
```

Enable geoip2 module in config
```
echo 'load_module modules/ngx_http_geoip2_module.so;' > /etc/nginx/modules-enabled/50-mod-geoip2.conf
```

Download MaxMind DB files from https://dev.maxmind.com/geoip/geoip2/geolite2/
we need GeoLite2 City and GeoLite2 Country. And put them to /etc/nginx

In http{} section of nginx.conf put next lines:

```
    geoip2 /etc/nginx/GeoLite2-Country.mmdb {
        auto_reload 5m;
        $geoip2_metadata_country_build metadata build_epoch;
        $geoip2_data_country_code default=US source=$remote_addr country iso_code;
        $geoip2_data_country_name country names en;
    }

    geoip2 /etc/nginx/GeoLite2-City.mmdb {
        $geoip2_data_city_name default=London city names en;


        log_format main '$geoip2_data_country_code $geoip2_data_country_name $remote_addr - $remote_user [$time_local] "$request" ' 
'$status $body_bytes_sent "$http_referer" ' '"$http_user_agent" "$http_x_forwarded_for"'; 
        access_log /var/log/nginx/access.log main;

```

Now try to restart nginx
```
/etc/init.d/nginx restart
```

Example of virtual hosts configuration:


```
server {
        listen 8080 default_server;

        server_name _;

        location / {
                #proxy_pass http://appservers;
                proxy_pass http://$nearest_server;
                # add_header X-Upstream $upstream_addr;
                #proxy_set_header Host $host;
                #proxy_set_header X-Real-IP $remote_addr;
                #proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_read_timeout 150;
        }
        location /nginx_status {
                stub_status on;
                access_log off;
                allow 127.0.0.1;
                allow ::1;
                deny all;
        }
}

    #map $geoip_city_continent_code $nearest_server {
    map $geoip2_data_country_code $nearest_server {
        US      us;
        RU      ru;
        SG      sg;
        NL      nl;
        default ca;
    } 
    upstream ru {
        server 172.17.0.5:80;
    }
    upstream nl {
        server 172.17.0.7:80;
    }
     upstream ca {
        server 172.17.0.4:80;
    }
    upstream us {
        server 172.17.0.3:80;
    }
    upstream sg {
        server 172.17.0.6:80;
    }

```

#### 5 Create docker containers for test(Optional)

Build image that listen port 80 and return container hostname:
```
$cd apache_docker
$docker build .
```
Create few containers:

```
$docker run -dit  -h singapore -name singapore <image id>
$docker run -dit  -h canada -name canada <image id>
```

Check on which adress they listen:
```
docker inspect <container id>
```









