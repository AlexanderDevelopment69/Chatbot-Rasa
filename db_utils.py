import mysql.connector
from datetime import datetime


class DBUtils:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='161.132.40.103',
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
            disponibilidad_info = "Habitaciones disponibles en esas fechas:\n\n"
            for row in result:
                disponibilidad_info += f"{row['nombre_tipo']}\n" \
                                       f"Cantidad Disponible: {row['cantidad_disponible']}\n" \
                                       f"Números de Habitaciones: {row['numeros_habitaciones']}\n\n"
        else:
            disponibilidad_info = "Lo siento, no hay habitaciones disponibles en esas fechas."

        return disponibilidad_info

    def consultar_precios(self):
        query = """
        SELECT nombre_tipo, precio FROM tipos_habitaciones
        """

        result = self.execute_query(query)

        precios_info = "Precios de los tipos de habitaciones:\n"
        for row in result:
            precios_info += f"- {row[0]}: S/. {row[1]}\n"
        precios_info += "El IGV esta incluido en el precio de las habitaciones"

        return precios_info


    # def consultar_precios(self):
    #     query = """
    #         SELECT nombre_tipo, costo, IGV, precio
    #         FROM tipos_habitaciones;
    #     """
    #     result = self.execute_query(query)
    #
    #     precios_info = "Precios de los tipos de habitaciones:\n"
    #
    #     for row in result:
    #         precios_info += f"- {row[0]}:\n"
    #         precios_info += f"  Costo: S/. {row[1]}\n"
    #         precios_info += f"  IGV: S/. {row[2]}\n"
    #         precios_info += f"  Precio: S/. {row[3]}\n\n"
    #
    #     return precios_info


    def consultar_servicios(self):
        query = """
        SELECT DISTINCT th.nombre_tipo AS Tipo_Habitacion, s.nombre AS Servicio
        FROM tipos_habitaciones th
        INNER JOIN habitaciones h ON th.id_tipo_habitacion = h.id_tipo_habitacion
        LEFT JOIN servicios s ON th.id_tipo_habitacion = s.id_tipo_habitacion
        ORDER BY FIELD(th.nombre_tipo, 'Habitación Individual', 'Habitación Doble', 'Habitación Matrimonial'), s.nombre;
        """

        result = self.execute_query(query)

        servicios_info = "Servicios disponibles por tipo de habitación:\n"
        current_tipo_habitacion = None

        for row in result:
            tipo_habitacion = row[0]
            servicio = row[1]

            if tipo_habitacion != current_tipo_habitacion:
                servicios_info += f"\n{tipo_habitacion}:\n"
                current_tipo_habitacion = tipo_habitacion

            servicios_info += f"- {servicio}\n"

        return servicios_info

    def consultar_tipos_habitaciones(self):
        self.cursor = self.conn.cursor(dictionary=True)
        query = """
        SELECT th.nombre_tipo, GROUP_CONCAT(h.numero_habitacion ORDER BY h.numero_habitacion) AS numeros_habitaciones
        FROM tipos_habitaciones th
        LEFT JOIN habitaciones h ON th.id_tipo_habitacion = h.id_tipo_habitacion
        GROUP BY th.nombre_tipo
        ORDER BY FIELD(th.nombre_tipo, 'Habitación Individual', 'Habitación Doble', 'Habitación Matrimonial')
        """

        result = self.execute_query(query)

        tipos_habitaciones_info = "Tipos de habitaciones y sus números de habitación:\n"

        for row in result:
            tipo_habitacion = row['nombre_tipo']
            numeros_habitaciones = row['numeros_habitaciones']
            tipos_habitaciones_info += f"- {tipo_habitacion}: {numeros_habitaciones}\n"

        return tipos_habitaciones_info

    def costo_tipo_habitaciones_por_evento(self, nombre_evento):
        self.cursor = self.conn.cursor(dictionary=True)
        query = """
        SELECT th.nombre_tipo AS tipo_habitacion, the.costo_tipo_habitacion_evento AS costo
        FROM tipos_habitaciones_eventos AS the
        JOIN tipos_habitaciones AS th ON the.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN eventos AS e ON the.id_evento = e.id_evento
        WHERE e.nombre_evento = %s
        """

        result = self.execute_query(query, (nombre_evento,))


        if result:
            costo_habitaciones_info = f"Costo de tipo de habitaciones para el evento {nombre_evento}:\n"
            for row in result:
                tipo_habitacion = row['tipo_habitacion']
                costo = row['costo']
                costo_habitaciones_info += f"- {tipo_habitacion}: {costo}\n"
        else:
            costo_habitaciones_info = f"No se encontraron resultados para el evento '{nombre_evento}'."

        return costo_habitaciones_info

    # def insert_interaccion(self, nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot):
    #     query = """
    #     INSERT INTO chatbot_interacciones (nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot)
    #     VALUES (%s, %s, %s, %s, %s)
    #     """
    #
    #     values = (nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot)
    #
    #     self.execute_query(query, values)

    def insert_interaccion(self, nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot,tiempo_usuario_envia, tiempo_chatbot_responde,id_usuario):
        # tiempo_usuario_envia = self.capture_user_message_time()
        # tiempo_chatbot_responde = self.capture_bot_response_time()

        query = """
        INSERT INTO chatbot_interacciones (nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde,id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nombres_usuario, correo_usuario, tipo_interaccion, mensaje_usuario, respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde,id_usuario)
        self.execute_query(query, values)

    def capture_user_message_time(self):
        return datetime.now()

    def capture_bot_response_time(self):
        return datetime.now()



    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close_connection()
