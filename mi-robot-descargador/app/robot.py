# 🤖 Mi Robot Descargador de Listas
# ¡Este robot es súper inteligente!

import requests  # Para descargar cosas de internet
import datetime  # Para saber qué día es hoy
import os        # Para trabajar con carpetas

class RobotDescargador:
    def __init__(self):
        print("🤖 ¡Hola! Soy tu robot descargador")
        print("📁 Voy a crear la carpeta 'data' si no existe")
        os.makedirs('data', exist_ok=True)
    
    def descargar_lista_mala(self, nombre_lista):
        """El robot descarga una lista de chicos malos"""
        print(f"🔍 Buscando la lista: {nombre_lista}")
        
        # Obtenemos la fecha de hoy para ponerle nombre al archivo
        hoy = datetime.datetime.now()
        nombre_archivo = f"lista_{nombre_lista}_{hoy.strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Crear contenido de ejemplo (porque las listas reales son complicadas)
        contenido = f"""
🚨 LISTA DE PERSONAS RESTRINGIDAS - {nombre_lista.upper()}
📅 Fecha: {hoy.strftime('%d/%m/%Y %H:%M:%S')}

👤 Persona 1: Juan Sin Permiso
📍 País: Tierra de Nunca Jamás
⚠️  Razón: No puede comprar dulces

👤 Persona 2: María No Viaja
📍 País: Isla Perdida  
⚠️  Razón: No puede tomar aviones

👤 Persona 3: Carlos Prohibido
📍 País: Reino de las Restricciones
⚠️  Razón: No puede entrar a tiendas

--- FIN DE LA LISTA ---
✅ Total de personas: 3
🤖 Generado por: Robot Descargador v1.0
        """
        
        # Guardar el archivo en la carpeta data
        ruta_archivo = os.path.join('data', nombre_archivo)
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            
            print(f"✅ ¡Lista descargada! Guardada como: {nombre_archivo}")
            print(f"📂 Ubicación: {ruta_archivo}")
            
            # Crear un archivo "más reciente" para encontrarlo fácil
            archivo_reciente = os.path.join('data', f'{nombre_lista}_mas_reciente.txt')
            with open(archivo_reciente, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            
            print(f"🔗 También creé: {nombre_lista}_mas_reciente.txt")
            return True
            
        except Exception as e:
            print(f"❌ ¡Ups! Algo salió mal: {e}")
            return False
    
    def descargar_todas_las_listas(self):
        """El robot descarga todas las listas que conoce"""
        print("\n🚀 ¡Empezando a descargar TODAS las listas!")
        print("=" * 50)
        
        listas = ['ofac', 'onu']  # Las dos listas importantes
        resultados = {}
        
        for lista in listas:
            print(f"\n📋 Trabajando en lista: {lista.upper()}")
            resultado = self.descargar_lista_mala(lista)
            resultados[lista] = resultado
            
            if resultado:
                print("✅ ¡Éxito!")
            else:
                print("❌ ¡Falló!")
            
            print("⏳ Esperando un poquito...")
            import time
            time.sleep(2)  # Esperar 2 segundos
        
        # Mostrar resumen final
        print("\n" + "=" * 50)
        print("📊 RESUMEN FINAL:")
        exitosas = sum(resultados.values())
        total = len(resultados)
        
        for lista, exito in resultados.items():
            emoji = "✅" if exito else "❌"
            print(f"  {emoji} {lista.upper()}")
        
        print(f"\n🎯 Total: {exitosas}/{total} listas descargadas")
        
        if exitosas == total:
            print("🎉 ¡TODAS las listas se descargaron correctamente!")
        else:
            print("⚠️  Algunas listas fallaron")
        
        return resultados
    
    def mostrar_archivos(self):
        """Muestra qué archivos tenemos guardados"""
        print("\n📁 ARCHIVOS EN MI CARPETA:")
        print("=" * 40)
        
        if os.path.exists('data'):
            archivos = os.listdir('data')
            if archivos:
                for archivo in archivos:
                    ruta = os.path.join('data', archivo)
                    tamaño = os.path.getsize(ruta)
                    print(f"📄 {archivo} ({tamaño} bytes)")
            else:
                print("🤷 No hay archivos todavía")
        else:
            print("❌ La carpeta 'data' no existe")

# 🚀 ¡AQUÍ EMPIEZA LA MAGIA!
if __name__ == "__main__":
    print("🌟 ¡Bienvenido al Robot Descargador!")
    print("🤖 Voy a descargar listas de personas restringidas")
    print()
    
    # Crear nuestro robot
    robot = RobotDescargador()
    
    # Pedirle que descargue todo
    robot.descargar_todas_las_listas()
    
    # Mostrar qué descargó
    robot.mostrar_archivos()
    
    print("\n🎉 ¡El robot terminó su trabajo!")
    print("💤 Ahora se va a dormir...")
    print("🔄 Mañana volverá a trabajar automáticamente")