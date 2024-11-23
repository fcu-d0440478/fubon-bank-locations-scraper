from bs4 import BeautifulSoup

# Load HTML content
html_file = "debug_page_source.html"  # 替換成你的 HTML 檔案路徑
with open(html_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find all branch sections
branch_sections = soup.find_all("div", class_="sub sub--location")

branches = []
for section in branch_sections:
    # Extract branch name and use it as the ID
    name = (
        section.find("a", class_="bank-info").text.strip()
        if section.find("a", class_="bank-info")
        else None
    )
    if not name:
        # Skip if branch name is not available
        # print("Skipping branch without name:", section.prettify())
        continue

    # Extract address
    address = (
        section.find("a", class_="icon--location-pin btn--pin").text.strip()
        if section.find("a", class_="icon--location-pin btn--pin")
        else "N/A"
    )

    # Extract latitude and longitude from 'onclick' attribute
    lat, lon = "N/A", "N/A"
    location_link = section.find("a", class_="icon--location-pin btn--pin")
    if location_link and "onclick" in location_link.attrs:
        onclick_content = location_link.attrs["onclick"]
        try:
            # Parse latitude and longitude
            lat_start = onclick_content.index("(") + 1
            lat_end = onclick_content.index(",", lat_start)
            lon_start = lat_end + 1
            lon_end = onclick_content.index(",", lon_start)
            lat = onclick_content[lat_start:lat_end].strip().replace('"', "")
            lon = onclick_content[lon_start:lon_end].strip().replace('"', "")
        except ValueError:
            print("Error parsing latitude/longitude for:", name)

    # Append valid branches
    branches.append(
        {"Branch Name": name, "Address": address, "Latitude": lat, "Longitude": lon}
    )

# Print valid branch information
for branch in branches:
    print(branch)
