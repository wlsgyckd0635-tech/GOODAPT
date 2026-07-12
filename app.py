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
    # 사용자가 검색창에 입력한 키워드 (예: 수성구, 푸르지오, 84㎡ 등)
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 실시간으로 부동산 매물 데이터셋 300개 이상을 필터링하여 가져옵니다.
    apt_results = search_diningcode(keyword)
    
    # 다운로드 기능을 위해 메모리에 저장
    db[keyword] = apt_results
        
    # 결과 화면 템플릿(search.html)으로 데이터와 개수 전달
    return render_template(
        "search.html", 
        matzips=enumerate(apt_results), 
        keyword=keyword, 
        count=len(apt_results)
    )

@app.route("/download")
def download():
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 메모리에 저장해둔 부동산 데이터가 있으면 가져오고 없으면 새로 갱신
    if keyword in db:
        apt_data = db[keyword]
    else:
        apt_data = search_diningcode(keyword)
        db[keyword] = apt_data
        
    # 수집한 데이터를 부동산 포맷의 CSV 파일로 저장
    filename = "./daegu-apt-data.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # CSV 파일의 상단 헤더(컬럼명) 설정
        writer.writerow(["번호", "아파트 단지명(동)", "공급/전용 면적", "소재지", "매물 호가"])
        
        # 데이터 행 추가
        for idx, item in enumerate(apt_data):
            writer.writerow([
                idx + 1, 
                item["name"], 
                item["category"], 
                item["address"], 
                item.get("price", "N/A")
            ])
            
    # 완성된 CSV 파일을 브라우저를 통해 즉시 다운로드 처리
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)