 이 코드는 특정 웹사이트의 여러 페이지에서 이미지를 다운로드하고, 파일 이름을 "카테고리.제목.jpg" 형식으로 저장하는 프로그램입니다.

1. 디렉토리 준비
python
output_dir = "downloaded_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir

목적: 이미지를 저장할 디렉토리를 생성합니다.
output_dir는 저장할 기본 디렉토리 경로입니다.
os.makedirs(output_dir)는 디렉토리가 존재하지 않을 경우 생성합니다.

2. HTTP 요청 헤더 설정
python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
목적: 서버와의 요청에서 브라우저처럼 보이도록 하기 위해 요청 헤더를 설정합니다.
웹사이트는 브라우저가 아닌 프로그램(크롤러)으로부터의 요청을 차단할 수 있으므로 User-Agent를 설정합니다.

3. URL 템플릿과 사용자 입력 처리
python
base_url = "https://hornygrail.com/new/{}"
start_page = int(input("Enter the start page number: "))
end_page = int(input("Enter the end page number: "))
base_url: 특정 웹사이트의 페이지 URL을 구성하는 템플릿입니다. {}는 페이지 번호가 삽입될 위치입니다.
start_page, end_page: 사용자가 크롤링할 시작 페이지와 끝 페이지 번호를 입력합니다.
예를 들어, 시작 페이지가 1, 끝 페이지가 3이면 페이지 1, 2, 3을 순회합니다.

4. 페이지 순회
python
for page in range(start_page, end_page + 1):
    print(f"Processing page {page}...")
    target_url = base_url.format(page)
목적: 시작 페이지부터 끝 페이지까지 순회하며 각각의 페이지 URL을 생성합니다.
base_url.format(page): 템플릿의 {}에 페이지 번호를 삽입하여 요청할 URL을 생성합니다.

5. 웹 페이지 HTML 가져오기
python
response = requests.get(target_url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
requests.get(target_url, headers=headers): 지정한 URL로 HTTP 요청을 보냅니다.
response.status_code: 응답 상태 코드를 확인합니다.
상태 코드가 200이면 요청 성공을 의미합니다.
BeautifulSoup(response.text, "html.parser"): HTML을 파싱하여 DOM 구조로 변환합니다. 이를 통해 HTML 요소에 쉽게 접근할 수 있습니다.

6. 이미지 카드 요소 찾기
python
cards = soup.find_all("div", class_="card")
print(f"Found {len(cards)} cards on page {page}.")
soup.find_all("div", class_="card"): HTML에서 div 태그 중 클래스 이름이 card인 모든 요소를 찾습니다.
이 부분은 사이트의 구조에 따라 수정이 필요할 수 있습니다.

7. 카테고리와 제목 추출
python
category_tag = card.find("div", class_="card-body__info tag")
title_tag = card.find("div", class_="card-body__line")

category = category_tag.text.strip() if category_tag else "Uncategorized"
title = title_tag.text.strip() if title_tag else "Untitled"
카테고리 추출:
card.find("div", class_="card-body__info tag"): 이미지 카드에서 카테고리를 나타내는 요소를 찾습니다.
.text.strip(): 텍스트만 추출하고 양쪽 공백을 제거합니다.
else "Uncategorized": 카테고리가 없을 경우 기본값을 설정합니다.
제목 추출: 동일한 방식으로 제목을 추출합니다.

8. 파일 이름 생성
python
sanitized_category = "".join(c if c.isalnum() or c in " _-" else "_" for c in category)
sanitized_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
file_name = f"{sanitized_category}.{sanitized_title}.jpg"
목적: 파일 이름에 포함될 카테고리와 제목에서 불법 문자를 제거합니다.
isalnum(): 문자와 숫자만 허용합니다.
" _-": 공백, 언더스코어(_), 하이픈(-)은 허용합니다.
file_name: 최종 파일 이름은 카테고리.제목.jpg 형식으로 생성됩니다.

9. 이미지 URL 추출 및 다운로드
python
img_tag = card.find("img")
img_url = img_tag.get("src") if img_tag else None
if not img_url:
    continue

if not img_url.startswith("http"):
    img_url = requests.compat.urljoin(target_url, img_url)
이미지 URL 추출: 카드에서 <img> 태그를 찾고, src 속성에서 이미지 URL을 가져옵니다.
절대 URL 변환: 이미지 URL이 상대 경로일 경우, requests.compat.urljoin을 사용하여 절대 경로로 변환합니다.

10. 이미지 저장
python
file_path = os.path.join(output_dir, file_name)
if os.path.exists(file_path):
    print(f"File already exists: {file_path}")
    continue

img_data = requests.get(img_url).content
with open(file_path, "wb") as img_file:
    img_file.write(img_data)
print(f"Downloaded: {file_path}")
저장 경로: 파일 이름과 저장 디렉토리를 결합하여 이미지의 최종 경로를 생성합니다.
중복 확인: 파일이 이미 존재할 경우 다운로드를 건너뜁니다.
이미지 다운로드:
requests.get(img_url).content: 이미지 데이터를 가져옵니다.
with open(file_path, "wb"): 바이너리 모드로 파일을 열고 데이터를 저장합니다.

11. 대기 시간
python
time.sleep(1)
목적: 크롤링 방지를 위해 요청 간에 1초의 대기 시간을 추가합니다.
필요에 따라 더 길게 설정하거나 랜덤한 대기 시간을 줄 수 있습니다.

12. 완료 메시지
python
print("Download complete.")
모든 페이지의 처리가 완료되면 완료 메시지를 출력합니다.

프로그램 흐름 요약
사용자에게 시작 페이지와 끝 페이지를 입력받습니다.
각 페이지의 URL에 접근하여 HTML을 파싱합니다.
카드 요소를 순회하며 카테고리, 제목, 이미지 URL을 추출합니다.
이미지를 다운로드하고, 카테고리와 제목을 조합한 파일 이름으로 저장합니다.
모든 작업이 끝나면 완료 메시지를 출력합니다.

장점
파일 이름에 카테고리와 제목을 포함해 정리가 쉽습니다.
불법 문자를 제거해 저장 시 오류를 방지합니다.
중복 파일을 건너뛰고 예외 처리가 포함되어 안정성이 높습니다.
추가 질문이나 개선 요청이 있다면 말씀해주세요! 😊
