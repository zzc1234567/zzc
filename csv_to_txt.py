import pandas as pd
import os

output_dir="SpeedTest"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def csv_to_txt(csv_filename,area_name):
    df = pd.read_csv(csv_filename, encoding='utf-8')
    ips = df.iloc[:, 0]
    download_speeds = df.iloc[:, 5]
    output_filename = csv_filename.replace(".csv", ".txt")
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, (ip, speed) in enumerate(zip(ips, download_speeds)):
            f.write(f"{ip}#{area_name} {i+1} ↓ {speed}MB/s\n")

csv_to_txt("HKG.csv","香港")
csv_to_txt("KHH.csv","台湾")
csv_to_txt("SIN.csv","新加坡")
csv_to_txt("NRT.csv","东京")
csv_to_txt("SEA.csv","西雅图")
csv_to_txt("LHR.csv","伦敦")