# 🤖 Robot Descargador de Listas REALES OFAC/ONU
# ¡Este robot descarga las listas oficiales!

import requests
import datetime
import os
import time
from bs4 import BeautifulSoup
import urllib.parse

class RobotDescargadorReal:
    def __init__(self):
        print("🤖 ¡Hola! Soy tu robot descargador de listas REALES")
        print("📁 Voy a crear la carpeta 'data' si no existe")
        os.makedirs('data', exist_ok=True)
        
        # URLs de las páginas oficiales
        self.sources = {
            'ofac': {
                'page_url': 'https://sanctionslist.ofac.treas.gov/Home/SdnList',
                'target_file': 'SDN_ENHANCED.XML',
                'description': 'Lista OFAC - Specially Designated Nationals'
            },
            'onu': {
                'page_url': 'https://main.un.org/securitycouncil/es/content/un-sc-consolidated-list',
                'xml_button': 'Xml',
                'description': 'Lista Consolidada ONU - Consejo de Seguridad'
            }
        }
    
    def get_ofac_download_url(self):
        """Encuentra la URL real del archivo SDN_ENHANCED.XML"""
        try:
            print("🔍 Buscando enlace de descarga de OFAC...")
            
            response = requests.get(self.sources['ofac']['page_url'], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar enlaces que contengan SDN_ENHANCED.XML
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if 'SDN_ENHANCED.XML' in href or 'sdn_enhanced.xml' in href.lower():
                    if href.startswith('http'):
                        print(f"✅ Encontré enlace OFAC: {href}")
                        return href
                    else:
                        # URL relativa, construir URL completa
                        base_url = 'https://sanctionslist.ofac.treas.gov'
                        full_url = urllib.parse.urljoin(base_url, href)
                        print(f"✅ Encontré enlace OFAC: {full_url}")
                        return full_url
            
            # Si no encontramos el enlace, usar URL conocida
            fallback_url = "https://sanctionslist.ofac.treas.gov/api/PublicationPreview/exports/SDN_ENHANCED.XML"
            print(f"⚠️ No encontré enlace específico, usando URL conocida: {fallback_url}")
            return fallback_url
            
        except Exception as e:
            print(f"❌ Error buscando enlace OFAC: {e}")
            # URL de respaldo
            return "https://sanctionslist.ofac.treas.gov/api/PublicationPreview/exports/SDN_ENHANCED.XML"
    
    def get_onu_download_url(self):
        """Encuentra la URL real del XML de la ONU"""
        try:
            print("🔍 Buscando enlace de descarga de ONU...")
            
            response = requests.get(self.sources['onu']['page_url'], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar botón o enlace XML
            for element in soup.find_all(['a', 'button'], href=True):
                text = element.get_text().strip().lower()
                href = element.get('href', '')
                
                if 'xml' in text and ('consolidat' in text.lower() or 'lista' in text.lower()):
                    if href.startswith('http'):
                        print(f"✅ Encontré enlace ONU: {href}")
                        return href
                    else:
                        base_url = 'https://main.un.org'
                        full_url = urllib.parse.urljoin(base_url, href)
                        print(f"✅ Encontré enlace ONU: {full_url}")
                        return full_url
            
            # Buscar cualquier enlace que contenga 'xml' y 'consolidated'
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if 'xml' in href.lower() and 'consolidat' in href.lower():
                    if href.startswith('http'):
                        print(f"✅ Encontré enlace ONU por href: {href}")
                        return href
                    else:
                        base_url = 'https://main.un.org'
                        full_url = urllib.parse.urljoin(base_url, href)
                        print(f"✅ Encontré enlace ONU por href: {full_url}")
                        return full_url
            
            # URL conocida de respaldo
            fallback_url = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
            print(f"⚠️ No encontré enlace específico, usando URL conocida: {fallback_url}")
            return fallback_url
            
        except Exception as e:
            print(f"❌ Error buscando enlace ONU: {e}")
            return "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
    
    def download_file(self, url, filename):
        """Descarga un archivo desde una URL"""
        try:
            print(f"📥 Descargando desde: {url}")
            
            # Headers para parecer un navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=300, stream=True)
            response.raise_for_status()
            
            # Verificar que el contenido sea XML
            content_type = response.headers.get('content-type', '').lower()
            print(f"📄 Tipo de contenido: {content_type}")
            
            filepath = os.path.join('data', filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verificar que el archivo se descargó correctamente
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:  # Al menos 1KB
                size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
                print(f"✅ Descarga exitosa: {filename} ({size_mb} MB)")
                return True
            else:
                print(f"❌ Archivo descargado está vacío o muy pequeño")
                return False
                
        except Exception as e:
            print(f"❌ Error descargando {filename}: {e}")
            return False
    
    def descargar_lista_ofac(self):
        """Descarga la lista real de OFAC"""
        print("\n📋 === DESCARGANDO LISTA OFAC ===")
        
        download_url = self.get_ofac_download_url()
        if not download_url:
            print("❌ No se pudo obtener URL de descarga de OFAC")
            return False
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ofac_sdn_enhanced_{timestamp}.xml"
        
        success = self.download_file(download_url, filename)
        
        if success:
            # Crear enlace al archivo más reciente
            latest_file = os.path.join('data', 'ofac_latest.xml')
            if os.path.exists(latest_file):
                os.remove(latest_file)
            
            # Crear copia con nombre fijo
            import shutil
            shutil.copy2(os.path.join('data', filename), latest_file)
            print(f"🔗 Creado enlace: ofac_latest.xml")
        
        return success
    
    def descargar_lista_onu(self):
        """Descarga la lista real de la ONU"""
        print("\n📋 === DESCARGANDO LISTA ONU ===")
        
        download_url = self.get_onu_download_url()
        if not download_url:
            print("❌ No se pudo obtener URL de descarga de ONU")
            return False
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"onu_consolidated_{timestamp}.xml"
        
        success = self.download_file(download_url, filename)
        
        if success:
            # Crear enlace al archivo más reciente
            latest_file = os.path.join('data', 'onu_latest.xml')
            if os.path.exists(latest_file):
                os.remove(latest_file)
            
            # Crear copia con nombre fijo
            import shutil
            shutil.copy2(os.path.join('data', filename), latest_file)
            print(f"🔗 Creado enlace: onu_latest.xml")
        
        return success
    
    def descargar_todas_las_listas(self):
        """Descarga todas las listas reales"""
        print("\n🚀 ¡Empezando descarga de LISTAS REALES!")
        print("=" * 60)
        
        resultados = {}
        
        # Descargar OFAC
        resultados['ofac'] = self.descargar_lista_ofac()
        
        print("\n⏳ Esperando 5 segundos entre descargas...")
        time.sleep(5)
        
        # Descargar ONU
        resultados['onu'] = self.descargar_lista_onu()
        
        # Mostrar resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL:")
        exitosas = sum(resultados.values())
        total = len(resultados)
        
        for lista, exito in resultados.items():
            emoji = "✅" if exito else "❌"
            description = self.sources[lista]['description']
            print(f"  {emoji} {lista.upper()}: {description}")
        
        print(f"\n🎯 Total: {exitosas}/{total} listas descargadas")
        
        if exitosas == total:
            print("🎉 ¡TODAS las listas REALES se descargaron correctamente!")
        else:
            print("⚠️  Algunas listas fallaron")
        
        return resultados
    
    def mostrar_archivos(self):
        """Muestra información de los archivos descargados"""
        print("\n📁 ARCHIVOS DESCARGADOS:")
        print("=" * 50)
        
        if os.path.exists('data'):
            archivos = os.listdir('data')
            if archivos:
                for archivo in sorted(archivos):
                    ruta = os.path.join('data', archivo)
                    if os.path.isfile(ruta):
                        size_mb = round(os.path.getsize(ruta) / (1024 * 1024), 2)
                        print(f"📄 {archivo} ({size_mb} MB)")
            else:
                print("🤷 No hay archivos todavía")
        else:
            print("❌ La carpeta 'data' no existe")

# 🚀 ¡AQUÍ EMPIEZA LA MAGIA!
if __name__ == "__main__":
    print("🌟 ¡Robot Descargador de Listas REALES OFAC/ONU!")
    print("🔄 Descargando listas oficiales de sanciones...")
    print()
    
    # Crear nuestro robot
    robot = RobotDescargadorReal()
    
    # Pedirle que descargue todo
    robot.descargar_todas_las_listas()
    
    # Mostrar qué descargó
    robot.mostrar_archivos()
    
    print("\n🎉 ¡El robot terminó su trabajo!")
    print("💤 Ahora se va a dormir...")
    print("🔄 Volverá a trabajar según su programación automática")