from bs4 import BeautifulSoup

# Load the provided HTML content
html_file = "debug_page_source.html"  # 替換成你的 HTML 檔案路徑
with open(html_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all branch information containers
branch_sections = soup.find_all("div", class_="sub sub--location")

branches = []
for section in branch_sections:
    # Extract branch name
    name = (
        section.find("a", class_="bank-info").text.strip()
        if section.find("a", class_="bank-info")
        else "N/A"
    )

    # Extract address
    address = (
        section.find("a", class_="icon--location-pin btn--pin").text.strip()
        if section.find("a", class_="icon--location-pin btn--pin")
        else "N/A"
    )

    # Extract phone number from 'onclick' attribute
    phone = "N/A"
    location_link = section.find("a", class_="icon--location-pin btn--pin")
    if location_link and "onclick" in location_link.attrs:
        onclick_content = location_link.attrs["onclick"]
        # Extract phone number from the onclick string (if present)
        phone_start = onclick_content.find(",'") + 2
        phone_end = onclick_content.find("'", phone_start)
        phone = onclick_content[phone_start:phone_end]

    # Append to the branches list
    branches.append({"Branch Name": name, "Address": address, "Phone": phone})

# Print the extracted information
for branch in branches:
    print(branch)
