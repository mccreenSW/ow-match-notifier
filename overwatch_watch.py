import psutil
from scapy.all import sniff, UDP, conf
import requests
import configparser
import os
import sys
import ctypes

# 管理者権限をチェック（パケット監視に必須）
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 1. プロパティ読み込み
config = configparser.ConfigParser()
config_file = 'config.properties'

if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        f.write("[Settings]\nwebhook_url = YOUR_URL_HERE\npacket_threshold = 150")
    print(f"{config_file} を作成しました。設定を記入して再起動してください。")
    input()
    sys.exit()

config.read(config_file)
WEBHOOK_URL = config.get('Settings', 'webhook_url')
THRESHOLD = config.getint('Settings', 'packet_threshold')
PROCESS_NAME = "Overwatch.exe"

conf.L3socket = conf.L3socket
packet_count = 0

def get_overwatch_ports():
    ports = set()
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == PROCESS_NAME:
            try:
                conns = proc.net_connections(kind='udp')
                for conn in conns:
                    ports.add(conn.laddr.port)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
    return ports

def packet_callback(pkt):
    global packet_count
    ow_ports = get_overwatch_ports()
    if pkt.haslayer(UDP) and ow_ports:
        if pkt[UDP].sport in ow_ports or pkt[UDP].dport in ow_ports:
            packet_count += 1
            print(f"OWパケット検知中: {packet_count} / {THRESHOLD}   ", end="\r")

    if packet_count > THRESHOLD:
        print(f"\n📢 マッチング検知！")
        try: requests.post(WEBHOOK_URL, json={"content": "📢 OWマッチング検知！"})
        except: pass
        print("=== 監視停止中（Enterで再開） ===")
        input()
        packet_count = 0

if not is_admin():
    print("エラー: 管理者権限で実行してください。")
    input()
    sys.exit()

print(f"監視開始... (閾値: {THRESHOLD})")
sniff(filter="udp", prn=packet_callback, store=0)