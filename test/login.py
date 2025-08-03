from utils.session import cargar_contexto_con_cookies

if __name__ == "__main__":
    playwright, browser, page = cargar_contexto_con_cookies()

    print("✅ Login (o carga de cookie) completado correctamente")
    input("Presiona ENTER para cerrar el navegador...")
    browser.close()
    playwright.stop()
