import flet as ft

def calculate_total(cart_items):
    total = 0
    for item in cart_items:
        total = total + item["price"]
    return total

