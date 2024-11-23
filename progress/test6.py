from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 初始化 WebDriver 並設置無沙盒模式
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
# options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# 打開目標頁面
driver.get("https://www.fubon.com/banking/locations/locations.htm?tab=1")

# 等待頁面加載完成
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "normalPagination"))
)

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

# 存儲分行數據的列表
branches = []

# 最大頁數
max_pages = 5
current_page = 1

while current_page <= max_pages:
    try:
        # 等待當前頁面內容加載
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sub--location"))
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
                # 使用字符串分割提取經緯度
                latitude, longitude = None, None
                if "changeMapContent" in onclick_attr:
                    parts = onclick_attr.split(",")
                    latitude = parts[0].split("(")[-1].strip('"')
                    longitude = parts[1].strip('"')

                # 添加到數據列表
                branches.append(
                    {"分行名稱": name, "地址": address, "經緯度": [latitude, longitude]}
                )
            except Exception as e:
                print(f"提取數據時出錯：{e}")

        # 嘗試點擊下一頁
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "next"))
        )
        next_button.click()
        current_page += 1

        # 等待頁面更新
        WebDriverWait(driver, 10).until(EC.staleness_of(locations[0]))

    except Exception as e:
        print(f"頁面加載或翻頁失敗：{e}")
        break

# 關閉瀏覽器
driver.quit()

# 將數據轉換為 DataFrame
df = pd.DataFrame(branches)

# 顯示前 50 行數據
print(df.head(50))

# 保存數據到 CSV 文件
df.to_csv("branches_data_5_pages.csv", index=False, encoding="utf-8")
