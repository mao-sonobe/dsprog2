import flet as ft
import config
import api_client
import ui_components

def main(page: ft.Page):
    page.title = "Weather App"
    page.padding = 0
    page.bgcolor = config.BG_COLOR
    page.theme_mode = ft.ThemeMode.LIGHT
    
    header_text = ft.Text("地域を選択してください", size=24, weight="bold", color=config.THEME_COLOR)
    
    grid = ft.GridView(
        expand=True, 
        runs_count=5, 
        max_extent=180, 
        spacing=15, 
        run_spacing=15
    )
    
    pref_list = ft.ListView(expand=True, spacing=0)

    def on_area_click(e):
        code = e.control.data['code']
        name = e.control.data['name']
        
        header_text.value = f"{name}の天気予報"
        grid.controls.clear()
        grid.controls.append(ft.Container(
            content=ft.ProgressRing(color=config.THEME_COLOR), 
            alignment=ft.alignment.center
        ))
        page.update()
        
        try:
            forecast_data_list = api_client.fetch_forecast_data(code)
            grid.controls.clear()
            for item in forecast_data_list:
                card = ui_components.AreaWeatherCard(
                    date_text=item["date"],
                    area_name=item["area_name"],
                    weather_text=item["weather"],
                    temp_text=item["temp"]
                )
                grid.controls.append(card)
                
        except Exception as err:
            grid.controls.clear()
            grid.controls.append(ft.Text(f"エラーが発生しました: {err}", color="red"))
            
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
        pref_list.controls.append(ft.Text("地域リストの読み込みに失敗しました"))

    sidebar = ft.Container(
        width=250,
        bgcolor=config.SIDEBAR_COLOR,
        content=ft.Column([
            ft.Container(
                content=ft.Text("地域選択", weight="bold", size=16, color="grey800"),
                padding=20
            ),
            ft.Divider(height=1, color="grey300"),
            pref_list
        ])
    )
    
    main_content = ft.Container(
        expand=True,
        padding=30,
        content=ft.Column([
            header_text, 
            ft.Divider(height=20, color="transparent"), 
            grid
        ])
    )

    page.add(
        ft.Row(
            controls=[sidebar, main_content], 
            expand=True, 
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main)