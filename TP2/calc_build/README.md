🌞 Packager l'application de calculatrice réseau || 🌞 Environnement : adapter le code si besoin

```bash
wiibleyde@NBK-Wiibleyde:~/Documents/Ynov/tp-b2-linux/TP2/calc_build$ docker compose build
[+] Building 0.6s (12/12) FINISHED                                                                                                                                              docker:default
 => [bot internal] load build definition from Dockerfile                                                                                                                                  0.0s
 => => transferring dockerfile: 385B                                                                                                                                                      0.0s
 => [bot internal] load .dockerignore                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                           0.0s
 => [bot internal] load metadata for docker.io/library/python:3.12                                                                                                                        0.3s
 => [bot 1/7] FROM docker.io/library/python:3.12@sha256:3733015cdd1bd7d9a0b9fe21a925b608de82131aa4f3d397e465a1fcb545d36f                                                                  0.0s
 => [bot internal] load build context                                                                                                                                                     0.0s
 => => transferring context: 4.59kB                                                                                                                                                       0.0s
 => CACHED [bot 2/7] WORKDIR /app                                                                                                                                                         0.0s
 => CACHED [bot 3/7] COPY requirements.txt .                                                                                                                                              0.0s
 => CACHED [bot 4/7] RUN python3 -m pip install -r requirements.txt                                                                                                                       0.0s
 => [bot 5/7] COPY calc.py .                                                                                                                                                              0.0s
 => [bot 6/7] COPY src/logs.py ./src/                                                                                                                                                     0.0s
 => [bot 7/7] RUN mkdir -p /app/logs/                                                                                                                                                     0.1s
 => [bot] exporting to image                                                                                                                                                              0.0s
 => => exporting layers                                                                                                                                                                   0.0s
 => => writing image sha256:bcec78dbc5615fd80a739e6f800726518f7b77c76e1965cfab9ca37c7fec8ea3                                                                                              0.0s
 => => naming to docker.io/wiibleyde/fcbot:latest   
```
```bash
wiibleyde@NBK-Wiibleyde:~/Documents/Ynov/tp-b2-linux/TP2/calc_build$ docker compose up 
[+] Running 2/2
 ✔ Network calc_build_default  Created                                                                                                                                                    0.1s 
 ✔ Container calculator        Created                                                                                                                                                    0.0s 
Attaching to calculator
calculator  | 2023-12-21 10:23:17,204 - INFO Le serveur tourne sur 127.0.0.1:13337
^CGracefully stopping... (press Ctrl+C again to force)
Aborting on container exit...
[+] Stopping 1/1
 ✔ Container calculator  Stopped                                                                                                                                                         10.2s 
canceled
```

