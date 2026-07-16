import requests 
import xml.etree.ElementTree as ET

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

SERVICE_KEY = os.getenv("SERVICE_KEY")
print()


def fetch_apt_trade(LAWD_CD, DEAL_YMD):
    # LAWD_CD="27260"
    # DEAL_YMD="202606"
    serviceKey=SERVICE_KEY
    URL='https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade'

    params={
        "serviceKey": serviceKey,
        "LAWD_CD": LAWD_CD, 
        "DEAL_YMD": DEAL_YMD,
        "numOfRows": 30   # 추가된 값   << 공공데이터 설정하지 않을경우 기본값 10개정도만 출력됨
    }

    response = requests.get(URL, params=params)
    # print(response.content)
    root = ET.fromstring(response.content)

    items = root.findall("./body/items/item")

    results = []
    for item in items:
        row = {}
        for child in item:
            row[child.tag] = child.text
        
        results.append(row)

        results.sort(key=lambda x: (int(x.get("dealYear", 0)), int(x.get("dealMonth", 0)), int(x.get("dealDay", 0))))

    return results
