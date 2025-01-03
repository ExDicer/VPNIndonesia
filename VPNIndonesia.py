import os
import requests
import colorama
from colorama import Fore, Style
import paramiko
import ssl
import socket
import select
import threading
import dns.resolver
import platform

if platform.system() == 'Windows':
    from colorama import init
    init(autoreset=True)

R = Fore.RED
G = Fore.GREEN
C = Fore.CYAN
Z = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
LG = Fore.LIGHTGREEN_EX
W = Fore.RESET

R = '\033[31m'  # merah untuk terminal berbasis Unix
G = '\033[32m'  # hijau
C = '\033[36m'  # cyan
Z = '\133[36m'  # kuning
B = '\033[34m'  # Biru
M = '\033[35m'  # magenta
LG = '\133[32m' # hijau cerah
W = '\033[0m'   # reset warna untuk terminal berbasis Unix

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(G + " " * 30 + "VPN Indonesia" + " " * 30 + '\n')
    print(" " * 30 + 'Bendera' + " " * 35 + W)
    print(R + '[*]' + M + ' Dibuat oleh : ' + W + 'ExDicer')
    print(G + '[+]' + C + ' Keterangan : ' + G + 'Free Internet 200GB')
    print(G + '[+]' + C + ' ' + G + 'Saya mau dong RORR')
    print(B + '[+]' + LG + ' Follow my github :' + Z + 'https://github.com/ExDicer')

def reconnect():
 global reconnect_attempts
 if reconnect_attempts > 0:
   reconnect_attempts -= 1
 print(f"Reconnect attempt {reconnect_attempts}...")

def konfigurasi_vpn_ssh():
 global SSH_HOST, SSH_PORT, USERNAME, PASSWORD, VPN_HOST, VPN_PORT, TLS_VERSION, TLS_INSECURE, DNS_CUSTOM, SEND_BUFFER, RECEIVE_BUFFER, UDPGW_BUFFER_SIZE, UDPGW_PORT, RECONNECT_ATTEMPTS
 
 SSH_HOST = input(G + "Masukkan alamat SSH: " + W)
 SSH_PORT = int(input(G + "Masukkan Port SSH: " + W))
 USERNAME = input(G + "Masukkan username: " + W)
 PASSWORD = input(G + "Masukkan password: " + W)
 HTTP_HOST = input(G + "Masukkan host HTTP: " + W)
 HTTP_PORT = int(input(G + "Masukkan port HTTP: " + W))
 WS_HOST = 'f"ws://{HTTP_HOST}:{HTTP_PORT}/websocket'
 PAYLOAD_SSH = input(G + "Masukkan payload SSH: " + W)
 PAYLOAD_WS = int(input(G + "Masukkan port HTTP: " + W))
 TLS_VERSION = "1.2"
 TLS_INSECURE = input(G + "Aktifkan TLS Insecure (y/n): " + W)
 DNS_CUSTOM = input(G + "Masukkan DNS Custom (pisahkan dengan spasi): " + W).split()
 SEND_BUFFER = int(input(G + "Masukkan ukuran buffer(ex: Netmod): " + W))
 RECEIVE_BUFFER = int(input(G + "Masukkan ukuran buffer: " + W))
 UDPGW_BUFFER_SIZE = int(input(G + "Masukkan ukuran buffer UDPGW: " + W))
 UDPGW_PORT = int(input(G + "Masukkan port UDPGW: " + W))
 RECONNECT_ATTEMPTS = int(input(G + "Masukkan jumlah percobaan reconnect: " + W))

def koneksi_vpn_ssh():
 global ssh_client, ssh_transport, ssh_channel, vpn_socket, ssl_context, dns_resolver, udpgw_socket

 ssh_client = paramiko.SSHClient()
 ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 ssh_client.connect(SSH_HOST, SSH_PORT, USERNAME, PASSWORD)
 ssh_transport = ssh_client.get_transport()
 ssh_channel = ssh_transport.open_session()
 ssh_channel.invoke_shell()

 http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 http_socket.bind((HTTP_HOST, HTTP_PORT))
 http_socket.listen(1)

 ssl_context = ssl.create_default_context()
 ssl_context.check_hostname = False
 ssl_context.verify_mode = ssl.CERT_NONE

 dns_resolver = dns.resolver.Resolver()
 dns_resolver.nameservers = DNS_CUSTOM

 udpgw_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def quick_ping():
 try:
  respon = requests.head("http://" + HTTP_HOST, proxies={"http": f"socks5h://{HTTP_HOST}:{HTTP_PORT}"}, timeout=5)
  print(f"Ping: {respon.status_code}")
 except requests.exceptions.RequestException as e:
  print(f"Ping gagal: {e}")

def reconnect_attempt():
 global reconnect_attempts
 if reconnect_attempts > 0:
  print(f"Reconnect attempt {reconnect_attempts}...")

def http_connection():
    print("VPN Berjalan")
    vpn_socket.listen(1)

def ssh_connection():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(SSH_HOST, SSH_PORT, USERNAME, PASSWORD)
    return ssh_client
    
def websocket_connection():
    ws = websocket.create_connection(WS_HOST)
    return ws
    
def forward_ssh_to_http(ssh_client, ws):
    while True:
        data = ssh_client.recv(1024)
        if data:
            if PAYLOAD_SSH:
                data += PAYLOAD_SSH.encode()
            ws.send(data.decode())

def forward_http_to_ssh(ws, ssh_client):
    while True:
        data = ws.recv()
        if data:
            if PAYLOAD_WS:
                data += PAYLOAD_WS.encode()
            ws.send(data.decode())

def udpgw_connection():
    print("UDPGW Berjalan")
    ssh_channel.invoke_shell()

def udpgw_connection():
    print("SSH Berjalan")
    udpgw_socket.bind((HTTP_HOST, UDPGW_PORT))

def test_ssh():
    print("Menguji SSH...")
    ssh_channel.send("ping 104.22.5.240\n")
    print(ssh_channel.recv(1024).decode())

def pertukaran_kunci_sidik_jari():
    print("Pertukaran kunci sidik jari...")
    ssh_channel.send("echo 'Kunci sidik jari telah ditukar'\n")
    print(ssh_channel.recv(1024).decode)

#def input_manual_payload():
#    payload = input(G + "Masukkan payload manual: " + W)
#    print(F"Payload: {payload}")

def main():
 banner()
 konfigurasi_vpn_ssh()
 koneksi_vpn_ssh()
 ssh_client = ssh_connection()
 ws = websocket_connection()
 quick_ping()
 reconnect_attempt()
 http_connection()
 ssh_connection()
 udpgw_connection()
 test_ssh()
 pertukaran_kunci_sidik_jari()
# input_manual_payload()

if __name__ == "__main__":
 main()

t1 = threading.Thread(target=http_connection).start()
t2 = threading.Thread(target=ssh_connection).start()
t3 = threading.Thread(target=udpgw_connection).start()
t4 = threading.Thread(target=pertukaran_kunci_sidik_jari).start()
t5 = threading.Thread(target=forward_ssh_to_http, args=(ssh_client, ws))
t6 = threading.Thread(target=forward_http_to_ssh, args=(ws, ssh_client))

t5.start()
t6.start()
t5.join()
t6.join()
#input_manual_payload()

print("Konfigurasi HTTP dan SSH berhasil!")
print("Pastikan Anda menguji koneksi secara berkala.")
