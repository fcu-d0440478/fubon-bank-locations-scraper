# 直接指定XML接口，所以不用selenium操作，會直接獲取所有元素的清單XML

import requests  # 用於發送 HTTP 請求
from bs4 import BeautifulSoup  # 用於解析 HTML/XML 資料
import html  # 用於處理 HTML 實體
import pandas as pd  # 用於數據處理和表格操作

# 發送請求獲取 XML 資料
# URL 指向的是 XML 接口，提供分行相關信息
url = "https://www.fubon.com/Fubon_Portal/banking/locations/branch.jsp?type=branch&zoned=0&zonedKind=0"
response = requests.get(url)  # 發送 GET 請求，獲取返回的 XML

# 使用 BeautifulSoup 解析 XML
# "xml" 解析器專門用於處理 XML 結構
soup = BeautifulSoup(response.text, "xml")

# 提取所有分行信息，將每個 <item> 節點中的數據存入列表
branches = []
for item in soup.find_all("item"):  # 遍歷所有 <item> 標籤
    branch = {
        # 使用 find 方法查找子標籤，如果找不到返回 None
        "SNO": item.find("sno").text if item.find("sno") else None,  # 分行代碼
        "Name": (
            html.unescape(item.find("title").text.strip())
            if item.find("title")
            else None
        ),  # 中文名稱
        "English Name": (
            item.find("titleEN").text if item.find("titleEN") else None
        ),  # 英文名稱
        "Type": item.find("type").text if item.find("type") else None,  # 分行類型
        "New Branch": (
            item.find("new").text if item.find("new") else None
        ),  # 是否為新分行
        "City": (
            html.unescape(item.find("zoned").text) if item.find("zoned") else None
        ),  # 城市名稱
        "District": (
            html.unescape(item.find("zoned_kind").text)
            if item.find("zoned_kind")
            else None
        ),  # 行政區域
        "Address": (
            html.unescape(item.find("address").text.strip())
            if item.find("address")
            else None
        ),  # 中文地址
        "English Address": (
            item.find("address_en").text if item.find("address_en") else None
        ),  # 英文地址
        "Latitude": (
            item.find("latitude").text if item.find("latitude") else None
        ),  # 緯度
        "Longitude": (
            item.find("longitude").text if item.find("longitude") else None
        ),  # 經度
        "Phone": item.find("phone").text if item.find("phone") else None,  # 聯絡電話
    }
    branches.append(branch)  # 將分行數據添加到列表中

# 構建數據列表
# 將分行數據進一步處理，準備轉為 DataFrame 格式
data = []
for branch in branches:
    name = branch.get("Name", "N/A")  # 取分行名稱，默認值為 "N/A"
    address = branch.get("Address", "N/A")  # 取地址
    latitude = branch.get("Latitude", "N/A")  # 取緯度
    longitude = branch.get("Longitude", "N/A")  # 取經度

    # 經緯度格式化為 [Latitude, Longitude]，便於處理地理位置
    coordinates = [latitude, longitude]

    # 將每個分行的信息添加到數據列表
    data.append({"銀行分部": name, "位置": address, "經緯度": coordinates})

# 使用 Pandas 將數據轉為 DataFrame
df = pd.DataFrame(data)

# 顯示前 50 行數據，也就是前5頁
print(df.head(50))  # 使用 head 方法顯示前 50 行
df[:50].to_csv("data/branches_data_xml.csv", index=False, encoding="utf-8")
