import requests
from win10toast import ToastNotifier
from time import sleep
from datetime import datetime

id = int(input("ID of item: "))
threshold = int(input("Threshold of price (notify when it goes under this value): "))
interval = int(input("Refresh interval (seconds): "))

while True:
    body = {"items": [{"itemType": "Asset", "id": id}]}
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://catalog.roblox.com/v1/catalog/items/details", json=body, headers=headers)
    if response.status_code == 403:
        headers["X-CSRF-TOKEN"] = response.headers["x-csrf-token"]
        response = requests.post("https://catalog.roblox.com/v1/catalog/items/details", json=body, headers=headers)
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"Requesting item {id} at {date_time}")
    print(response.json())
    details = response.json()["data"][0]
    print()
    if details["lowestResalePrice"] <= threshold or details["lowestPrice"] <= threshold:
        print(f"Item {id} found at lowestResalePrice:{details["lowestResalePrice"]}, lowestPrice:{details["lowestPrice"]}")
        toast = ToastNotifier()
        toast.show_toast(
            "Robux Notifier",
            f"Item {id} found at lowestResalePrice:{details["lowestResalePrice"]}, lowestPrice:{details["lowestPrice"]}",
            duration = 10,
            threaded = True)
    sleep(interval)
