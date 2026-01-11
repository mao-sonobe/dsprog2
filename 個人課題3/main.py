import flet as ft
import config
import api_client
import ui_components
import database 

def main(page: ft.Page):
    page.title = "Weather App (DB Version)"
    page.padding = 0
    page.bgcolor = config.BG_COLOR
    page.theme_mode = ft.ThemeMode.LIGHT
    
    database.init_db()
    
    header_text = ft.Text("地域を選択してください", size=24, weight="bold", color=config.THEME_COLOR)
    grid = ft.GridView(expand=True, runs_count=5, max_extent=180, spacing=15, run_spacing=15)
    pref_list = ft.ListView(expand=True, spacing=0)

    def on_area_click(e):
        code = e.control.data['code']
        name = e.control.data['name']
        
        header_text.value = f"{name}の天気予報"
        grid.controls.clear()
        grid.controls.append(ft.Container(content=ft.ProgressRing(color=config.THEME_COLOR), alignment=ft.alignment.center))
        page.update()
        
        database.save_area(code, name)
        
        try:
            api_data = api_client.fetch_forecast_data(code)
            
            database.save_forecasts(code, api_data)
            
            db_data = database.get_forecasts_by_area(code)
            
            grid.controls.clear()
            for item in db_data:
                temp_display = item["min"]
                if item["max"]:
                    temp_display += f" / {item['max']}"

                card = ui_components.AreaWeatherCard(
                    date_text=item["date"],
                    area_name=name, 
                    weather_text=item["weather"],
                    temp_text=temp_display
                )
                grid.controls.append(card)
                
        except Exception as err:
            grid.controls.clear()
            grid.controls.append(ft.Text(f"エラー: {err}", color="red"))
            print(err)
            
        page.update()

    offices = api_client.fetch_area_list()
    if offices:
        for code, info in offices.items():
            pref_list.controls.append(
                ft.ListTile(
                    title=ft.Text(info['name'], size=14),
                    data={'code': code, 'name': info['name']},
                    on_click=on_area_click,
                    hover_color="white",
                )
            )
    else:
        pref_list.controls.append(ft.Text("地域リスト読込失敗"))

    sidebar = ft.Container(
        width=250, bgcolor=config.SIDEBAR_COLOR,
        content=ft.Column([
            ft.Container(content=ft.Text("地域選択", weight="bold", size=16, color="grey800"), padding=20),
            ft.Divider(height=1, color="grey300"),
            pref_list
        ])
    )
    
    main_content = ft.Container(
        expand=True, padding=30,
        content=ft.Column([header_text, ft.Divider(height=20, color="transparent"), grid])
    )

    page.add(ft.Row(controls=[sidebar, main_content], expand=True, spacing=0))

if __name__ == "__main__":
    ft.app(target=main)