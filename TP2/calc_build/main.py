import ast
import socket
import time
import argparse
import os

from src.logs import Logger

import ast

def safe_eval(expression):
    try:
        node = ast.parse(expression, mode='eval')
    except SyntaxError:
        raise ValueError("Invalid expression syntax")
    try:
        return evaluate_node(node.body)
    except ValueError:
        raise ValueError("Invalid expression")

def evaluate_node(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ValueError("Division by zero")
            return left / right
    else:
        raise ValueError("Invalid expression")

def listen(ip, port=13337, timeout=60):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((ip, port))
    s.listen(1)
    s.setblocking(0) 
    logger.info(f"Le serveur tourne sur {ip}:{port}")
    
    start_time = time.time()

    while True:
        try:
            conn, addr = s.accept()
            logger.info(f"Un client {addr} s'est connecté.")

            header = conn.recv(3)
            size = header[:2]
            calc = conn.recv(int.from_bytes(size, 'big'))
            calcul = calc.decode()
            logger.info(f"Calcul reçu du client {addr} : {calcul}")
            try:
                answer = safe_eval(calcul)
                if answer < 0:
                    header = 0
                    answer = abs(answer)
                else:
                    header = 1
            except ValueError or SyntaxError:
                logger.warning(f"Le calcul envoyé par le client {addr} n'est pas valide.")
                answer = -0
                header = 0
            if answer > 4294967295:
                logger.warning(f"Le résultat du calcul dépasse la taille maximale d'un entier non signé sur 32 bits (4294967295).")
                answer = 4294967295
                conn.send(header.to_bytes(1, 'big') + answer.to_bytes(4, 'big'))
            else:
                conn.send(header.to_bytes(1, 'big') + answer.to_bytes(4, 'big'))
                logger.info(f"Réponse envoyée au client {addr} : {answer}")
            
            end = conn.recv(1)
            if end == b'\x00':
                logger.info(f"Le client {addr} a envoyé un message de fin, fermeture de la connexion.")
            else:
                logger.warning(f"Le client {addr} n'a pas envoyé de message de fin / le message de fin n'est pas correct, fermeture de la connexion.")
            conn.close()

            start_time = time.time()
        except socket.error as e:
            if e.errno == 11:
                pass
            else:
                raise

        except KeyboardInterrupt:
            s.close()
            logger.info("Le serveur a été arrêté.")
            exit(0)

        if time.time() - start_time > timeout:
            logger.warning(f"Aucun client depuis plus de {timeout} secondes.")
            start_time = time.time()

def parseArgs():
    parser = argparse.ArgumentParser(description="Serveur de la partie II du TP4")
    parser.add_argument('-p', '--port', type=int, default=13337, help="Port d'écoute du serveur entre 1024 et 65535 (13337 par défaut)")
    return parser.parse_args()

if __name__ == '__main__':
    logger = Logger("logs/bs_server.log")
    args = parseArgs()

    if args.port < 0 or args.port > 65535:

        if args.port < 1024:
            logger.critical("ERROR Le port spécifié est un port privilégié. Spécifiez un port au-dessus de 1024.")
            exit(2)

        else:
            logger.critical("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
            exit(1)
    
    if 'PORT' in os.environ:
        args.port = int(os.environ['PORT'])

    listen('127.0.0.1', args.port, 60)