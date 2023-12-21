# II. Images

- [II. Images](#ii-images)
  - [1. Images publiques](#1-images-publiques)
  - [2. Construire une image](#2-construire-une-image)

## 1. Images publiques

🌞 **Récupérez des images**

```bash
docker pull python:3.11
docker pull mysql:5.7
docker pull wordpress
docker pull linuxserver/wikijs
```
```bash
docker images
```

🌞 **Lancez un conteneur à partir de l'image Python**

```bash
root@d9115abb1cf5:/# python --version
Python 3.11.7
```

## 2. Construire une image


🌞 **Ecrire un Dockerfile pour une image qui héberge une application Python**

```dockerfile
FROM debian:11

RUN apt update && apt install -y python3 python3-pip
RUN pip install emoji

COPY app.py /app.py

ENTRYPOINT ["python3", "/app.py"]
```

```python
import emoji

print(emoji.emojize("Cet exemple d'application est vraiment naze :thumbs_down:"))
```

🌞 **Build l'image**

```bash
wiibleyde@NBK-Wiibleyde:~/B2-Docker/TP1$ docker build -t python_app:latest ./python_app_build
```

🌞 **Lancer l'image**

```bash
docker run python_app:latest
```