import csv
from flask import Flask, render_template, request, send_file, redirect
from scrapper import search_diningcode

app = Flask(__name__)

# 수집된 데이터를 임시 저장해둘 전역 데이터베이스 변수
db = {}

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    # 사용자가 검색창에 입력한 키워드 (예: 맛집, 고기, 카페 등)
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 실시간으로 다이닝코드에서 300개 이상의 데이터를 긁어옵니다.
    matzip_results = search_diningcode(keyword)
    
    # 다운로드 기능을 위해 메모리에 저장
    db[keyword] = matzip_results
        
    # 결과 화면 템플릿으로 데이터와 개수 전달
    return render_template(
        "search.html", 
        matzips=enumerate(matzip_results), 
        keyword=keyword, 
        count=len(matzip_results)
    )

@app.route("/download")
def download():
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 메모리에 저장해둔 맛집 데이터가 있으면 가져오고 없으면 새로 크롤링
    if keyword in db:
        matzips = db[keyword]
    else:
        matzips = search_diningcode(keyword)
        db[keyword] = matzips
        
    # 수집한 데이터를 CSV 파일로 저장하는 파이썬 표준 로직
    filename = "./su-seong-matzip.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # CSV 헤더 작성
        writer.writerow(["번호", "식당명", "음식 종류", "상세 주소", "출처"])
        
        # 데이터 행 추가
        for idx, item in enumerate(matzips):
            writer.writerow([idx + 1, item["name"], item["category"], item["address"], item["source"]])
            
    # 완성된 CSV 파일을 사용자 브라우저로 내보내기(다운로드)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)