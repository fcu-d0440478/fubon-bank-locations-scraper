from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrape_fubon_locations():
    url = "https://www.fubon.com/banking/locations/locations.htm?tab=1"

    # 配置 Selenium 瀏覽器
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 無頭模式
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        # 等待頁面完全加載
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Page body loaded successfully.")

        # 輸出網頁源代碼（調試用）
        time.sleep(2)  # 確保動態內容加載完成
        page_source = driver.page_source
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)  # 將 HTML 寫入文件以檢查

        # 將 HTML 傳給 BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # 輸出 BeautifulSoup 的解析結果
        print("Parsed HTML with BeautifulSoup:")
        print(soup.prettify())

        # 查找目標元素 (調試選擇器)
        branch_list = soup.find_all("div", class_="branch-list")
        print(f"Found {len(branch_list)} branch entries.")

        # 提取每個分行的資訊
        branches = []
        for branch in branch_list:
            branch_name = branch.find("h3").text.strip()
            address = branch.find("p", class_="address").text.strip()
            phone = branch.find("p", class_="phone").text.strip()
            print(
                f"Extracted Branch: {branch_name}, Address: {address}, Phone: {phone}"
            )
            branches.append(
                {"Branch Name": branch_name, "Address": address, "Phone": phone}
            )

    finally:
        driver.quit()

    return branches


if __name__ == "__main__":
    branches = scrape_fubon_locations()
    for branch in branches:
        print(branch)
