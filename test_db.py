# Importa la clase
from db_utils import DBUtils  # Reemplaza "tu_modulo" con el nombre real de tu archivo

# Crea una instancia de la clase
db_utils = DBUtils()

# Prueba el método consultar_disponibilidad

# fecha_llegada = '2024-01-23'
# fecha_salida = '2024-01-30'

fecha_llegada = '23-01-2024'
fecha_salida = '30-01-2024'

disponibilidad_info = db_utils.consultar_disponibilidad(fecha_llegada, fecha_salida)
print(disponibilidad_info)

#
# # Prueba el método consultar_precios
# precios_info = db_utils.consultar_precios()
# print(precios_info)

# Prueba el método consultar_servicios
# servicios_info = db_utils.consultar_servicios()
# print(servicios_info)

#
# Prueba el método insert_interaccion
# nombres_usuario = 'John Doe'
# correo_usuario = 'john.doe@example.com'
# tipo_interaccion = 'Consulta'
# mensaje_usuario = '¿Cuáles son los servicios disponibles?'
# respuesta_chatbot = 'Los servicios disponibles son...'
# db_utils2 = DBUtils()
# db_utils2.insert_interaccion(nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, disponibilidad_info)

# Cierra la conexión al finalizar
del db_utils
