import random
import ipaddress
import requests
import subprocess

url = "https://www.cloudflare-cn.com/ips-v4"
ip_count = 50

cidr_list = requests.get(url).text.strip().splitlines()
all_ips = [str(ip) for cidr in cidr_list for ip in ipaddress.ip_network(cidr, strict=False).hosts()]
random_ips = random.sample(all_ips, ip_count)

def is_ping_ok(ip):
    # Linux: -c 1 发送1个包，-W 1 超时1秒
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
    return result.returncode == 0

alive_ips = [ip for ip in random_ips if is_ping_ok(ip)]

with open("randomIP.txt", "w") as file:
    file.write("\n".join(alive_ips))