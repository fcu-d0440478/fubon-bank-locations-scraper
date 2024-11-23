import requests
from bs4 import BeautifulSoup
import html
import pandas as pd

# 發送請求獲取 XML 資料
url = "https://www.fubon.com/Fubon_Portal/banking/locations/biBranch.jsp?type=branch&zoned=0&zonedKind=0"
response = requests.get(url)

# 使用 BeautifulSoup 解析 XML
soup = BeautifulSoup(response.text, "xml")

# 提取所有分行信息
branches = []
for item in soup.find_all("item"):
    branch = {
        "SNO": item.find("sno").text if item.find("sno") else None,
        "Name": html.unescape(item.find("title").text) if item.find("title") else None,
        "English Name": item.find("title_en").text if item.find("title_en") else None,
        "Type": item.find("type").text if item.find("type") else None,
        "New Branch": item.find("new").text if item.find("new") else None,
        "City": html.unescape(item.find("zoned").text) if item.find("zoned") else None,
        "District": (
            html.unescape(item.find("zoned_kind").text)
            if item.find("zoned_kind")
            else None
        ),
        "Address": (
            html.unescape(item.find("address").text) if item.find("address") else None
        ),
        "English Address": (
            item.find("address_en").text if item.find("address_en") else None
        ),
        "Latitude": item.find("latitude").text if item.find("latitude") else None,
        "Longitude": item.find("longitude").text if item.find("longitude") else None,
        "Phone": html.unescape(item.find("phone").text) if item.find("phone") else None,
    }
    branches.append(branch)

# 構建數據列表
data = []
for branch in branches:
    name = branch.get("Name", "N/A")
    address = branch.get("Address", "N/A")
    latitude = branch.get("Latitude", "N/A")
    longitude = branch.get("Longitude", "N/A")

    # 經緯度格式化為 [Latitude, Longitude]
    coordinates = f"[{latitude}, {longitude}]"

    # 添加到數據列表
    data.append({"銀行分部": name, "位置": address, "經緯度": coordinates})

# 創建 DataFrame
df = pd.DataFrame(data)

# 顯示 DataFrame
print(df)
