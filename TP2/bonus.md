# Bonus CI/CD

## Sommaire

- [Bonus CI/CD](#bonus-cicd)
  - [Sommaire](#sommaire)
- [0. Setup](#0-setup)
- [I. Premiers pas CI](#i-premiers-pas-ci)
  - [1. Préparation runner](#1-préparation-runner)
  - [2. Une première pipeline](#2-une-première-pipeline)
  - [3. Quelques idées pour la pipeline](#3-quelques-idées-pour-la-pipeline)
- [II. Premier déploiement CD](#ii-premier-déploiement-cd)
  - [1. Préparation](#1-préparation)
    - [A. SSH](#a-ssh)
    - [B. Gitlab](#b-gitlab)
  - [2. Déploiement automatique : CD](#2-déploiement-automatique--cd)
- [III. Cas concret ?](#iii-cas-concret-)

# 0. Setup

# I. Premiers pas CI

## 1. Préparation runner

🌞 **Préparer un fichier de conf pour le Runner**

```bash
[wiibleyde@runner-bonus ~]$ cat runner/conf/config.toml 
concurrent = 4
```

🌞 **Lancer le Runner**

```bash
[wiibleyde@runner-bonus ~]$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS         PORTS     NAMES
dfdcc18f201a   gitlab/gitlab-runner:latest   "/usr/bin/dumb-init …"   3 seconds ago   Up 2 seconds             gitlab-runner
```

🌞 **Effectue un *register* depuis le Runner**

```bash
root@dfdcc18f201a:/# cat /etc/gitlab-runner/config.toml 
concurrent = 1
check_interval = 0
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "symfony"
  url = "https://gitlab.com/"
  id = 30856295
  token = ";)"
  token_obtained_at = 2023-12-22T09:39:25Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.cache]
    MaxUploadedArchiveSize = 0
  [runners.docker]
    tls_verify = false
    image = "php:8.2"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
    network_mtu = 0
```

## 2. Une première pipeline

🌞 **Créer un fichier `.gitlab-ci.yml`**

```yml
stages:
  - mon_premier_stage

mon_premier_stage:
  stage: mon_premier_stage
  image: alpine
  script:
    - echo "Hello World"
```

## 3. Quelques idées pour la pipeline

# II. Premier déploiement CD

## 1. Préparation

### A. SSH

🌞 **Générez une nouvelle paire de clés SSH**

```bash
wiibleyde@NBK-Wiibleyde:~/Documents/Perso/ssh_key$ ls | grep gitlab
gitlab
gitlab.pub
```

🌞 **Déposer la clé publique sur `prod.bonus`**

```bash
wiibleyde@creatia:~$ cat .ssh/authorized_keys | grep Wiibleyde
ssh-rsa [...] wiibleyde@NBK-Wiibleyde
```

### B. Gitlab

🌞 **Créer une variable de CI qui contient la clé privée**



## 2. Déploiement automatique : CD

🌞 **Adaptez votre `.gitlab-ci.yml`**

```yml
stages:
  - build
  - deploy

just_a_test:
  stage: build
  image: python
  script:
    - cat /etc/os-release
    - python --version

deploy_to_prod:
  stage: deploy
  image: debian
  before_script:
    - 'command -v ssh-agent >/dev/null || ( apt-get update -y && apt-get install openssh-client -y )'
    - eval $(ssh-agent -s)
    - mkdir ~/.ssh && chmod 700 ~/.ssh 
    - echo "$PRIVATE_KEY" | base64 -d | tr -d '\r' | ssh-add - 
    - ssh-keyscan creatia > ~/.ssh/known_hosts
  script:
    - ssh wiibleyde@creatia whoami
```

```bash
[0KRunning with gitlab-runner 16.7.0 (102c81ba)[0;m
[0K  on symfony xvJoFTzD, system ID: r_4ndfjyTeCrtd[0;m
section_start:1703240385:prepare_executor
[0K[0K[36;1mPreparing the "docker" executor[0;m[0;m
[0KUsing Docker executor with image python ...[0;m
[0KPulling docker image python ...[0;m
[0KUsing docker image sha256:fc7a60e86baeb42215d3f91f262880a3a9b4efd00c91f6597e65d9e1c7745ec9 for python with digest python@sha256:3733015cdd1bd7d9a0b9fe21a925b608de82131aa4f3d397e465a1fcb545d36f ...[0;m
section_end:1703240407:prepare_executor
[0Ksection_start:1703240407:prepare_script
[0K[0K[36;1mPreparing environment[0;m[0;m
Running on runner-xvjoftzd-project-53288648-concurrent-0 via dfdcc18f201a...
section_end:1703240408:prepare_script
[0Ksection_start:1703240408:get_sources
[0K[0K[36;1mGetting source from Git repository[0;m[0;m
[32;1mFetching changes with git depth set to 20...[0;m
Reinitialized existing Git repository in /builds/wiibleydev/projet-symfony/.git/
[32;1mChecking out 35a72dc5 as detached HEAD (ref is dev)...[0;m

[32;1mSkipping Git submodules setup[0;m
section_end:1703240409:get_sources
[0Ksection_start:1703240409:step_script
[0K[0K[36;1mExecuting "step_script" stage of the job script[0;m[0;m
[0KUsing docker image sha256:fc7a60e86baeb42215d3f91f262880a3a9b4efd00c91f6597e65d9e1c7745ec9 for python with digest python@sha256:3733015cdd1bd7d9a0b9fe21a925b608de82131aa4f3d397e465a1fcb545d36f ...[0;m
[32;1m$ cat /etc/os-release[0;m
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
[32;1m$ python --version[0;m
Python 3.12.1
section_end:1703240409:step_script
[0Ksection_start:1703240409:cleanup_file_variables
[0K[0K[36;1mCleaning up project directory and file based variables[0;m[0;m
section_end:1703240409:cleanup_file_variables
[0K[32;1mJob succeeded[0;m
```

# III. Cas concret ?

```Dockerfile
FROM php:8.2

RUN apt update && apt install -y git
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /app
COPY . /app

RUN composer install
```

```yml
stages:
  - build
  - deploy

syntax:
    stage: build
    image: docker/compose:debian-2.0.1
    script:
        - docker-compose config
        - docker-compose run --rm php vendor/bin/phpcs --standard=PSR12 src/
    rules:
        - if: $CI_COMMIT_BRANCH == "dev"

docker_build:
    stage: build
    image: docker:20.10.9
    services:
        - docker:20.10.9-dind
    variables:
        DOCKER_HOST: tcp://docker:2375
        DOCKER_TLS_CERTDIR: ""
    script:
        - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
        - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
        - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    rules:
        - if: $CI_COMMIT_BRANCH == "dev"

prod:
    stage: deploy
    image: alpine
    before_script:
        - apk add openssh-client
        - mkdir -p ~/.ssh
        - echo "$SSH_PRIVATE_KEY" | tr -d '\r' > ~/.ssh/id_rsa
        - chmod 600 ~/.ssh/id_rsa
        - ssh-keyscan -H $SSH_HOST >> ~/.ssh/known_hosts
    script:
        - ssh -i ~/.ssh/id_rsa $SSH_USER@$SSH_HOST "cd /home/wiibleyde/projet-symfony && git pull && docker-compose up -d"
    rules:
        - if: $CI_COMMIT_BRANCH == "dev"
```

```yml
stages:
  - build
  - deploy

syntax:
    stage: build
    image: docker/compose:debian-2.0.1
    script:
        - docker-compose config
        - docker-compose run --rm php vendor/bin/phpcs --standard=PSR12 src/
    rules:
        - if: $CI_COMMIT_BRANCH == "dev"

docker_build:
    stage: build
    image: docker:20.10.9
    services:
        - docker:20.10.9-dind
    variables:
        DOCKER_HOST: tcp://docker:2375
        DOCKER_TLS_CERTDIR: ""
    script:
        - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
        - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
        - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    rules:
        - if: $CI_COMMIT_BRANCH == "dev"

prod:
    stage: deploy
    image: alpine
    before_script:
        - apk add openssh-client
        - mkdir -p ~/.ssh
        - echo "$SSH_PRIVATE_KEY" | tr -d '\r' > ~/.ssh/id_rsa
        - chmod 600 ~/.ssh/id_rsa
        - ssh-keyscan -H $SSH_HOST >> ~/.ssh/known_hosts
    script:
        - ssh -i ~/.ssh/id_rsa $SSH_USER@$SSH_HOST "cd /home/wiibleyde/projet-symfony && git pull && docker-compose up -d"
    rules:
        - if: $CI_COMMIT_BRANCH == "dev"
```
