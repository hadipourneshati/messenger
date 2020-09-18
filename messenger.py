import conf
import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from threading import Thread

def key_generation():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = key.private_bytes(serialization.Encoding.PEM,
                                    serialization.PrivateFormat.PKCS8,
                                    serialization.NoEncryption())
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH,
                                               serialization.PublicFormat.OpenSSH)
    with open("private_key", "wb") as private_key_file:
        private_key_file.write(private_key)
    with open("public_key", "wb") as public_key_file:
        public_key_file.write(public_key)


def receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((conf.receiver_ip, conf.receiver_port))
    sock.listen(10)
    while True:
        conn, addr = sock.accept()
        while conn:
            data = conn.recv(1024).decode("ascii")
            if data:
                print(data)

def sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((conf.sender_ip, conf.sender_port))
    while True:
        txt = input()
        sock.send(str(txt).encode())