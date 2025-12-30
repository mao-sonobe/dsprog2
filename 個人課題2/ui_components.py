import flet as ft
from config import CARD_COLOR

def get_weather_style(weather_text):
    text = weather_text or ""
    if "晴" in text: return "wb_sunny", "orange"
    if "雨" in text: return "umbrella", "blue"
    if "雪" in text: return "ac_unit", "cyan"
    if "曇" in text: return "wb_cloudy", "grey"
    return "wb_cloudy_outlined", "blueGrey"

class AreaWeatherCard(ft.Container):
    def __init__(self, date_text, area_name, weather_text, temp_text):
        super().__init__()
        icon_name, icon_color = get_weather_style(weather_text)
        
        self.bgcolor = CARD_COLOR
        self.border_radius = 12
        self.padding = 15
        self.width = 160
        self.height = 200
        self.border = ft.border.all(1, "grey300")
        
        self.content = ft.Column(
            controls=[
                ft.Text(date_text, size=14, color="grey"),
                ft.Text(area_name, weight="bold", size=16, color="grey800", text_align="center", no_wrap=True, overflow="ellipsis"),
                ft.Divider(height=5, color="transparent"),
                ft.Icon(name=icon_name, color=icon_color, size=48),
                ft.Text(weather_text, size=12, color="grey600", text_align="center", max_lines=2, overflow="ellipsis"),
                ft.Divider(height=5, color="transparent"),
                ft.Text(temp_text, weight="bold", size=14, color="blueGrey800"),
            ],
            horizontal_alignment="center",
            alignment="center",
            spacing=2
        )