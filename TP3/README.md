# Monitoring App

## Description

This is a simple monitoring app that can be used to monitor the status of a server. 

## Installation

To install the app, you need to have python3 and docker installed on your machine.

Then, you need to install the requirements using the following command:

```bash
pip install -r requirements.txt
```

## Usage

To use the app, you need to run create the configuration file using the following command:
```bash
python3 app.py init
```

This will create a configuration file in the current directory. You can then edit the configuration file to add the servers you want to monitor.
Example of configuration file : 
```json
{
    "tcp_ports": [80, 443, 5000, 8080, 8081, 8082, 8083, 8084, 8085, 8086],
    "webhook_url": ""
}
```

Then, you can run the app:

### To start a check
```bash
docker compose up
```

You can now access the app on http://localhost:5000/apidocs/ to look at the API documentation.

# Happy monitoring
![meme](https://media.makeameme.org/created/no-worries-its-5bb659.jpg)


