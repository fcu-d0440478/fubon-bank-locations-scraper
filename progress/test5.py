from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 初始化 Selenium WebDriver
driver = webdriver.Chrome()  # 確保已安裝 ChromeDriver
driver.get("https://www.fubon.com/banking/locations/locations.htm?tab=1")

# 等待頁面加載完成
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
)

# 存儲分行數據的列表
branches = []

# 找到分頁按鈕
pagination = driver.find_element(By.CLASS_NAME, "pagination")
pages = pagination.find_elements(By.CLASS_NAME, "page")  # 所有頁碼按鈕

# 遍歷每個頁碼，模擬點擊並提取數據
for page in pages:
    try:
        # 等待頁面內容更新
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "normal"))
        )

        # 提取當前頁面的分行數據
        locations = driver.find_elements(By.CLASS_NAME, "sub--location")
        for location in locations:
            try:
                # 提取分行名稱
                name = location.find_element(By.CLASS_NAME, "bank-info").text

                # 提取地址
                address = location.find_element(By.CLASS_NAME, "btn--pin").text

                # 提取經緯度
                onclick_attr = location.find_element(
                    By.CLASS_NAME, "btn--pin"
                ).get_attribute("onclick")
                latitude, longitude = None, None
                if "changeMapContent" in onclick_attr:
                    parts = onclick_attr.split(",")
                    latitude = parts[0].split("(")[-1].strip('"')
                    longitude = parts[1].strip('"')

                # 添加到數據列表
                branches.append(
                    {"分行名稱": name, "地址": address, "經緯度": [latitude, longitude]}
                )

                # 點擊當前頁碼
                page.click()

            except Exception as e:
                print(f"提取數據時出錯：{e}")

    except Exception as e:
        print(f"頁碼點擊失敗：{e}")
        continue

# 關閉瀏覽器
driver.quit()

# 將數據轉換為 DataFrame
df = pd.DataFrame(branches)

# 顯示前 10 行數據
print(df.head(10))

# 保存數據到 CSV 文件
df.to_csv("branches_data.csv", index=False, encoding="utf-8")
