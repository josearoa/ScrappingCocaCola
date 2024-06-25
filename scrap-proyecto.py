## Proyecto de Web Scraping (Coca-Cola) - Lenguaje y Paradigmas de Programación
# Integrantes: José Aguilera e Isadora Ahumada

# Para la correcta ejecución del script, se deben instalar las siguientes librerías:
# pip install selenium webdriver-manager pandas matplotlib seaborn json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import json

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

##### Paradigma Procedural #####
# Se centra en el uso de funciones y procedimientos para llevar a cabo tareas específicas.

# Modularidad
# Simplicidad y claridad

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
    opciones.add_argument("--disable-infobars")
    
    exp_opt=["enable-automation", 
             "ignore-certificate-errors", 
             "enable-logging"]
    opciones.add_experimental_option("excludeSwitches", exp_opt)

    prefs ={"profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": ["es-ES","es"],
            "credentials_enable_service": False}
    
    opciones.add_experimental_option("prefs", prefs)

    s = Service(ruta)

    driver = webdriver.Chrome(service=s, options=opciones)
    return driver

def ScrapJumbo():
    driver = iniciar_chrome()
    driver.implicitly_wait(10)
    url = "https://www.jumbo.cl/bebidas-aguas-y-jugos/bebidas-gaseosas?b=coca-cola"
    driver.get(url)
    
    productos = driver.find_elements(By.CSS_SELECTOR, 'div.product-card-wrap')
    prods = []
    
    for producto in productos:
        try:
            nombre = producto.find_element(By.CSS_SELECTOR, 'a.product-card-name').text.strip()
            precio = producto.find_element(By.CSS_SELECTOR, 'span.prices-main-price').text.strip()
            prods.append({'nombre': nombre, 'precio': precio})
        except Exception as e:
            continue
    
    driver.quit()
    return prods

def ScrapAcuenta():
    driver = iniciar_chrome()
    driver.implicitly_wait(10)
    url = "https://acuenta.cl/ca/bebidas-y-licores/02?brands=Coca-Cola"
    driver.get(url)
    
    productos = driver.find_elements(By.CSS_SELECTOR, 'div.product-card-default')
    prods = []
    
    for producto in productos:
        try:
            nombre = producto.find_element(By.CSS_SELECTOR, 'p.prod__name').text.strip()
            precio = producto.find_element(By.CSS_SELECTOR, 'p.base__price').text.strip()
            prods.append({'nombre': nombre, 'precio': precio})
        except Exception as e:
            continue
    
    driver.quit()
    return prods

jumbo_data = ScrapJumbo()
acuenta_data = ScrapAcuenta()

# Guardar datos en JSON
with open('bebidas-jumbo.json', 'w', encoding='utf8') as outfile:
    json.dump(jumbo_data, outfile, indent=4, ensure_ascii=False)

with open('bebidas-acuenta.json', 'w', encoding='utf8') as outfile:
    json.dump(acuenta_data, outfile, indent=4, ensure_ascii=False)

###### Paradigma Orientado a Objetos ######
# Organiza el código en torno a objetos, que son instancias de clases que encapsulan datos y comportamientos relacionados.

# Encapsulamiento
# Manejo de complejidad

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        return f"Producto(nombre={self.nombre}, precio={self.precio})"

class Supermercado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def cargar_datos(self, data):
        for item in data:
            producto = Producto(item['nombre'], item['precio'])
            self.agregar_producto(producto)

    # Guardamos los datos de los productos de un supermercado en un archivo JSON
    def guardar_datos(self, archivo):
        with open(archivo, 'w', encoding='utf8') as outfile:
            json.dump([producto.__dict__ for producto in self.productos], outfile, indent=4, ensure_ascii=False)

    def __repr__(self):
        return f"Supermercado(nombre={self.nombre}, productos={self.productos})"

# Cargar los datos desde JSON, creando instancias de la clase Supermercado y cargando esos datos en dichas instancias.

with open('bebidas-jumbo.json', 'r', encoding='utf8') as infile:
    jumbo_data = json.load(infile)

with open('bebidas-acuenta.json', 'r', encoding='utf8') as infile:
    acuenta_data = json.load(infile)

jumbo = Supermercado('Jumbo')
jumbo.cargar_datos(jumbo_data)

acuenta = Supermercado('Acuenta')
acuenta.cargar_datos(acuenta_data)

###### Paradigma Funcional ######
# Se centra en el uso de funciones puras y la evitación de estados mutables.

# Inmutabilidad
# Facilidad de pruebas

def crear_dataframe(supermercado):
    data = {'nombre': [], 'precio': [], 'supermercado': []}
    for producto in supermercado.productos:
        data['nombre'].append(producto.nombre)
        data['precio'].append(float(producto.precio.replace('$', '').replace('.', '')))
        data['supermercado'].append(supermercado.nombre)
    return pd.DataFrame(data)

df_jumbo = crear_dataframe(jumbo)
df_acuenta = crear_dataframe(acuenta)

df = pd.concat([df_jumbo, df_acuenta])

# Análisis comparativo
plt.figure(figsize=(12, 6))
sns.boxplot(x='supermercado', y='precio', data=df)
plt.title('Comparación de Precios de Bebidas Azucaradas de Coca Cola entre Jumbo y Acuenta')
plt.xlabel('Supermercado')
plt.ylabel('Precio ($)')
plt.show()

# Histograma de distribución de precios
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='precio', hue='supermercado', element='step', kde=True)
plt.title('Distribución de Precios de Bebidas Azucaradas en Jumbo y Acuenta')
plt.xlabel('Precio ($)')
plt.ylabel('Frecuencia')
plt.show()

# Agrupar por nombre del producto y supermercado para calcular el precio promedio
precio_promedio = df.groupby(['nombre', 'supermercado'])['precio'].mean().unstack()

# Visualización de precios promedio
plt.figure(figsize=(14, 7))
precio_promedio.plot(kind='bar')
plt.title('Precio Promedio de Bebidas Azucaradas por Supermercado')
plt.ylabel('Precio Promedio ($)')
plt.xlabel('Producto')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Supermercado')
plt.tight_layout()
plt.show()

# Estadísticas descriptivas
print(df.groupby('supermercado')['precio'].describe())
