import os
import requests
from bs4 import BeautifulSoup
import time

# 저장할 디렉토리 설정
output_dir = "downloaded_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# HTTP 요청 헤더
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# 기본 URL 템플릿
base_url = "https://hornygrail.com/new/{}"

# 시작 페이지와 끝 페이지 입력받기
start_page = int(input("Enter the start page number: "))
end_page = int(input("Enter the end page number: "))

# 페이지 순회하며 이미지 다운로드
for page in range(start_page, end_page + 1):
    print(f"Processing page {page}...")
    target_url = base_url.format(page)

    # 페이지 요청
    response = requests.get(target_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # 이미지 카드 검색
        cards = soup.find_all("div", class_="card")  # 수정: 사이트 구조에 따라 변경 필요
        print(f"Found {len(cards)} cards on page {page}.")

        for card in cards:
            # 카테고리와 제목 추출
            category_tag = card.find("div", class_="card-body__info tag")
            title_tag = card.find("div", class_="card-body__line")

            category = category_tag.text.strip() if category_tag else "Uncategorized"
            title = title_tag.text.strip() if title_tag else "Untitled"

            # 불법 문자 제거 및 파일명 생성
            sanitized_category = "".join(c if c.isalnum() or c in " _-" else "_" for c in category)
            sanitized_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
            file_name = f"{sanitized_category}.{sanitized_title}.jpg"

            # 저장 경로 설정
            file_path = os.path.join(output_dir, file_name)

            # 이미지 URL 추출
            img_tag = card.find("img")
            img_url = img_tag.get("src") if img_tag else None
            if not img_url:
                continue

            # 절대 URL로 변환
            if not img_url.startswith("http"):
                img_url = requests.compat.urljoin(target_url, img_url)

            # 이미지 다운로드
            try:
                if os.path.exists(file_path):
                    print(f"File already exists: {file_path}")
                    continue

                img_data = requests.get(img_url).content
                with open(file_path, "wb") as img_file:
                    img_file.write(img_data)
                print(f"Downloaded: {file_path}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

        # 요청 간 대기 (크롤링 방지)
        time.sleep(1)
    else:
        print(f"Failed to access {target_url}: Status code {response.status_code}")

print("Download complete.")
