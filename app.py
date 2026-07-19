from flask import Flask, render_template, request, Response # 1. 필요한 모듈 임포트
from scrapper import fetch_apt_trade
import csv
import io

# 2. app 변수를 반드시 먼저 정의해야 합니다! (이 줄이 @app.route보다 위에 있어야 함)
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    DEAL_YMD = request.args.get("DEAL_YMD")
    LAWD_CD = request.args.get("LAWD_CD")
    print(DEAL_YMD, LAWD_CD)
    results = fetch_apt_trade(LAWD_CD, DEAL_YMD)
    return render_template("search.html", results=results)

# 3. app이 정의된 상태이므로 이제 @app.route를 정상적으로 사용할 수 있습니다.
@app.route("/download")
def download():
    DEAL_YMD = request.args.get("DEAL_YMD")
    LAWD_CD = request.args.get("LAWD_CD")
    
    results = fetch_apt_trade(LAWD_CD, DEAL_YMD)
    
    si = io.StringIO()
    cw = csv.writer(si)
    
    cw.writerow(['아파트이름', '실거래정보(만원)', '지역(법정동)', '거래일', '전용면적(㎡)'])
    
    for r in results:
        cw.writerow([
            r.get("aptNm", ""),
            r.get("dealAmount", ""),
            r.get("umdNm", ""),
            f"{r.get('dealYear', '')}년 {r.get('dealMonth', '')}월 {r.get('dealDay', '')}일",
            r.get("excluUseAr", "")
        ])
        
    output = si.getvalue()
    
    return Response(
        output.encode('utf-8-sig'),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=apt_trade_{LAWD_CD}_{DEAL_YMD}.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)