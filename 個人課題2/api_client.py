import requests
import urllib3
import datetime
from config import AREA_URL, FORECAST_URL_TEMPLATE


def format_date(iso_date):
    try:
        dt = datetime.datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return dt.strftime("%m/%d")
    except:
        return "--/--"

def fetch_area_list():
    try:
        res = requests.get(AREA_URL, verify=False)
        res.raise_for_status()
        data = res.json()
        return data.get("offices", {})
    except Exception as e:
        print(f"地域リスト取得エラー: {e}")
        return {}

def fetch_forecast_data(code):
    if code == "014030":
        code = "014100"

    url = FORECAST_URL_TEMPLATE.format(code=code)
    
    try:
        res = requests.get(url, verify=False)
        res.raise_for_status()
        data = res.json()
        weather_report = data[0]['timeSeries'][0]
        temp_report = data[0]['timeSeries'][2] if len(data[0]['timeSeries']) > 2 else None
        date_iso = weather_report['timeDefines'][0]
        date_str = format_date(date_iso)

        results = []

        for i, area in enumerate(weather_report['areas']):
            area_name = area['area']['name']
            weather = area['weathers'][0]
            
            temp_text = "--℃"
            if temp_report and i < len(temp_report['areas']):
                try:
                    temps = temp_report['areas'][i]['temps']
                    if len(temps) >= 2:
                        temp_text = f"{temps[0]}℃ / {temps[1]}℃"
                    elif len(temps) == 1:
                        temp_text = f"{temps[0]}℃"
                except:
                    pass 

            results.append({
                "date": date_str,
                "area_name": area_name,
                "weather": weather,
                "temp": temp_text
            })
            
        return results

    except Exception as e:
        print(f"予報取得エラー: {e}")
        raise e