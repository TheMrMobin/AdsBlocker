import os
import subprocess
import sys
import socket
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
#t.me/LordDigital_LD
def read_domains(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        sys.exit(1)
#t.me/LordDigital_LD
domains_to_block = read_domains("ListAds.txt")
#t.me/LordDigital_LD
def display_banner():
    banner = """
======================================================
    _       _       ____  _            _
   / \   __| |___  | __ )| | ___   ___| | _____ _ __
  / _ \ / _` / __| |  _ \| |/ _ \ / __| |/ / _ \ '__|
 / ___ \ (_| \__ \ | |_) | | (_) | (__|   <  __/ |
/_/   \_\__,_|___/ |____/|_|\___/ \___|_|\_\___|_|

            Telegram: @LordDigitdl_LD
======================================================
"""
    print(banner)
#t.me/LordDigital_LD
def ensure_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--upgrade'])#t.me/LordDigital_LD
#t.me/LordDigital_LD
def install_packages():
    try:
        import tqdm
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])#t.me/LordDigital_LD
#t.me/LordDigital_LD
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#t.me/LordDigital_LD
def get_base_domain(domain):
    parts = domain.split('.')#t.me/LordDigital_LD
    if len(parts) > 2:
        return '.'.join(parts[-2:])#t.me/LordDigital_LD
    return domain
#t.me/LordDigital_LD
def manage_domain(domain, action, blocked_domains):
    base_domain = get_base_domain(domain)
    if base_domain in blocked_domains:
        return
    
    try:
        ip = socket.gethostbyname(domain)
        if action == 'block':
            cmd_check = ['sudo', 'iptables', '-C', 'OUTPUT', '-d', ip, '-j', 'DROP']
            cmd_add = [['sudo', 'iptables', '-A', 'OUTPUT', '-d', ip, '-j', 'DROP'],
                       ['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP']]
        else:
            cmd_check = ['sudo', 'iptables', '-C', 'OUTPUT', '-d', ip, '-j', 'DROP']
            cmd_add = [['sudo', 'iptables', '-D', 'OUTPUT', '-d', ip, '-j', 'DROP'],
                       ['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP']]

        output = subprocess.run(cmd_check, capture_output=True)
        if (action == 'block' and output.returncode != 0) or (action == 'unblock' and output.returncode == 0):
            for cmd in cmd_add:
                subprocess.run(cmd, capture_output=True)
            blocked_domains.add(base_domain)

    except socket.gaierror:
        pass
#t.me/LordDigital_LD
def block_unblock_ads(action):
    clear_screen()
    display_banner()
    blocked_domains = set()
    max_threads = min(50, multiprocessing.cpu_count() * 10)#t.me/LordDigital_LD
    start_time = time.time()
    
    with tqdm(total=len(domains_to_block), desc=f"{action.capitalize()}ing domains", ncols=100, ascii=True) as pbar:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {executor.submit(manage_domain, domain, action, blocked_domains): domain for domain in domains_to_block}
            for future in as_completed(futures):
                pbar.update(1)
    
    elapsed_time = time.time() - start_time
    print(f"\nAds have been {action}ed in {elapsed_time:.2f} seconds.")
#t.me/LordDigital_LD
def menu():
    actions = {'1': 'block', '2': 'unblock', '3': 'exit'}
    while True:
        clear_screen()
        display_banner()
        print("Please choose an option:")
        print("1. Block Ads")
        print("2. Unblock Ads")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice in actions:
            if actions[choice] == 'exit':
                clear_screen()
                print("Exiting...")
                break
            else:
                block_unblock_ads(actions[choice])
        else:
            print("Invalid choice, please select 1, 2, or 3.")
#t.me/LordDigital_LD
if __name__ == "__main__":
    ensure_pip()
    install_packages()
    clear_screen()
    menu()
