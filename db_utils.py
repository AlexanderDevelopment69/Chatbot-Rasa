import mysql.connector
from datetime import datetime


class DBUtils:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='161.132.54.10',
            user='admin',
            password='EwYNY0Dvz6bst3vI',
            database='hotelSanCristobal'
        )
        self.cursor = self.conn.cursor()
        # self.cursor = self.conn.cursor(dictionary=True)

    def execute_query(self, query, values=None):

        try:
            self.cursor.execute(query, values)

            result = self.cursor.fetchall()  # Lee y almacena los resultados
            self.conn.commit()
            return result
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            return None
        finally:
            self.close_connection()


    # def consultar_disponibilidad(self, fecha_llegada, fecha_salida):
    #     # Query optimizado adaptado
    #     query = f"""
    #            SELECT
    #                th.nombre_tipo,
    #                COUNT(h.id_habitacion) as cantidad_disponible,
    #                GROUP_CONCAT(h.id_habitacion ORDER BY h.id_habitacion) AS numeros_habitaciones
    #            FROM tipos_habitaciones th
    #            INNER JOIN habitaciones h ON th.id_tipo_habitacion = h.id_tipo_habitacion
    #            LEFT JOIN reservas r ON h.id_habitacion = r.id_habitacion
    #               AND (r.fecha_inicio <= '{fecha_salida}' AND r.fecha_fin >= '{fecha_llegada}')
    #            WHERE r.id_habitacion IS NULL
    #            GROUP BY th.nombre_tipo
    #            ORDER BY FIELD(th.nombre_tipo, 'Habitación Individual', 'Habitación Doble', 'Habitación Matrimonial');
    #        """
    #
    #     result = self.execute_query(query, values=None)
    #
    #     if result:
    #         disponibilidad_info = "Habitaciones disponibles en esas fechas:"
    #         for row in result:
    #             disponibilidad_info += f"\nTipo de Habitación: {row['nombre_tipo']}, " \
    #                                    f"Cantidad Disponible: {row['cantidad_disponible']}, " \
    #                                    f"Números de Habitaciones: {row['numeros_habitaciones']}"
    #     else:
    #         disponibilidad_info = "Lo siento, no hay habitaciones disponibles en esas fechas."
    #
    #     return disponibilidad_info

    def consultar_disponibilidad(self, fecha_llegada, fecha_salida):
        self.cursor = self.conn.cursor(dictionary=True)
        # Convierte las fechas de entrada al formato deseado
        fecha_llegada = datetime.strptime(fecha_llegada, '%d-%m-%Y')
        fecha_salida = datetime.strptime(fecha_salida, '%d-%m-%Y')

        # Formatea las fechas para que coincidan con el formato en la base de datos
        fecha_llegada_str = fecha_llegada.strftime('%Y-%m-%d')
        fecha_salida_str = fecha_salida.strftime('%Y-%m-%d')

        # Query optimizado adaptado
        query = f"""
                  SELECT
                      th.nombre_tipo,
                      COUNT(h.id_habitacion) as cantidad_disponible,
                      GROUP_CONCAT(h.id_habitacion ORDER BY h.id_habitacion) AS numeros_habitaciones
                  FROM tipos_habitaciones th
                  INNER JOIN habitaciones h ON th.id_tipo_habitacion = h.id_tipo_habitacion
                  LEFT JOIN reservas r ON h.id_habitacion = r.id_habitacion
                     AND (r.fecha_inicio <= '{fecha_salida_str}' AND r.fecha_fin >= '{fecha_llegada_str}')
                  WHERE r.id_habitacion IS NULL
                  GROUP BY th.nombre_tipo
                  ORDER BY FIELD(th.nombre_tipo, 'Habitación Individual', 'Habitación Doble', 'Habitación Matrimonial');
              """

        result = self.execute_query(query, values=None)

        if result:
            disponibilidad_info = "Habitaciones disponibles en esas fechas:"
            for row in result:
                disponibilidad_info += f"\nTipo de Habitación: {row['nombre_tipo']}, " \
                                       f"Cantidad Disponible: {row['cantidad_disponible']}, " \
                                       f"Números de Habitaciones: {row['numeros_habitaciones']}"
        else:
            disponibilidad_info = "Lo siento, no hay habitaciones disponibles en esas fechas."

        return disponibilidad_info

    def consultar_precios(self):
        query = """
        SELECT nombre_tipo, costo FROM tipos_habitaciones
        """

        result = self.execute_query(query)

        precios_info = "Precios de los tipos de habitaciones:\n"
        for row in result:
            precios_info += f"{row[0]}: ${row[1]}\n"

        return precios_info

    def consultar_servicios(self):
        query = """
        SELECT nombre FROM servicios
        """

        result = self.execute_query(query)

        servicios_info = "Servicios disponibles:\n"
        for row in result:
            servicios_info += f"{row[0]}\n"

        return servicios_info

    def insert_interaccion(self, nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot):
        query = """
        INSERT INTO chatbot_interacciones (nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot)

        self.execute_query(query, values)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close_connection()
