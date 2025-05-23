import random
import ipaddress
import requests
import subprocess

url = "https://www.cloudflare-cn.com/ips-v4"
ip_count = 50

cidr_list = requests.get(url).text.strip().splitlines()
all_ips = [str(ip) for cidr in cidr_list for ip in ipaddress.ip_network(cidr, strict=False).hosts()]
random.shuffle(all_ips)

def is_ping_ok(ip):
    # Linux: -c 1 发送1个包，-W 1 超时1秒
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
    return result.returncode == 0

alive_ips = []
used_ips = set()
i = 0

while len(alive_ips) < ip_count:
    if i >= len(all_ips):
        # 如果所有IP都检测过了还不够，重新洗牌再来
        random.shuffle(all_ips)
        i = 0
    ip = all_ips[i]
    if ip in used_ips:
        i += 1
        continue
    used_ips.add(ip)
    if is_ping_ok(ip):
        alive_ips.append(ip)
    i += 1

with open("randomIP.txt", "w") as file:
    file.write("\n".join(alive_ips))
