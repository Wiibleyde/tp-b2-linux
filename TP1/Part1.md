# I. Init

- [I. Init](#i-init)
  - [1. Installation de Docker](#1-installation-de-docker)
  - [2. Vérifier que Docker est bien là](#2-vérifier-que-docker-est-bien-là)
  - [3. sudo c pa bo](#3-sudo-c-pa-bo)
  - [4. Un premier conteneur en vif](#4-un-premier-conteneur-en-vif)
  - [5. Un deuxième conteneur en vif](#5-un-deuxième-conteneur-en-vif)

## 1. Installation de Docker

## 2. Vérifier que Docker est bien là

## 3. sudo c pa bo

🌞 **Ajouter votre utilisateur au groupe `docker`**

```bash
wiibleyde@NBK-Wiibleyde:~$ docker ps
CONTAINER ID   IMAGE                          COMMAND                  CREATED              STATUS              PORTS                                       NAMES
549499ff87ec   phpmyadmin/phpmyadmin:latest   "/docker-entrypoint.…"   About a minute ago   Up About a minute   0.0.0.0:8080->80/tcp, :::8080->80/tcp       phpmyadmin
1d19b76d59fc   mariadb:latest                 "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp   db
```

## 4. Un premier conteneur en vif

🌞 **Lancer un conteneur NGINX**

```bash
wiibleyde@NBK-Wiibleyde:~$ docker ps | grep nginx
249d8389fa27   nginx                          "/docker-entrypoint.…"   15 seconds ago   Up 14 seconds   0.0.0.0:9999->80/tcp, :::9999->80/tcp       agitated_sutherland
```

🌞 **Visitons**

```bash
wiibleyde@NBK-Wiibleyde:~$ docker ps | grep nginx
249d8389fa27   nginx                          "/docker-entrypoint.…"   15 seconds ago   Up 14 seconds   0.0.0.0:9999->80/tcp, :::9999->80/tcp       agitated_sutherland
```
```bash
wiibleyde@NBK-Wiibleyde:~$ docker logs agitated_sutherland 
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/12/21 09:11:27 [notice] 1#1: using the "epoll" event method
2023/12/21 09:11:27 [notice] 1#1: nginx/1.25.3
2023/12/21 09:11:27 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2023/12/21 09:11:27 [notice] 1#1: OS: Linux 6.6.6-200.fc39.x86_64
2023/12/21 09:11:27 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1073741816:1073741816
2023/12/21 09:11:27 [notice] 1#1: start worker processes
2023/12/21 09:11:27 [notice] 1#1: start worker process 29
2023/12/21 09:11:27 [notice] 1#1: start worker process 30
2023/12/21 09:11:27 [notice] 1#1: start worker process 31
2023/12/21 09:11:27 [notice] 1#1: start worker process 32
2023/12/21 09:11:27 [notice] 1#1: start worker process 33
2023/12/21 09:11:27 [notice] 1#1: start worker process 34
2023/12/21 09:11:27 [notice] 1#1: start worker process 35
2023/12/21 09:11:27 [notice] 1#1: start worker process 36
172.17.0.1 - - [21/Dec/2023:09:12:32 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "-"
2023/12/21 09:12:32 [error] 29#29: *1 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 172.17.0.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "localhost:9999", referrer: "http://localhost:9999/"
172.17.0.1 - - [21/Dec/2023:09:12:32 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://localhost:9999/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "-"
```
```bash
wiibleyde@NBK-Wiibleyde:~$ docker inspect agitated_sutherland 
[
    {
        "Id": "249d8389fa272a63f3635bbf1707ab44826f3e616f55d50d93ce68214e39ff6c",
        "Created": "2023-12-21T09:11:26.711686222Z",
        "Path": "/docker-entrypoint.sh",
        "Args": [
            "nginx",
            "-g",
            "daemon off;"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 42216,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2023-12-21T09:11:27.169345484Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        "Image": "sha256:d453dd892d9357f3559b967478ae9cbc417b52de66b53142f6c16c8a275486b9",
        "ResolvConfPath": "/var/lib/docker/containers/249d8389fa272a63f3635bbf1707ab44826f3e616f55d50d93ce68214e39ff6c/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/249d8389fa272a63f3635bbf1707ab44826f3e616f55d50d93ce68214e39ff6c/hostname",
        "HostsPath": "/var/lib/docker/containers/249d8389fa272a63f3635bbf1707ab44826f3e616f55d50d93ce68214e39ff6c/hosts",
        "LogPath": "/var/lib/docker/containers/249d8389fa272a63f3635bbf1707ab44826f3e616f55d50d93ce68214e39ff6c/249d8389fa272a63f3635bbf1707ab44826f3e616f55d50d93ce68214e39ff6c-json.log",
        "Name": "/agitated_sutherland",
        "RestartCount": 0,
        "Driver": "overlay2",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {
                "80/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": "9999"
                    }
                ]
            },
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "ConsoleSize": [
                56,
                217
            ],
            "CapAdd": null,
            "CapDrop": null,
            "CgroupnsMode": "private",
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "private",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "BlkioDeviceReadBps": [],
            "BlkioDeviceWriteBps": [],
            "BlkioDeviceReadIOps": [],
            "BlkioDeviceWriteIOps": [],
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DeviceCgroupRules": null,
            "DeviceRequests": null,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": null,
            "PidsLimit": null,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0,
            "MaskedPaths": [
                "/proc/asound",
                "/proc/acpi",
                "/proc/kcore",
                "/proc/keys",
                "/proc/latency_stats",
                "/proc/timer_list",
                "/proc/timer_stats",
                "/proc/sched_debug",
                "/proc/scsi",
                "/sys/firmware",
                "/sys/devices/virtual/powercap"
            ],
            "ReadonlyPaths": [
                "/proc/bus",
                "/proc/fs",
                "/proc/irq",
                "/proc/sys",
                "/proc/sysrq-trigger"
            ]
        },
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/6ff02285818230dc4244963671dae57a16efc63752304a3c91efacfc2f207ad8-init/diff:/var/lib/docker/overlay2/9752a292d3e63a5428be3523eb75415ae69b0549a899c04ad2f09ddd0be73d84/diff:/var/lib/docker/overlay2/b0cbc45c817b7237af95183e98fce3deb5d4bf05072d6198ced88d0d53ab20c5/diff:/var/lib/docker/overlay2/3f703e0494af20fa48f5ee5943a2334938f40ab3ba5e4388267f1ed963fa0ec6/diff:/var/lib/docker/overlay2/b84a4dd213b8106dd5279a561704e0751957533d8e81f4323188d1c52deee54e/diff:/var/lib/docker/overlay2/0aa77bc61c40c2657cda747dd59b1bc09216951cabdde6dacf5b761d8fe3258c/diff:/var/lib/docker/overlay2/25f0bb105136af3acb80ef684d91b96c034cf4d079aa8900f76ab40038434660/diff:/var/lib/docker/overlay2/db1f8c76be95cdfab2df5cb277157df2310e22eb007db75ee4e68b9ec81b1212/diff",
                "MergedDir": "/var/lib/docker/overlay2/6ff02285818230dc4244963671dae57a16efc63752304a3c91efacfc2f207ad8/merged",
                "UpperDir": "/var/lib/docker/overlay2/6ff02285818230dc4244963671dae57a16efc63752304a3c91efacfc2f207ad8/diff",
                "WorkDir": "/var/lib/docker/overlay2/6ff02285818230dc4244963671dae57a16efc63752304a3c91efacfc2f207ad8/work"
            },
            "Name": "overlay2"
        },
        "Mounts": [],
        "Config": {
            "Hostname": "249d8389fa27",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "80/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "NGINX_VERSION=1.25.3",
                "NJS_VERSION=0.8.2",
                "PKG_RELEASE=1~bookworm"
            ],
            "Cmd": [
                "nginx",
                "-g",
                "daemon off;"
            ],
            "Image": "nginx",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": [
                "/docker-entrypoint.sh"
            ],
            "OnBuild": null,
            "Labels": {
                "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
            },
            "StopSignal": "SIGQUIT"
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "7aa7a981ab8e5a7707a549b6b05da510b4cd7b165a69641693e7c8708c3deccd",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {
                "80/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "9999"
                    },
                    {
                        "HostIp": "::",
                        "HostPort": "9999"
                    }
                ]
            },
            "SandboxKey": "/var/run/docker/netns/7aa7a981ab8e",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "5c88dcb67f169ba7f4edcc30af38f97d935ecae5ad4ad66d273431eb8814cdb4",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:02",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "4671d00d3175535570a4adc76bc377e970d40d2abb6d5ec3f92883b4ece9dea8",
                    "EndpointID": "5c88dcb67f169ba7f4edcc30af38f97d935ecae5ad4ad66d273431eb8814cdb4",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]
```
```bash
wiibleyde@NBK-Wiibleyde:~$ sudo ss -lnpt | grep 9999
LISTEN 0      4096         0.0.0.0:9999      0.0.0.0:*    users:(("docker-proxy",pid=42169,fd=4))   
LISTEN 0      4096            [::]:9999         [::]:*    users:(("docker-proxy",pid=42176,fd=4))   
```
```bash
wiibleyde@NBK-Wiibleyde:~$ curl localhost:9999
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

🌞 **On va ajouter un site Web au conteneur NGINX**

```bash
wiibleyde@NBK-Wiibleyde:~$ curl localhost:9999
<h1>MEOOOW</h1>
```

🌞 **Visitons**

```bash
wiibleyde@NBK-Wiibleyde:~$ docker ps | grep nginx
ba7c7c0f7ec1   nginx                          "/docker-entrypoint.…"   4 seconds ago   Up 3 seconds   80/tcp, 0.0.0.0:9999->8080/tcp, :::9999->8080/tcp   reverent_kilby
```
```bash
wiibleyde@NBK-Wiibleyde:~$ sudo firewall-cmd --list-all
FedoraWorkstation (default, active)
  target: default
  ingress-priority: 0
  egress-priority: 0
  icmp-block-inversion: no
  interfaces: wlp0s20f3
  sources: 
  services: dhcpv6-client mdns samba-client ssh
  ports: 1025-65535/udp 1025-65535/tcp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```
```bash
wiibleyde@NBK-Wiibleyde:~$ curl localhost:9999
<h1>MEOOOW</h1>
```

## 5. Un deuxième conteneur en vif

🌞 **Lance un conteneur Python, avec un shell**

```bash
wiibleyde@NBK-Wiibleyde:~$ docker run -it python bash
Unable to find image 'python:latest' locally
latest: Pulling from library/python
bc0734b949dc: Pull complete 
b5de22c0f5cd: Pull complete 
917ee5330e73: Pull complete 
b43bd898d5fb: Pull complete 
7fad4bffde24: Pull complete 
d685eb68699f: Pull complete 
107007f161d0: Pull complete 
02b85463d724: Pull complete 
Digest: sha256:3733015cdd1bd7d9a0b9fe21a925b608de82131aa4f3d397e465a1fcb545d36f
Status: Downloaded newer image for python:latest
root@879d8233cc22:/# python
Python 3.12.1 (main, Dec 19 2023, 20:14:15) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit
Use exit() or Ctrl-D (i.e. EOF) to exit
>>> exit()
```

🌞 **Installe des libs Python**

```bash
root@879d8233cc22:/# python
Python 3.12.1 (main, Dec 19 2023, 20:14:15) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import aiohttp
>>> 
```