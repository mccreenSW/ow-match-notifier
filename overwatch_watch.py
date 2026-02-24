import psutil
from scapy.all import sniff, UDP, conf
import requests
import configparser
import os
import sys
import ctypes
import threading
import time
from collections import deque

# --- グローバル変数 ---
ow_ports = set()          # Overwatchが使用中のポート一覧
packet_times = deque()    # 受信したパケットのタイムスタンプを保存
PROCESS_NAME = "Overwatch.exe"
is_monitoring = True      # 監視状態のフラグ

# --- 設定関連 ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

config = configparser.ConfigParser()
config_file = 'config.properties'

if not os.path.exists(config_file):
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("[Settings]\nwebhook_url = YOUR_URL_HERE\npacket_threshold = 150\ntime_window = 1.0\n")
    print(f"{config_file} を作成しました。設定を記入して再起動してください。")
    input()
    sys.exit()

config.read(config_file, encoding='utf-8')
WEBHOOK_URL = config.get('Settings', 'webhook_url')
THRESHOLD = config.getint('Settings', 'packet_threshold')
# 新規追加: 何秒間の間にパケットが閾値を超えたら検知するうか (デフォルト1.0秒)
TIME_WINDOW = config.getfloat('Settings', 'time_window', fallback=1.0) 

conf.L3socket = conf.L3socket

# --- バックグラウンド処理: 定期的なポート取得 ---
def update_overwatch_ports():
    """別スレッドで実行: 2秒ごとにOverwatchのポート情報を更新する（CPU負荷を劇的に下げる）"""
    global ow_ports
    while True:
        if is_monitoring:
            new_ports = set()
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == PROCESS_NAME:
                    try:
                        # UDPコネクションのみを取得
                        conns = proc.net_connections(kind='udp')
                        for conn in conns:
                            if conn.laddr:
                                new_ports.add(conn.laddr.port)
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
            ow_ports = new_ports
        time.sleep(2) # 2秒ごとに更新

# --- パケット解析処理 ---
def packet_callback(pkt):
    global packet_times, is_monitoring
    
    # 監視一時停止中、またはポートが取得できていない場合は無視 (O(1)の高速判定)
    if not is_monitoring or not ow_ports:
        return

    if pkt.haslayer(UDP):
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
        
        # OWのポートと一致するか判定
        if sport in ow_ports or dport in ow_ports:
            now = time.time()
            packet_times.append(now)

            # 指定した時間枠(TIME_WINDOW)より古いパケット履歴を削除
            while packet_times and now - packet_times[0] > TIME_WINDOW:
                packet_times.popleft()

            current_count = len(packet_times)
            print(f"OWパケット検知中 [過去{TIME_WINDOW}秒]: {current_count} / {THRESHOLD}   ", end="\r")

            # 閾値を超えた場合の処理
            if current_count >= THRESHOLD:
                is_monitoring = False # バックグラウンドのポート更新も一時停止
                print(f"\n📢 マッチング検知！")
                try:
                    requests.post(WEBHOOK_URL, json={"content": "📢 OWマッチング検知！"})
                except Exception as e:
                    print(f"Discord通知エラー: {e}")
                
                print("=== 監視停止中（Enterで再開） ===")
                # input() はブロック処理なので検知を一時停止できる
                input() 
                
                # 再開処理
                packet_times.clear()
                print("監視を再開しました...")
                is_monitoring = True

# --- メイン処理 ---
if __name__ == "__main__":
    if not is_admin():
        print("エラー: 管理者権限で実行してください。")
        input()
        sys.exit()

    print(f"監視開始... (条件: {TIME_WINDOW}秒間に {THRESHOLD} パケット)")
    
    # ポート監視スレッドの起動 (デーモン化してメイン終了と共に終了させる)
    port_thread = threading.Thread(target=update_overwatch_ports, daemon=True)
    port_thread.start()

    # パケット監視の開始
    sniff(filter="udp", prn=packet_callback, store=0)