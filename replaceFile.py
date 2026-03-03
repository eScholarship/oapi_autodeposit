from escholIntf import eschol
from loggingIntf import logger
import csv
import time
print("start")

datafile = "../data/20260127-europmc_failed_pdfs.csv"
def extract_id_and_native_file(csv_path):
    results = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                "id": row["id"],
                "name": row["native_file"]
            })
    return results


def process_all():
    x = eschol()
    y = logger()
    count = 0
    result = extract_id_and_native_file(datafile)
    for row in result:
        count += 1
        if count > 155:
            ark = "ark:/13030/" + row["id"]
            url = y.getArkUrl(ark)
            x.replaceFile(ark, url, row["name"])
            time.sleep(10)
        print(count)


process_all()

print("end")
