import pandas as pd

csv_files = [
    "HKG.csv",
    "KHH.csv",
    "SIN.csv",
    "NRT.csv",
    "SEA.csv",
]

area_names = [
    "香港",
    "台湾",
    "新加坡",
    "东京",
    "西雅图",
]

def csv_to_txt(csv_files, area_names, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        for csv_file, area in zip(csv_files, area_names):
            df = pd.read_csv(csv_file, encoding='utf-8')
            for i, (ip, speed) in enumerate(zip(df.iloc[:, 0], df.iloc[:, 5]), start=1):
                f.write(f"{ip}#{area} {i}\n")

csv_to_txt(csv_files, area_names, "AutoTest.txt")
