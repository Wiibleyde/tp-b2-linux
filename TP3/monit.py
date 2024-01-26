#!/usr/bin/python3

"""
Monit
"""

from os import path
from datetime import datetime
import json
import glob
import hashlib
import sys
import socket
import psutil
import discord_webhook

SAVE_FOLDER = "/var/monit"
USER = "monit"

cmd = {
    "check": "Check les valeurs de RAM, CPU, Disques et Ports ouverts",
    "list": "Liste des rapports",
    "get": {
        "last": "Récupère le dernier rapport",
        "avg": {"X": "Récupère la moyenne des X dernières heures"},
    },
}

default_config = {"tcp_ports": [], "webhook_url": ""}


class Monit:
    """Monit class"""

    def check_ram(self) -> int:
        """Check the RAM usage

        Returns:
            int: RAM usage in percent
        """
        return psutil.virtual_memory().percent

    def check_cpu(self) -> int:
        """Check the CPU usage

        Returns:
            int: CPU usage in percent
        """
        return psutil.cpu_percent()

    def check_disk(self) -> int:
        """Check the disk usage

        Returns:
            int: Disk usage in percent
        """
        return psutil.disk_usage("/").percent

    def check_open_port(self, port: int) -> bool:
        """Check if the port is open

        Args:
            port (int): Port to check

        Returns:
            bool: True if the port is open, False if not
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        return result == 0


class Config:
    """Config class"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = {}
        self.load()

    def load(self):
        """Load the config file"""
        if path.exists(self.file_path):
            with open(self.file_path, "r", encoding='utf8') as f:
                self.data = json.loads(f.read())
        else:
            self.data = default_config
            self.save()

    def save(self):
        """Save the config file"""
        with open(self.file_path, "w", encoding='utf8') as f:
            f.write(json.dumps(self.data, indent=4, separators=(",", ": ")))

    def get(self, key_wanted: str):
        """Get a value from the config

        Args:
            key (str): Key to get

        Returns:
            Any: Value of the key
        """
        return self.data[key_wanted]

    def set(self, key_wanted: str, value):
        self.data[key_wanted] = value
        self.save()


class MonitBot:
    """MonitBot class"""

    def __init__(self, config: Config):
        self.config = config
        self.monit = Monit()
        self.webhook = discord_webhook.DiscordWebhook(
            url=self.config.get("webhook_url"), content=""
        )

    def alert(self, message: str, level: int):
        """Send an alert to the discord webhook

        Args:
            message (str): Message to send
            level (int): Level of the alert
        """
        embed = discord_webhook.DiscordEmbed(
            title="Alerte", description=message, color=0xFFFFFF
        )
        if level == 1:
            embed.color = 0xFF0000
        elif level == 2:
            embed.color = 0xFFFF00
        self.webhook.add_embed(embed)
        self.webhook.execute()


class Save:
    """Save class"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = {}
        self.load()

    def load(self):
        """Load the save file"""
        if path.exists(self.file_path):
            with open(self.file_path, "r", encoding='utf8') as f:
                self.data = json.loads(f.read())
        else:
            self.data = {}
            self.save()

    def save(self):
        """Save the save file"""
        with open(self.file_path, "w", encoding='utf8') as f:
            f.write(json.dumps(self.data, separators=(",", ":")))

    def insert_save(
        self, id: str, date: str, ram: int, cpu: int, disk: int, ports: dict
    ):
        """Insert a new save

        Args:
            id (str): ID of the save
            date (str): Date of the save
            ram (int): RAM usage
            cpu (int): CPU usage
            disk (int): Disk usage
            ports (dict): Open ports
        """
        report = {
            "id": id,
            "date": date,
            "report": {"ram": ram, "cpu": cpu, "disk": disk, "ports": ports},
        }
        self.data = report
        self.save()


class Calls:
    """Calls class
    """
    def request_check():
        """Request a check

        Returns:
            dict: Report
        """
        check()
        last = get_last(SAVE_FOLDER + "/save*.json")
        return {
            "ram": last["report"]["ram"],
            "cpu": last["report"]["cpu"],
            "disk": last["report"]["disk"],
            "ports": last["report"]["ports"],
        }

    def request_reports():
        """Request all reports

        Returns:
            list: List of reports
        """
        files = glob.glob(SAVE_FOLDER + "/save*.json")
        files.sort(key=path.getmtime)
        reports = []
        for file in files:
            with open(file, "r") as f:
                reports.append(json.loads(f.read()))
        return reports

    def request_last():
        """Request the last report

        Returns:
            dict: Last report
        """
        return get_last(SAVE_FOLDER + "/save*.json")

    def request_avg(hours: int):
        """Request the average of the last X hours

        Args:
            hours (int): Number of hours

        Returns:
            dict: Average report
        """
        return get_avg(SAVE_FOLDER + "/save*.json", hours)

    def request_report(id: str):
        """Request a report by ID

        Args:
            id (str): ID of the report

        Returns:
            dict: Report
        """
        files = glob.glob(SAVE_FOLDER + "/save*.json")
        files.sort(key=path.getmtime)
        for file in files:
            with open(file, "r") as f:
                data = json.loads(f.read())
                if data["id"] == id:
                    return data
        return None


def get_level(value: int) -> int:
    """Get the level of the value

    Args:
        value (int): Value to check

    Returns:
        int: Level of the value
    """
    if value > 90:
        return 2
    if value > 80:
        return 1
    return 0


def get_report(monit: Monit, save: Save, config: Config) -> tuple:
    """Get a report

    Args:
        monit (Monit): Monit instance
        save (Save): Save instance
        config (Config): Config instance

    Returns:
        tuple: Report
    """
    ram = monit.checkRam()
    cpu = monit.checkCpu()
    disk = monit.checkDisk()
    ports = {}
    for port in config.get("tcp_ports"):
        ports[port] = monit.checkOpenPort(port)
    return (ram, cpu, disk, ports)


def check():
    """Check the values"""
    now_time = datetime.now().timestamp()
    config = Config("config.json")
    save = Save(
        f'{SAVE_FOLDER}/save{datetime.now().strftime('%d-%m-%Y %H:%M:%S').replace(' ', '-')}.json'
    )
    bot = MonitBot(config)
    report = get_report(Monit(), save, config)
    uuid = hashlib.md5(str(report).encode()).hexdigest()
    save.insert_save(uuid, now_time, report[0], report[1], report[2], report[3])
    ram_level = get_level(report[0])
    if ram_level >= 1:
        bot.alert("RAM au dessus de 80%", ram_level)
    cpu_level = get_level(report[1])
    if cpu_level >= 1:
        bot.alert("CPU au dessus de 80%", cpu_level)
    disk_level = get_level(report[2])
    if disk_level >= 1:
        bot.alert("Disque au dessus de 80%", disk_level)


def get_last(path: str) -> dict:
    """Get the last report

    Args:
        path (str): Path to the reports

    Returns:
        dict: Last report
    """
    files = glob.glob(path)
    if len(files) == 0:
        return {}
    files.sort(key=path.getmtime)
    with open(files[-1], "r") as f:
        return json.loads(f.read())


def get_avg(path: str, hours: int) -> dict:
    """Get the average of the last X hours

    Args:
        path (str): Path to the reports
        hours (int): Number of hours

    Returns:
        dict: Average report
    """
    files = glob.glob(path)
    if len(files) == 0:
        return {}
    files.sort(key=path.getmtime)
    files = files[-hours:]
    avg = {
        "ram": 0,
        "cpu": 0,
        "disk": 0,
    }
    for file in files:
        with open(file, "r", encoding='utf8') as f:
            data = json.loads(f.read())
            avg["ram"] += data["report"]["ram"]
            avg["cpu"] += data["report"]["cpu"]
            avg["disk"] += data["report"]["disk"]
    avg["ram"] /= len(files)
    avg["cpu"] /= len(files)
    avg["disk"] /= len(files)
    avg["ram"] = round(avg["ram"], 2)
    avg["cpu"] = round(avg["cpu"], 2)
    avg["disk"] = round(avg["disk"], 2)
    return avg


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python monit.py <command> <args>")
        print("Commands:")
        for key in cmd.items():
            if isinstance(cmd[key],str):
                print(f"\t{key}: {cmd[key]}")
            else:
                print(f"\t{key}:")
                for key2 in cmd[key]:
                    if isinstance(cmd[key][key2],str):
                        print(f"\t\t{key2}: {cmd[key][key2]}")
                    else:
                        print(f"\t\t{key2}:")
                        for key3 in cmd[key][key2]:
                            print(f"\t\t\t{key3}: {cmd[key][key2][key3]}")
    elif args[0] == "init":
        print("To init the folder, please run the init.sh script")
    elif args[0] == "check":
        check()
    elif args[0] == "list":
        files = glob.glob(SAVE_FOLDER + "/save*.json")
        files.sort(key=path.getmtime)
        for file in files:
            print(file)
    elif args[0] == "get":
        if len(args) == 1:
            print("Usage: python monit.py get <command> <args>")
            print("Commands:")
            for key in cmd["get"]:
                if isinstance(cmd["get"][key],str):
                    print(f'\t{key}: {cmd["get"][key]}')
                else:
                    print(f"\t{key}:")
                    for key2 in cmd["get"][key]:
                        print(f'\t\t{key2}: {cmd["get"][key][key2]}')
        elif args[1] == "last":
            print(get_last(SAVE_FOLDER + "/save*.json"))
        elif args[1] == "avg":
            if len(args) == 2:
                print("Usage: python monit.py get avg <hours>")
            else:
                print(get_avg(SAVE_FOLDER + "/save*.json", int(args[2])))
    else:
        print("Usage: python monit.py <command> <args>")
        print("Commands:")
        for key in cmd.items():
            if isinstance(cmd[key],str):
                print(f"\t{key}: {cmd[key]}")
            else:
                print(f"\t{key}:")
                for key2 in cmd[key]:
                    if isinstance(cmd[key][key2],str):
                        print(f"\t\t{key2}: {cmd[key][key2]}")
                    else:
                        print(f"\t\t{key2}:")
                        for key3 in cmd[key][key2]:
                            print(f"\t\t\t{key3}: {cmd[key][key2][key3]}")
