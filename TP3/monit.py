#!/usr/bin/python3
import psutil
import json
import os
import socket
import discord_webhook
from datetime import datetime
import glob
import hashlib
import sys

SAVE_FOLDER = './monit-saves'
USER = 'monit'

cmd = {
    'check': 'Check les valeurs de RAM, CPU, Disques et Ports ouverts',
    'list': 'Liste des rapports',
    'get': {
        'last': 'Récupère le dernier rapport',
        'avg': {
            'X': 'Récupère la moyenne des X dernières heures'
        }
    }
}

default_config = {
    'tcp_ports': [],
    'webhook_url': ''
}

class Monit:
    def checkRam(self) -> int:
        return psutil.virtual_memory().percent
    
    def checkCpu(self) -> int:
        return psutil.cpu_percent()
    
    def checkDisk(self) -> int:
        return psutil.disk_usage('/').percent
    
    def checkOpenPort(self, port: int) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0

class Config:
    def __init__(self, path: str):
        self.path = path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.data = json.loads(f.read())
        else:
            self.data = default_config
            self.save()

    def save(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.data, indent=4, separators=(',', ': ')))

    def get(self, key: str):
        return self.data[key]
    
    def set(self, key: str, value):
        self.data[key] = value
        self.save()

class MonitBot:
    def __init__(self, config: Config):
        self.config = config
        self.monit = Monit()
        self.webhook = discord_webhook.DiscordWebhook(url=self.config.get('webhook_url'), content='')

    def alert(self, message: str, level: int):
        embed = discord_webhook.DiscordEmbed(title='Alerte', description=message, color=0xffffff)
        if level == 1:
            embed.color = 0xff0000
        elif level == 2:
            embed.color = 0xffff00
        self.webhook.add_embed(embed)
        self.webhook.execute()

class Save:
    def __init__(self, path: str):
        self.path = path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.data = json.loads(f.read())
        else:
            self.data = {}
            self.save()

    def save(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.data, separators=(',', ':')))

    def insertSave(self, id:str, date: str, ram: int, cpu: int, disk: int, ports: dict):
        report = {
            'id': id,
            'date': date,
            'report': {
                'ram': ram,
                'cpu': cpu,
                'disk': disk,
                'ports': ports
            }
        }
        self.data = report
        self.save()

class Calls:
    def requestCheck():
        check()
        last = getLast(SAVE_FOLDER + '/save*.json')
        return {
            'ram': last['report']['ram'],
            'cpu': last['report']['cpu'],
            'disk': last['report']['disk'],
            'ports': last['report']['ports']
        }
    
    def requestReports():
        files = glob.glob(SAVE_FOLDER + '/save*.json')
        files.sort(key=os.path.getmtime)
        reports = []
        for file in files:
            with open(file, 'r') as f:
                reports.append(json.loads(f.read()))
        return reports
    
    def requestLast():
        return getLast(SAVE_FOLDER + '/save*.json')
    
    def requestAvg(hours: int):
        return getAvg(SAVE_FOLDER + '/save*.json', hours)
    
    def requestReport(id: str):
        files = glob.glob(SAVE_FOLDER + '/save*.json')
        files.sort(key=os.path.getmtime)
        for file in files:
            with open(file, 'r') as f:
                data = json.loads(f.read())
                if data['id'] == id:
                    return data
        return None

def getLevel(value:int) -> int:
    if value > 90:
        return 2
    elif value > 80:
        return 1
    else:
        return 0

def getReport(monit: Monit, save: Save, config: Config) -> tuple:
    ram = monit.checkRam()
    cpu = monit.checkCpu()
    disk = monit.checkDisk()
    ports = {}
    for port in config.get('tcp_ports'):
        ports[port] = monit.checkOpenPort(port)
    return (ram, cpu, disk, ports)

def check():
    nowTime = datetime.now().timestamp()
    config = Config('config.json')
    save = Save(f'{SAVE_FOLDER}/save{datetime.now().strftime('%d-%m-%Y %H:%M:%S').replace(' ','-')}.json')
    bot = MonitBot(config)
    report = getReport(Monit(), save, config)
    uuid = hashlib.md5(str(report).encode()).hexdigest()
    save.insertSave(uuid, nowTime, report[0], report[1], report[2], report[3])
    ramLevel = getLevel(report[0])
    if ramLevel >= 1:
        bot.alert('RAM au dessus de 80%', ramLevel)
    cpuLevel = getLevel(report[1])
    if cpuLevel >= 1:
        bot.alert('CPU au dessus de 80%', cpuLevel)
    diskLevel = getLevel(report[2])
    if diskLevel >= 1:
        bot.alert('Disque au dessus de 80%', diskLevel)

def getLast(path: str) -> dict:
    files = glob.glob(path)
    if len(files) == 0:
        return {}
    files.sort(key=os.path.getmtime)
    with open(files[-1], 'r') as f:
        return json.loads(f.read())
    
def getAvg(path: str, hours: int) -> dict:
    files = glob.glob(path)
    if len(files) == 0:
        return {}
    files.sort(key=os.path.getmtime)
    files = files[-hours:]
    avg = {
        'ram': 0,
        'cpu': 0,
        'disk': 0,
    }
    for file in files:
        with open(file, 'r') as f:
            data = json.loads(f.read())
            avg['ram'] += data['report']['ram']
            avg['cpu'] += data['report']['cpu']
            avg['disk'] += data['report']['disk']
    avg['ram'] /= len(files)
    avg['cpu'] /= len(files)
    avg['disk'] /= len(files)
    avg['ram'] = round(avg['ram'], 2)
    avg['cpu'] = round(avg['cpu'], 2)
    avg['disk'] = round(avg['disk'], 2)
    return avg
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        print('Usage: python monit.py <command> <args>')
        print('Commands:')
        for key in cmd:
            if type(cmd[key]) == str:
                print(f'\t{key}: {cmd[key]}')
            else:
                print(f'\t{key}:')
                for key2 in cmd[key]:
                    if type(cmd[key][key2]) == str:
                        print(f'\t\t{key2}: {cmd[key][key2]}')
                    else:
                        print(f'\t\t{key2}:')
                        for key3 in cmd[key][key2]:
                            print(f'\t\t\t{key3}: {cmd[key][key2][key3]}')
    elif args[0] == 'init':
        print('To init the folder, please run the init.sh script')
    elif args[0] == 'check':
        check()
    elif args[0] == 'list':
        files = glob.glob(SAVE_FOLDER + '/save*.json')
        files.sort(key=os.path.getmtime)
        for file in files:
            print(file)
    elif args[0] == 'get':
        if len(args) == 1:
            print('Usage: python monit.py get <command> <args>')
            print('Commands:')
            for key in cmd['get']:
                if type(cmd['get'][key]) == str:
                    print(f'\t{key}: {cmd["get"][key]}')
                else:
                    print(f'\t{key}:')
                    for key2 in cmd['get'][key]:
                        print(f'\t\t{key2}: {cmd["get"][key][key2]}')
        elif args[1] == 'last':
            print(getLast(SAVE_FOLDER + '/save*.json'))
        elif args[1] == 'avg':
            if len(args) == 2:
                print('Usage: python monit.py get avg <hours>')
            else:
                print(getAvg(SAVE_FOLDER + '/save*.json', int(args[2])))
    else:
        print('Usage: python monit.py <command> <args>')
        print('Commands:')
        for key in cmd:
            if type(cmd[key]) == str:
                print(f'\t{key}: {cmd[key]}')
            else:
                print(f'\t{key}:')
                for key2 in cmd[key]:
                    if type(cmd[key][key2]) == str:
                        print(f'\t\t{key2}: {cmd[key][key2]}')
                    else:
                        print(f'\t\t{key2}:')
                        for key3 in cmd[key][key2]:
                            print(f'\t\t\t{key3}: {cmd[key][key2][key3]}')