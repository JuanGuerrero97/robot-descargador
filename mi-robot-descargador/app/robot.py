# 🤖 Robot OFAC Mejorado - Múltiples estrategias automáticas

import requests
import datetime
import os
import time
from bs4 import BeautifulSoup
import urllib.parse
import random

class RobotOFACMejorado:
    def __init__(self):
        print("🤖 ¡Robot OFAC Mejorado iniciado!")
        os.makedirs('data', exist_ok=True)
        
        # URLs múltiples de OFAC para intentar
        self.ofac_urls = [
            "https://www.treasury.gov/ofac/downloads/sdn.xml",
            "https://sanctionslist.ofac.treas.gov/api/PublicationPreview/exports/SDN_ENHANCED.XML",
            "https://www.treasury.gov/ofac/downloads/sdn_enhanced.xml",
            "https://sanctionslist.ofac.treas.gov/api/PublicationPreview/exports/sdn.xml"
        ]
        
        # Headers múltiples para rotar
        self.headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/xml,text/xml,*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Referer': 'https://sanctionslist.ofac.treas.gov/'
            }
        ]
    
    def download_with_retry(self, url, headers, max_retries=3):
        """Descarga con reintentos y backoff exponencial"""
        for attempt in range(max_retries):
            try:
                wait_time = random.uniform(2, 8) + (attempt * 3)  # 2-8 segundos + incremento
                print(f"⏳ Esperando {wait_time:.1f} segundos antes del intento {attempt + 1}")
                time.sleep(wait_time)
                
                print(f"📥 Intento {attempt + 1}: Descargando desde {url}")
                
                response = requests.get(url, headers=headers, timeout=60, stream=True)
                
                print(f"📊 Status code: {response.status_code}")
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    print("❌ Error 403 - Acceso denegado")
                    continue
                elif response.status_code == 429:
                    print("⚠️ Error 429 - Rate limit, esperando más tiempo...")
                    time.sleep(30)  # Esperar 30 segundos en rate limit
                    continue
                else:
                    print(f"⚠️ Error {response.status_code}")
                    continue
                    
            except requests.exceptions.Timeout:
                print("⏰ Timeout - reintentando...")
                continue
            except requests.exceptions.RequestException as e:
                print(f"❌ Error de conexión: {e}")
                continue
        
        return None
    
    def descargar_ofac_multiple_estrategias(self):
        """Prueba múltiples URLs y headers para OFAC"""
        print("\n🚀 === ESTRATEGIA MÚLTIPLE PARA OFAC ===")
        
        for i, url in enumerate(self.ofac_urls):
            print(f"\n🔍 Probando URL {i+1}/{len(self.ofac_urls)}: {url}")
            
            # Rotar headers
            headers = self.headers_list[i % len(self.headers_list)]
            
            response = self.download_with_retry(url, headers)
            
            if response:
                return self.save_ofac_file(response)
            else:
                print(f"❌ Falló URL {i+1}")
                continue
        
        print("❌ Todas las URLs de OFAC fallaron")
        return False
    
    def save_ofac_file(self, response):
        """Guarda el archivo OFAC descargado"""
        try:
            # Verificar que sea XML
            content_type = response.headers.get('content-type', '').lower()
            print(f"📄 Tipo de contenido: {content_type}")
            
            # Generar nombre de archivo
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ofac_sdn_enhanced.xml"
            filepath = os.path.join('data', filename)
            
            # Guardar archivo
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verificar descarga
            if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:  # Al menos 10KB
                size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
                print(f"✅ OFAC descargado exitosamente: {filename} ({size_mb} MB)")
                
                # Crear enlace fácil
                latest_file = os.path.join('data', 'ofac_latest.xml')
                if os.path.exists(latest_file):
                    os.remove(latest_file)
                
                import shutil
                shutil.copy2(filepath, latest_file)
                print(f"🔗 Creado enlace: ofac_latest.xml")
                
                return True
            else:
                print(f"❌ Archivo muy pequeño o vacío")
                return False
                
        except Exception as e:
            print(f"❌ Error guardando archivo OFAC: {e}")
            return False
    
    def descargar_onu_mejorado(self):
        """Descarga ONU con estrategia mejorada"""
        print("\n🔍 === DESCARGANDO ONU (MEJORADO) ===")
        
        onu_urls = [
            "https://scsanctions.un.org/resources/xml/en/consolidated.xml",
            "https://scsanctions.un.org/resources/xml/sp/consolidated.xml"
        ]
        
        for url in onu_urls:
            print(f"🔍 Probando ONU: {url}")
            
            headers = random.choice(self.headers_list)
            response = self.download_with_retry(url, headers, max_retries=2)
            
            if response:
                return self.save_onu_file(response)
        
        return False
    
    def save_onu_file(self, response):
        """Guarda archivo ONU"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"onu_consolidated.xml"
            filepath = os.path.join('data', filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
                print(f"✅ ONU descargado: {filename} ({size_mb} MB)")
                
                # Crear enlace fácil
                latest_file = os.path.join('data', 'onu_latest.xml')
                if os.path.exists(latest_file):
                    os.remove(latest_file)
                
                import shutil
                shutil.copy2(filepath, latest_file)
                print(f"🔗 Creado enlace: onu_latest.xml")
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error guardando ONU: {e}")
            return False
    
    def ejecutar_descarga_completa(self):
        """Ejecuta descarga completa con estrategias mejoradas"""
        print("🚀 ¡ROBOT MEJORADO - INICIANDO DESCARGA AUTOMÁTICA!")
        print("=" * 60)
        
        resultados = {}
        
        # Descargar OFAC con múltiples estrategias
        print("🇺🇸 Descargando OFAC...")
        resultados['ofac'] = self.descargar_ofac_multiple_estrategias()
        
        # Pausa entre descargas
        print("\n⏳ Pausa de 10 segundos entre descargas...")
        time.sleep(10)
        
        # Descargar ONU
        print("🇺🇳 Descargando ONU...")
        resultados['onu'] = self.descargar_onu_mejorado()
        
        # Resumen final
        self.mostrar_resumen(resultados)
        return resultados
    
    def mostrar_resumen(self, resultados):
        """Muestra resumen final"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL:")
        
        for fuente, exito in resultados.items():
            emoji = "✅" if exito else "❌"
            nombre = "OFAC - Specially Designated Nationals" if fuente == 'ofac' else "ONU - Lista Consolidada"
            print(f"  {emoji} {fuente.upper()}: {nombre}")
        
        exitosas = sum(resultados.values())
        total = len(resultados)
        
        print(f"\n🎯 Total: {exitosas}/{total} listas descargadas")
        
        if exitosas == total:
            print("🎉 ¡TODAS las listas se descargaron exitosamente!")
        elif exitosas > 0:
            print("⚠️ Descarga parcial - algunas listas exitosas")
        else:
            print("❌ No se pudo descargar ninguna lista")
        
        # Mostrar archivos
        self.mostrar_archivos()
    
    def mostrar_archivos(self):
        """Muestra archivos descargados"""
        print("\n📁 ARCHIVOS DISPONIBLES:")
        print("=" * 50)
        
        if os.path.exists('data'):
            archivos = [f for f in os.listdir('data') if f.endswith('.xml')]
            if archivos:
                for archivo in sorted(archivos):
                    ruta = os.path.join('data', archivo)
                    size_mb = round(os.path.getsize(ruta) / (1024 * 1024), 2)
                    print(f"📄 {archivo} ({size_mb} MB)")
            else:
                print("🤷 No hay archivos XML")
        else:
            print("❌ Carpeta data no existe")

# 🚀 EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    print("🌟 Robot OFAC Mejorado - Descarga Automática 100%")
    print("🔄 Usando múltiples estrategias anti-bloqueo...")
    print()
    
    robot = RobotOFACMejorado()
    robot.ejecutar_descarga_completa()
    
    print("\n🎉 ¡Proceso completado!")
    print("💤 Robot entrando en modo de espera...")
    print("🔄 Próxima ejecución automática según programación")
