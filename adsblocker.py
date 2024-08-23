import os
import subprocess
import sys
import socket
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def read_domains(file_path):
    """Read domains from a file and return a list of non-empty lines."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

# Read domains from the specified file
domains_to_block = read_domains("ListAds.txt")

def display_banner():
    """Display a banner with project information."""
    banner = """
======================================================
    _       _       ____  _            _
   / \   __| |___  | __ )| | ___   ___| | _____ _ __
  / _ \ / _` / __| |  _ \| |/ _ \ / __| |/ / _ \ '__|
 / ___ \ (_| \__ \ | |_) | | (_) | (__|   <  __/ |
/_/   \_\__,_|___/ |____/|_|\___/ \___|_|\_\___|_|

            Telegram: @LordDigital_LD
======================================================
"""
    print(banner)

def ensure_pip():
    """Ensure that pip is available and up-to-date."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--upgrade'])

def install_packages():
    """Ensure that required packages are installed."""
    try:
        import tqdm
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_base_domain(domain):
    """Extract the base domain from a given domain."""
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[-2:])
    return domain

def manage_domain(domain, action, blocked_domains):
    """Manage (block or unblock) a domain based on the specified action."""
    base_domain = get_base_domain(domain)
    if base_domain in blocked_domains:
        return
    
    try:
        ip = socket.gethostbyname(domain)
        cmd_check = ['sudo', 'iptables', '-C', 'OUTPUT', '-d', ip, '-j', 'DROP']
        if action == 'block':
            cmd_add = [
                ['sudo', 'iptables', '-A', 'OUTPUT', '-d', ip, '-j', 'DROP'],
                ['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP']
            ]
        else:  # action == 'unblock'
            cmd_add = [
                ['sudo', 'iptables', '-D', 'OUTPUT', '-d', ip, '-j', 'DROP'],
                ['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP']
            ]

        # Check if the rule already exists
        output = subprocess.run(cmd_check, capture_output=True)
        if (action == 'block' and output.returncode != 0) or (action == 'unblock' and output.returncode == 0):
            for cmd in cmd_add:
                subprocess.run(cmd, capture_output=True)
            blocked_domains.add(base_domain)

    except socket.gaierror:
        pass

def block_unblock_ads(action):
    """Block or unblock ads based on the specified action."""
    clear_screen()
    display_banner()
    blocked_domains = set()
    max_threads = min(50, multiprocessing.cpu_count() * 2)  # Adjusted to 2x CPU count

    start_time = time.time()
    
    with tqdm(total=len(domains_to_block), desc=f"{action.capitalize()}ing domains", ncols=100, ascii=True) as pbar:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {executor.submit(manage_domain, domain, action, blocked_domains): domain for domain in domains_to_block}
            for future in as_completed(futures):
                pbar.update(1)
    
    elapsed_time = time.time() - start_time
    print(f"\nAds have been {action}ed in {elapsed_time:.2f} seconds.")

def menu():
    """نمایش منو و مدیریت ورودی کاربر."""
    actions = {'1': 'block', '2': 'unblock', '3': 'exit'}
    while True:
        clear_screen()
        display_banner()
        print("لطفاً یک گزینه را انتخاب کنید:")
        print("1. بلوکه کردن تبلیغات")
        print("2. باز کردن تبلیغات")
        print("3. خروج")

        try:
            choice = input("انتخاب خود را وارد کنید (1، 2، یا 3): ")
        except EOFError:
            print("\nخطای EOF رخ داده است. در حال خروج...")
            break

        if choice in actions:
            if actions[choice] == 'exit':
                clear_screen()
                print("در حال خروج...")
                break
            else:
                block_unblock_ads(actions[choice])
        else:
            print("انتخاب نامعتبر است، لطفاً 1، 2 یا 3 را انتخاب کنید.")


if __name__ == "__main__":
    ensure_pip()
    install_packages()
    clear_screen()
    menu()
