import random
from datetime import datetime

# ============================================
# DATOS DEL SISTEMA Y REPORTE
# ============================================

num_reporte = random.randint(1000, 9999)
numero_reporte = f"REP-{num_reporte}"

fecha_actual = datetime.now().strftime("%d/%m/%Y")
hora_actual = datetime.now().strftime("%H:%M")

print("=" * 60)
print("       SISTEMA DE DIAGNÓSTICO TÉCNICO MULTIDISPOSITIVO")
print("=" * 60)
print("Bienvenido al sistema de diagnóstico\n")

# Captura de datos
nombre = input("¿Cuál es tu nombre?: ").strip()
ubicacion = input("¿Desde dónde nos visitas?: ").strip()

print("\n--- Selección de Equipo ---")
print("1. PC de Escritorio")
print("2. Laptop")
print("3. Tablet")
print("4. Otro")

try:
    opcion_equipo = int(input("Selecciona tu tipo de equipo (1-4): "))
except ValueError:
    opcion_equipo = 4

# Identificación clara del dispositivo
if opcion_equipo == 1:
    tipo_dispositivo = "PC"
elif opcion_equipo == 2:
    tipo_dispositivo = "Laptop"
elif opcion_equipo == 3:
    tipo_dispositivo = "Tablet"
else:
    tipo_dispositivo = "Otro"

usuario_id = input("¿Cuál es tu usuario?: ").strip()

print("\n" + "-" * 60)
print(f" FOLIO DE REPORTE: {numero_reporte} | Fecha: {fecha_actual} {hora_actual}")
print(f" Cliente: {nombre} | Usuario ID: {usuario_id}")
print(f" Ubicación: {ubicacion} | Equipo: {tipo_dispositivo}")
print("-" * 60 + "\n")

# ============================================
# ÁRBOL DE DIAGNÓSTICO SEGÚN DISPOSITIVO
# ============================================

# 1. ENERGÍA / ALIMENTACIÓN
electricidad = input("¿El equipo enciende o muestra indicador de carga? (si/no): ").strip().lower() == "si"

if not electricidad:
    print("\nDIAGNÓSTICO:")
    print("Fallo de energía o batería completamente agotada.")
    print("PROPUESTA:")
    if tipo_dispositivo == "Tablet":
        print("- Probar con otro cargador/cable USB-C o Lightning de mayor potencia (W).")
        print("- Limpiar el puerto de carga (revisar que no tenga pelusa o suciedad).")
        print("- Dejar cargando mínimo 30 minutos sin intentar encender.")
        print("- Inspeccionar el centro de carga por daño físico o sulfatación.")
    elif tipo_dispositivo == "Laptop":
        print("- Verificar el cargador/eliminador y tomar lectura del voltaje.")
        print("- Intentar desconectar la batería interna y encender directo a la corriente.")
        print("- Inspeccionar puerto de carga (Jack DC o USB-C PD).")
    else:  # PC u otro
        print("- Revisar conexión a la toma de corriente y el regulador/No-Break.")
        print("- Verificar el cable de alimentación trifásico.")
        print("- Probar el switch I/O posterior de la fuente de poder.")

else:
    # 2. ENCENDIDO / PANTALLA
    enciende = input("¿El sistema responde al presionar el botón de encendido? (si/no): ").strip().lower() == "si"

    if not enciende:
        print("\nDIAGNÓSTICO:")
        print("El dispositivo no completa el proceso de arranque.")
        print("PROPUESTA:")
        if tipo_dispositivo == "Tablet":
            print("- Realizar un reinicio forzado (mantener presionado Botón Encendido + Bajar Volumen por 15 segundos).")
            print("- Verificar si el botón de encendido se encuentra atascado.")
            print("- Revisar tarjeta lógica por posible corto en la línea principal.")
        elif tipo_dispositivo == "Laptop":
            print("- Drenar la energía estática (mantener botón de encendido presionado 30 seg sin cargador).")
            print("- Revisar si el flexor del teclado o botón de encendido funciona correctamente.")
        else:
            print("- Revisar estado de la fuente de poder o la placa madre.")
            print("- Verificar botones del chasis y conexiones internas.")

    else:
        # 3. IMAGEN (Ajustado por dispositivo)
        imagen = input("¿Muestra imagen en la pantalla? (si/no): ").strip().lower() == "si"

        if not imagen:
            print("\nDIAGNÓSTICO:")
            print("El equipo enciende pero no proyecta imagen.")
            print("PROPUESTA:")
            if tipo_dispositivo == "Tablet":
                print("- Iluminar el display con una lámpara para descartar fallo en el Backlight (luz de fondo).")
                print("- Verificar si la pantalla táctil o el display AMOLED/LCD sufrió presión interna o ruptura.")
                print("- Revisar conexión del flexor del display en la tarjeta madre.")
            elif tipo_dispositivo == "Laptop":
                print("- Conectar a monitor externo vía USB-C (Modo DisplayPort / Alt DP) o Mini DisplayPort.")
                print("- Probar atajo de conmutación de pantalla (Fn + F4/F5/F8).")
                print("- Inspeccionar el flexor de video de la bisagra.")
            else:  # PC
                print("- Inspeccionar puertos de video de la GPU/Motherboard (HDMI / DisplayPort / VGA).")
                print("- Probar cambiando el cable de video o probando en otro monitor.")

        else:
            # 4. SONIDO
            sonido = input("¿Tiene sonido? (si/no): ").strip().lower() == "si"

            if not sonido:
                print("\nDIAGNÓSTICO:")
                print("El equipo no emite audio.")
                print("PROPUESTA:")
                if tipo_dispositivo == "Tablet":
                    print("- Verificar que el equipo no esté congelado en 'Modo Audífonos' por suciedad en la entrada USB-C/3.5mm.")
                    print("- Desactivar conexiones Bluetooth que puedan estar desviando el audio.")
                    print("- Probar las bocinas integradas con una aplicación de prueba.")
                else:
                    print("- Revisar salida de audio predeterminada en el sistema operativo.")
                    print("- Reinstalar o actualizar los controladores de audio.")
                    print("- Inspeccionar bocinas o conexión del Jack de audio.")

            else:
                # 5. INTERNET / RED
                internet = input("¿Tiene conexión a internet? (si/no): ").strip().lower() == "si"

                if not internet:
                    print("\nDIAGNÓSTICO:")
                    print("El dispositivo no se conecta a internet.")
                    print("PROPUESTA:")
                    if tipo_dispositivo == "Tablet":
                        print("- Olvidar la red Wi-Fi y volver a ingresar la contraseña.")
                        print("- Restablecer la configuración de red desde el menú de Ajustes.")
                        print("- Comprobar si el módulo Wi-Fi / Bluetooth integrado requiere reinicio.")
                    elif tipo_dispositivo == "Laptop":
                        print("- Verificar que la tecla de Modo Avión / Wi-Fi no esté activa.")
                        print("- Usar adaptador Ethernet USB-C en caso de requerir red cableada.")
                    else:
                        print("- Inspeccionar cable de red RJ45, router o antena Wi-Fi PCIe.")

                else:
                    # 6. TEMPERATURA
                    temperatura = input("¿Presenta calentamiento excesivo durante el uso? (si/no): ").strip().lower() == "si"

                    if temperatura:
                        print("\nDIAGNÓSTICO:")
                        print("El sistema presenta sobrecalentamiento excesivo.")
                        print("PROPUESTA:")
                        if tipo_dispositivo == "Tablet":
                            print("- Cerrar aplicaciones en segundo plano que saturen el procesador SoC.")
                            print("- Evitar el uso mientras se carga con cargadores de carga rápida.")
                            print("- Comprobar que la batería no presente hinchazón o degradación grave.")
                        else:
                            print("- Limpiar las rejillas y ventiladores de polvo.")
                            print("- Cambiar la pasta térmica del procesador/GPU.")

                    else:
                        print("\nDIAGNÓSTICO:")
                        print("El sistema funciona correctamente.")
                        print("PROPUESTA:")
                        print("- Realizar mantenimiento preventivo de software y optimización del almacenamiento.")

print("\n" + "=" * 60)
print("          FIN DEL REPORTE TÉCNICO")
print("=" * 60)