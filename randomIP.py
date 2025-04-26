import random
import ipaddress
import requests

url = "https://www.cloudflare-cn.com/ips-v4"
ip_count = 15

cidr_list = requests.get(url).text.strip().splitlines()

all_ips = [str(ip) for cidr in cidr_list for ip in ipaddress.ip_network(cidr, strict=False).hosts()]
random_ips = random.sample(all_ips, ip_count)

with open("randomIP.txt", "w") as file:
    file.write("\n".join(random_ips))