import flet as ft
from view import render_auth_form

def main(page: ft.Page):
    page.title = "Gerador de Currículo"
    render_auth_form(page)

ft.app(target=main)
