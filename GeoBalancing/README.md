Decription
===========

This Step-by-Step instruction, of how to install Geoip2 module to nginx and configure Geo balancing.

**ngx_http_geoip2_module** - creates variables with values from the maxmind geoip2 databases based on the client IP (default) or from a specific variable (supports both IPv4 and IPv6)

The module now supports nginx streams and can be used in the same way the http module can be used.

This instruction tested on Debian 9, but most likely will work on any ubuntu
Used nginx versiont 1.14.1, but will work on nginx 1.9.11+

#####1. Install dependecies
For maxminddb:

```
$sudo apt install libmaxminddb0 libmaxminddb-dev mmdb-bin
```

For nginx compilation:
```
$sudo apt install nginx libxslt-dev libxslt1-dev libgeoip-dev libgd-dev libpcre++-dev libpcre++0v5 zlib1g zlib1g-dev libssl-dev
```

#####2. Get geoip2 module

Its official repository of geoip2 module

```
git clone https://github.com/leev/ngx_http_geoip2_module
```

#####3. Compile nginx.
First of all lets check current nginx version

```
$nginx -v
```

Now we need to find all flags that used to complile our nginx version:

```
$nginx -V
nginx version: nginx/1.14.1
built with OpenSSL 1.1.0f  25 May 2017 (running with OpenSSL 1.1.0j  20 Nov 2018)
TLS SNI support enabled
configure arguments: --with-cc-opt='-g -O2 -fdebug-prefix-map=/build/nginx-jqo7Nx/nginx-1.14.1=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --modules-path=/usr/lib/nginx/modules --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-debug --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --with-http_addition_module --with-http_geoip_module=dynamic --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_xslt_module=dynamic --with-stream=dynamic --with-stream_ssl_module --with-stream_ssl_preread_module --with-mail=dynamic --with-mail_ssl_module --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-auth-pam --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-dav-ext --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-echo --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-upstream-fair --add-dynamic-module=/build/nginx-jqo7Nx/nginx-1.14.1/debian/modules/http-subs-filter

```

Than remove all "--add-dynamic-module=" from arguments and add geoip module --add-dynamic-module=/path/to/ngx_http_geoip2_module



