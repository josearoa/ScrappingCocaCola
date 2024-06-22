#Instala automaticamente el driver de chrome
import json
from webdriver_manager.chrome import ChromeDriverManager
# Driver de selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
# Modifica las opciones de chrome
from selenium.webdriver.chrome.options import Options
# Importa la clase By
from selenium.webdriver.common.by import By

def iniciar_chrome():
    ruta = ChromeDriverManager().install()
    opciones = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    opciones.add_argument(f"user-agent={user_agent}")
    opciones.add_argument("--window-size=1080,1080")
    opciones.add_argument("--disable-web-security")
    opciones.add_argument("--disable-extensions")
    opciones.add_argument("--disable-notifications")
    opciones.add_argument("--ignore-certificate-errors")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--allow-running-insecure-content")
    opciones.add_argument("--no-default-browser-check")
    opciones.add_argument("--no-first-run")
    opciones.add_argument("--no-proxy-server")
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    
    exp_opt=["enable-automation", 
             "ignore-certificate-errors", 
             "enable-logging"]
    opciones.add_experimental_option("excludeSwitches", exp_opt)

    prefs ={"profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": ["es-ES","es"],
            "credentials_enable_service": False}
    
    opciones.add_experimental_option("prefs", prefs)

    s= Service(ruta)
    driver=webdriver.Chrome(service=s, options=opciones)
    return driver

def ScrapJumbo():
    # Inicializar el driver
    driver = iniciar_chrome()
    driver.implicitly_wait(10)
    url = "https://www.jumbo.cl/bebidas-aguas-y-jugos/bebidas-gaseosas?b=coca-cola"
    driver.get(url)
    
    # Esperar a que los productos se carguen
    productos = driver.find_elements(By.CSS_SELECTOR, 'div.product-card-wrap')
    prods = {'productos': []}
    
    print(f"Se encontraron {len(productos)} productos en la página")
    
    for producto in productos:
        try:
            # Obtener el nombre del producto
            nombre = producto.find_element(By.CSS_SELECTOR, 'a.product-card-name').text.strip()
            
            # Obtener el precio del producto
            precio = producto.find_element(By.CSS_SELECTOR, 'span.prices-main-price').text.strip()
            
            # Agregar producto al diccionario
            prods['productos'].append({
                'nombre': nombre,
                'precio': precio,
            })
            print(f"Producto encontrado: {nombre} - {precio}")
        except Exception as e:
            print(f"Error al procesar producto: {e}")
            continue
    
    # Guardar los productos en un archivo JSON
    with open('bebidas-jumbo.json', 'w', encoding='utf8') as outfile:
        json.dump(prods, outfile, indent=4, ensure_ascii=False)
    
    print(f'Se obtuvieron {len(prods["productos"])} productos')
    
    driver.quit()

# Llamar a la función para realizar el scraping
ScrapJumbo()