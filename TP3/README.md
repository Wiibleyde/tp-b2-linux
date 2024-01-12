# Monitoring App

## Description

This is a simple monitoring app that can be used to monitor the status of a server. 

## Installation

To install the app, you need to have python3 installed on your machine. 

Then, you need to install the requirements using the following command:

```bash
pip install -r requirements.txt
```

## Usage

To use the app, you need to run create the configuration file using the following command:
```bash
python3 app.py init
```

Then, you can run the app:

### To start a check
```bash
python3 app.py check
```

### To get last check result
```bash
python3 app.py get last
```

### To get average for a specific period (In hours)
```bash
python3 app.py get avg X
```
- X: Number of hours

# Happy monitoring
![meme](https://media.makeameme.org/created/no-worries-its-5bb659.jpg)


