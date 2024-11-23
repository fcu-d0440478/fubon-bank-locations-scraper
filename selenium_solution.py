from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 初始化 WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# 打開目標頁面
driver.get("https://www.fubon.com/banking/locations/locations.htm?tab=1")

# 存儲分行數據的列表
branches = []


# 點擊 "同意" 按鈕
try:
    # 等待按鈕出現
    agree_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "mCookieBtn"))
    )
    agree_button.click()
    print("成功點擊 '同意' 按鈕")
except Exception as e:
    print(f"點擊 '同意' 按鈕失敗：{e}")

try:
    for page in range(5):  # 假設需要提取前 5 頁
        # 提取當前頁面的數據
        locations = driver.find_elements(By.CLASS_NAME, "sub--location")
        for location in locations:
            try:
                name = location.find_element(By.CLASS_NAME, "bank-info").text
                address = location.find_element(By.CLASS_NAME, "location-addr").text
                onclick_attr = location.find_element(
                    By.CLASS_NAME, "btn--pin"
                ).get_attribute("onclick")
                latitude, longitude = None, None
                if "changeMapContent" in onclick_attr:
                    parts = onclick_attr.split(",")
                    latitude = parts[0].split("(")[-1].strip('"')
                    longitude = parts[1].strip('"')
                branches.append(
                    {"銀行分部": name, "位置": address, "經緯度": [latitude, longitude]}
                )
            except Exception as e:
                print(f"提取數據時出錯：{e}")

        # 點擊下一頁按鈕
        if page < 4:  # 避免在最後一頁嘗試點擊下一頁
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next"))
            )
            next_button.click()

            # 等待新頁面的內容加載
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sub--location"))
            )

except Exception as e:
    print(f"提取數據失敗：{e}")

# 關閉瀏覽器
driver.quit()

# 保存數據到 DataFrame
df = pd.DataFrame(branches)
print(df)
df.to_csv("data/branches_data_selenium.csv", index=False, encoding="utf-8")
