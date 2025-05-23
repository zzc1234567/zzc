import random
import ipaddress
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://www.cloudflare-cn.com/ips-v4"
ip_count = 50

cidr_list = requests.get(url).text.strip().splitlines()
all_ips = [str(ip) for cidr in cidr_list for ip in ipaddress.ip_network(cidr, strict=False).hosts()]
random.shuffle(all_ips)

def is_ping_ok(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

alive_ips = set()
checked_ips = set()
batch_size = 50  # 每批检测50个IP，可根据机器性能调整

while len(alive_ips) < ip_count:
    candidates = [ip for ip in all_ips if ip not in checked_ips]
    if not candidates:
        # 所有IP都检测过了还不够，重新洗牌再来
        checked_ips.clear()
        random.shuffle(all_ips)
        candidates = all_ips
    batch = candidates[:batch_size]
    with ThreadPoolExecutor(max_workers=16) as executor:
        future_to_ip = {executor.submit(is_ping_ok, ip): ip for ip in batch}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            checked_ips.add(ip)
            if future.result():
                alive_ips.add(ip)
            if len(alive_ips) >= ip_count:
                break

with open("randomIP.txt", "w") as file:
    file.write("\n".join(list(alive_ips)[:ip_count]))
