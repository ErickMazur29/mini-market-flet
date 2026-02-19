import flet as ft

def card_padrao_login(): 
    card_style = { 
        "bgcolor": ft.Colors.WHITE, 
        "padding": 40, 
        "width": 400, 
        "border_radius": 20, 
        "shadow": ft.BoxShadow( 
            blur_radius=15, 
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK), 
            offset=ft.Offset(0, 5), ), 
    }
    return card_style

def card_padrao_home():
    card_style = { 
        "bgcolor": ft.Colors.WHITE, 
        "padding": 30, 
        "width": 500, 
        "height": 700, 
        "border_radius": 20, 
        "shadow": ft.BoxShadow( 
            blur_radius=15, 
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK), 
            offset=ft.Offset(0, 5), ), 
    }
    return card_style
    

def style_product_list(content):
    return ft.Container(
        content = content,
        width = 400,
        height = 300,
        padding = 10,                
        margin = ft.Margin.only(top = 10, bottom = 10),  
        bgcolor = ft.Colors.GREY_100, 
        border_radius = 12,
        border = ft.Border.all(1, ft.Colors.GREY_300), 
    )

def style_cart_list (content):
    return ft.Container(
        content = content,
        width = 400,
        height = 300,
        padding = 10,
        border_radius = 12,
        bgcolor = ft.Colors.GREY_100, 
        border = ft.Border.all(1, ft.Colors.GREY_300)
    )


def list_text(content, data, color,on_click):
    return ft.Container(
        content = content,
        padding = 10,  
        border_radius = 8,
        bgcolor = color,
        data = data,
        on_click=on_click
    )
    


    
