import sqlite3
from config import DB_NAME

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    sql_areas = """
    CREATE TABLE IF NOT EXISTS areas (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    
    sql_forecasts = """
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_code TEXT,
        date TEXT,
        weather TEXT,
        weather_code TEXT,
        min_temp TEXT,
        max_temp TEXT,
        UNIQUE(area_code, date)
    );
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql_areas)
    cursor.execute(sql_forecasts)
    conn.commit()
    conn.close()

def save_area(code, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO areas (code, name) VALUES (?, ?)",
        (code, name)
    )
    conn.commit()
    conn.close()

def save_forecasts(area_code, forecast_list):
    conn = get_connection()
    cursor = conn.cursor()
    
    for f in forecast_list:
        cursor.execute("""
            INSERT OR REPLACE INTO forecasts 
            (area_code, date, weather, weather_code, min_temp, max_temp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            area_code,
            f["date"],
            f["weather"],
            f["code"],  
            f["min"],
            f["max"]
        ))
    
    conn.commit()
    conn.close()

def get_forecasts_by_area(area_code):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM forecasts WHERE area_code = ? ORDER BY id", 
        (area_code,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "date": row["date"],
            "weather": row["weather"],
            "code": row["weather_code"],
            "min": row["min_temp"],
            "max": row["max_temp"]
        })
    return results