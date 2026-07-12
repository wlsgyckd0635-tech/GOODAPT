# make_csv.py
import csv
import random

# 대흥동(알파시티) 및 시지 지역 대표 동네와 음식 종류
areas = ["대구 수성구 대흥동(알파시티)", "대구 수성구 신매동(시지)", "대구 수성구 매호동", "대구 수성구 욱수동"]
categories = ["한식", "중식", "일식/일식당", "양식/레스토랑", "카페/디저트", "고기구이", "분식"]

food_names = {
    "한식": ["시지 정식한상", "알파시티 백반집", "대흥동 집밥", "고산 시골밥상", "매호 뚝배기", "수성 보리밥"],
    "중식": ["알파반점", "시지 대반점", "대흥성", "시지 짬뽕전문점", "짜장천국", "수성 마라탕"],
    "일식/일식당": ["시지초밥", "알파시티 돈카츠", "대흥동 규동", "시지 라멘야", "고산 연어덮밥"],
    "양식/레스토랑": ["알파시티 파스타", "시지 스테이크 하우스", "대흥 피자리아", "수성 뇨끼 맛집"],
    "카페/디저트": ["스마트시티 카페", "알파시티 에스프레소 바", "시지 베이커리", "매호 감성카페", "욱수동 디저트랩"],
    "고기구이": ["시지 삼겹살", "알파시티 한우", "대흥동 돼지갈비", "고산 막창", "매호 뒷고기"],
    "분식": ["시지 떡볶이", "알파시티 김밥", "대흥동 수제튀김", "고산 라면", "매호 순대"]
}

# 350개의 고유한 맛집 데이터 생성
print("350개 맛집 데이터 생성 중...")
with open('matzip_db.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 헤더 작성 (다이닝코드 스타일 반영)
    writer.writerow(["식당명", "카테고리", "주소", "대표메뉴", "다이닝코드평점", "리뷰수"])
    
    for i in range(1, 351):
        cat = random.choice(categories)
        base_name = random.choice(food_names[cat])
        name = f"{base_name} {i}호점"
        addr = f"{random.choice(areas)} {random.randint(1, 500)}번지"
        menu = f"추천 {cat} 메뉴 A"
        score = round(random.uniform(3.5, 4.9), 1)
        review = random.randint(5, 180)
        
        writer.writerow([name, cat, addr, menu, score, review])

print("✅ matzip_db.csv 파일 생성 완료 (350개 데이터 확보!)")