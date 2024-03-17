# actions.py

import subprocess
import time
import webbrowser
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import ActionExecuted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

# from .db_utils import DBUtils
from db_utils import DBUtils


#
# class ActionStoreUserInfo(Action):
#     def name(self) -> Text:
#         return "action_store_user_info"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         nombres_usuario = tracker.get_slot("nombres_usuario")
#         correo_usuario = tracker.get_slot("correo_usuario")
#
#         # Almacena la información del usuario en la base de datos
#         db_utils = DBUtils()
#         db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Registro", "", "")
#
#         dispatcher.utter_message(text=f"Gracias, {nombres_usuario}!.")
#
#         # Registra la interacción en la base de datos
#         mensaje_usuario = tracker.latest_message['text']
#         respuesta_chatbot = dispatcher.messages[-1]['text']
#         db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Registro", mensaje_usuario, respuesta_chatbot)
#
#         return []


class ActionStoreUserInfo(Action):
    def name(self) -> Text:
        return "action_store_user_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")

        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # id_usuario = tracker.sender_id  # Identificador único del usuario proporcionado por Rasa
        # print("Sender ID:", id_usuario)

        # Almacena la información del usuario en la base de datos
        db_utils = DBUtils()
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = f"Gracias, {nombres_usuario}!."

        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()

        # Registra la interacción en la base de datos
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Registro", mensaje_usuario, respuesta_chatbot,
                                    tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        # dispatcher.utter_message(text=respuesta_chatbot)

        return []


class ActionConsultaDisponibilidad(Action):
    def name(self) -> Text:
        return "action_consulta_disponibilidad"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        fecha_llegada = tracker.get_slot("fecha_llegada")
        fecha_salida = tracker.get_slot("fecha_salida")

        # Lógica para consultar disponibilidad desde la base de datos
        db_utils = DBUtils()
        disponibilidad_info = db_utils.consultar_disponibilidad(fecha_llegada, fecha_salida)

        dispatcher.utter_message(text=disponibilidad_info)

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = disponibilidad_info

        db_utils2 = DBUtils()

        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()

        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Disponibilidad", mensaje_usuario,
                                     respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaPrecios(Action):
    def name(self) -> Text:
        return "action_consulta_precios"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Lógica para consultar precios desde la base de datos
        db_utils = DBUtils()
        precios_info = db_utils.consultar_precios()

        dispatcher.utter_message(text=precios_info)

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = precios_info

        db_utils2 = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()

        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Precios", mensaje_usuario,
                                     respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaHabitaciones(Action):
    def name(self) -> Text:
        return "action_consulta_habitaciones"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Lógica para consultar precios desde la base de datos
        db_utils = DBUtils()
        habitaciones_info = db_utils.consultar_tipos_habitaciones()

        dispatcher.utter_message(text=habitaciones_info)

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = habitaciones_info

        db_utils2 = DBUtils()

        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()

        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Habitaciones", mensaje_usuario,
                                     respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []

    class ActionConsultarCostoHabitacionesPorEvento(Action):
        def name(self) -> Text:
            return "action_consulta_costo_habitaciones_evento"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            # nombre_evento = tracker.latest_message['text']  # Obtener el nombre del evento desde el mensaje del usuario

            # Capturar el tiempo cuando el usuario envía un mensaje
            tiempo_usuario_envia = datetime.now()

            # Obtener el usuario_id del cuerpo del mensaje
            id_usuario = tracker.sender_id

            # Obtener el valor de la entidad nombre_evento
            nombre_evento = next(tracker.get_latest_entity_values("nombre_evento"))

            # nombre_evento = tracker.get_slot("nombre_evento")

            # Lógica para consultar los costos de habitación por evento
            db_utils = DBUtils()
            costo_habitaciones_info = db_utils.costo_tipo_habitaciones_por_evento(nombre_evento)

            # Registra la interacción en la base de datos
            nombres_usuario = tracker.get_slot("nombres_usuario")
            correo_usuario = tracker.get_slot("correo_usuario")
            mensaje_usuario = tracker.latest_message['text']
            respuesta_chatbot = costo_habitaciones_info

            db_utils2 = DBUtils()

            # Capturar el tiempo cuando el chatbot responde
            tiempo_chatbot_responde = datetime.now()

            db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Habitaciones_Evento",
                                         mensaje_usuario,
                                         respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

            dispatcher.utter_message(text=costo_habitaciones_info)

            return []


class ActionConsultaServicios(Action):
    def name(self) -> Text:
        return "action_consulta_servicios"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Lógica para consultar servicios desde la base de datos
        db_utils = DBUtils()
        servicios_info = db_utils.consultar_servicios()

        dispatcher.utter_message(text=servicios_info)

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = servicios_info

        db_utils2 = DBUtils()

        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()

        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Servicios", mensaje_usuario,
                                     respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionMostrarBotonesReserva(Action):
    def name(self) -> Text:
        return "action_mostrar_botones_reserva"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_reserva_buttons")
        return []


class ActionConsultaReserva(Action):
    def name(self) -> Text:
        return "action_confirmar_reserva"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Obtener la respuesta del usuario del slot 'numero_habitacion'
        tipo_id = tracker.get_slot('numero_habitacion')

        print("Numero de habitacion: ", tipo_id)

        # Validar si la respuesta es un número válido
        if tipo_id.isdigit() and 0 < int(tipo_id) <= 20:
            url = f"https://hotelsancristobal-ayacucho.com/reserva/reserva_form?tipoId={tipo_id}"
            # Emoticones Unicode
            emoticon_habitaciones = "\U0001F3E8"  # Emoticon Unicode para habitaciones
            mano_derecha = "\U0001F449"  # Emoticon Unicode para mano que apunta hacia la derecha

            # Enviar un mensaje con los emoticones y el enlace en formato HTML
            message = f"Puedes reservar tu habitación {emoticon_habitaciones}{mano_derecha} <a href='{url}' target='_blank'>aquí</a>."
            dispatcher.utter_message(text=message, parse_mode="HTML")

            # Registra la interacción en la base de datos
            nombres_usuario = tracker.get_slot("nombres_usuario")
            correo_usuario = tracker.get_slot("correo_usuario")
            mensaje_usuario = tracker.latest_message['text']
            respuesta_chatbot = url

            db_utils = DBUtils()

            # Capturar el tiempo cuando el chatbot responde
            tiempo_chatbot_responde = datetime.now()

            db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Reserva", mensaje_usuario,
                                        respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde,
                                        id_usuario)

        return []


class ActionMostrarBotonWhatsapp(Action):
    def name(self) -> Text:
        return "action_mostrar_boton_whatssap"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_whatsapp_button")
        return []


class ActionMostrarBotonPromocion(Action):
    def name(self) -> Text:
        return "action_mostrar_boton_promocion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_conculta_promocion_button")
        return []


class ActionMostrarBotonEncuesta(Action):
    def name(self) -> Text:
        return "action_mostrar_boton_encuesta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_encuesta_button")
        return []


class ActionMostrarBotonContinuarConversacion(Action):
    def name(self) -> Text:
        return "action_mostrar_boton_continuar_conversacion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_continuar_conversacion_button")
        return []


# class ActionRedirigirWsp(Action):
#     def name(self) -> Text:
#         return "action_redirigir_wsp"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         # Obtener la URL del enlace externo desde el dominio
#         url = "https://wa.link/w653qw"
#
#         # Enviar un mensaje al usuario indicando el redireccionamiento
#         dispatcher.utter_message(text="¡Redirigiendo al WhatsApp del recepcionista!")
#
#         # Crear una respuesta de tipo "redirect" para abrir la URL en una nueva pestaña
#         dispatcher.utter_custom_json({
#             "redirect": url
#         })
#
#         return []


class ValidateNombresUsuarioForm(Action):
    def name(self) -> Text:
        return "validate_nombres_usuario_form"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        nombres_usuario = tracker.get_slot("nombres_usuario")

        if nombres_usuario is None:
            dispatcher.utter_message(template="utter_ask_nombres_usuario")

        return []


class ValidateCorreoUsuarioForm(Action):
    def name(self) -> Text:
        return "validate_correo_usuario_form"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        correo_usuario = tracker.get_slot("correo_usuario")

        if correo_usuario is None:
            dispatcher.utter_message(template="utter_ask_correo_usuario")

        return []


class ActionRedirigirWsp(Action):
    def name(self) -> Text:
        return "action_redirigir_wsp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Abre el enlace en el navegador
        # url = "https://wa.link/zcknj0"
        # webbrowser.open_new_tab(url)
        # dispatcher.utter_message(text="¡Abriendo WhatsApp en el navegador!")

        # Generar el enlace
        url = "https://wa.link/yv2l8v"

        # Emoticones Unicode
        emoticon_whatsapp = "\U0001F4F1"  # Emoticon Unicode para WhatsApp
        emoticon_mano_whatsapp = "\U0001F44B"  # Emoticon Unicode para mano que señala hacia arriba

        # Enviar un mensaje con los emoticones y el enlace en formato HTML
        message = f"Puedes contactarnos en WhatsApp {emoticon_whatsapp} {emoticon_mano_whatsapp} <a href='{url}' target='_blank'>aqui</a>."
        dispatcher.utter_message(text=message, parse_mode="HTML")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = url

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()

        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_wsp", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionRedirigirReserva(Action):
    def name(self) -> Text:
        return "action_redirigir_reserva"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Abre el enlace en el navegador
        # url = "http://localhost:80/habitaciones"
        # webbrowser.open_new_tab(url)
        # dispatcher.utter_message(text="¡Abriendo la pagina de reservas en el navegador!")

        # Generar el enlace
        url = "https://hotelsancristobal-ayacucho.com/habitaciones"

        # Emoticones Unicode
        emoticon_habitaciones = "\U0001F3E8"  # Emoticon Unicode para habitaciones
        mano_derecha = "\U0001F449"  # Emoticon Unicode para mano que apunta hacia la derecha

        # Enviar un mensaje con los emoticones y el enlace en formato HTML
        message = f"Puedes reservar habitaciones {emoticon_habitaciones}{mano_derecha} <a href='{url}' target='_blank'>aqui</a>."
        dispatcher.utter_message(text=message, parse_mode="HTML")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = url

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_reserva", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionRedirigirEncuesta(Action):
    def name(self) -> Text:
        return "action_redirigir_encuesta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # # Abre el enlace en el navegador
        # url = "https://docs.google.com/forms/d/e/1FAIpQLSctnNrx4mcbVfAepsClb6zoXN3xBwaycCjj70FXPWrt2W8m3A/viewform"
        # webbrowser.open_new_tab(url)

        # Generar el enlace
        url = "https://docs.google.com/forms/d/e/1FAIpQLSctnNrx4mcbVfAepsClb6zoXN3xBwaycCjj70FXPWrt2W8m3A/viewform"

        # Emoticones Unicode
        mano_derecha = "\U0001F449"  # Emoticon Unicode para mano que apunta hacia la derecha
        emoticon_encuesta = "\U0001F4D6"  # Emoticon Unicode para encuesta

        # Enviar un mensaje con los emoticones y el enlace en formato HTML
        message = f"Puedes acceder a nuestra encuesta {emoticon_encuesta} {mano_derecha}<a href='{url}' target='_blank'>aqui</a>."
        dispatcher.utter_message(text=message, parse_mode="HTML")

        # dispatcher.utter_message(text="¡Abriendo encuenta en el navegador!")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = url

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_encuenta", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionRedirigirPromocionSi(Action):
    def name(self) -> Text:
        return "action_redirigir_promocion_si"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Enviar un mensaje con los emoticones y el enlace en formato HTML
        message = "Gracias 😊,ahora podemos informarte. ¿Cómo puedo ayudarte hoy? "

        dispatcher.utter_message(text=message)

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = message

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_promocion_si", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionRedirigirPromocionNo(Action):
    def name(self) -> Text:
        return "action_redirigir_promocion_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Enviar un mensaje con los emoticones y el enlace en formato HTML
        message = "¿Cómo puedo ayudarte hoy? 😊"

        dispatcher.utter_message(text=message)

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = message

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_promocion_no", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionInformacionPago(Action):
    def name(self) -> Text:
        return "action_info_pago"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Captura el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        # Envía el mensaje al usuario
        dispatcher.utter_message(response="utter_asistencia_pago")

        # Obtener el contenido del mensaje definido en el dominio
        respuesta = next(response['text'] for response in domain['responses']['utter_asistencia_pago'])

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Información pagos", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaRegistroSalida(Action):
    def name(self) -> Text:
        return "action_consulta_registro_salida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Capturar el tiempo cuando el usuario envía un mensaje
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        dispatcher.utter_message(response="utter_consulta_registro_salida")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_registro_salida'])

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        # Capturar el tiempo cuando el chatbot responde
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Politica de regisro y salida", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaDeposito(Action):
    def name(self) -> Text:
        return "action_consulta_deposito"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        dispatcher.utter_message(response="utter_consulta_deposito")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_deposito'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta depósito", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaCancelaciones(Action):
    def name(self) -> Text:
        return "action_consulta_cancelaciones"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()

        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        dispatcher.utter_message(response="utter_consulta_cancelaciones")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_cancelaciones'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta cancelaciones", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaPoliticaEdad(Action):
    def name(self) -> Text:
        return "action_consulta_politica_edad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        dispatcher.utter_message(response="utter_consulta_politica_edad")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_politica_edad'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta política de edad", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaCargoDanios(Action):
    def name(self) -> Text:
        return "action_consulta_cargo_danios"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        dispatcher.utter_message(response="utter_consulta_cargo_danios")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_cargo_danios'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta cargo por daños", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaLimpieza(Action):
    def name(self) -> Text:
        return "action_consulta_limpieza"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id

        dispatcher.utter_message(response="utter_consulta_limpieza")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_limpieza'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta política de limpieza", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaRestriccionesBebidas(Action):
    def name(self) -> Text:
        return "action_consulta_restricciones_bebidas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id
        dispatcher.utter_message(response="utter_consulta_restricciones_bebidas")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_restricciones_bebidas'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta restricciones de bebidas",
                                    mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaHorarioSilencio(Action):
    def name(self) -> Text:
        return "action_consulta_horario_silencio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id
        dispatcher.utter_message(response="utter_consulta_horario_silencio")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_horario_silencio'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta horario de silencio", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaMascotas(Action):
    def name(self) -> Text:
        return "action_consulta_mascotas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id
        dispatcher.utter_message(response="utter_consulta_mascotas")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_mascotas'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta política de mascotas", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaComportamientoInapropiado(Action):
    def name(self) -> Text:
        return "action_consulta_comportamiento_inapropiado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id
        dispatcher.utter_message(response="utter_consulta_comportamiento_inapropiado")

        respuesta = next(
            response['text'] for response in domain['responses']['utter_consulta_comportamiento_inapropiado'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta comportamiento inapropiado",
                                    mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaPerdidas(Action):
    def name(self) -> Text:
        return "action_consulta_perdidas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id
        dispatcher.utter_message(response="utter_consulta_perdidas")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_perdidas'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta política de pérdidas", mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


class ActionConsultaAtencion(Action):
    def name(self) -> Text:
        return "action_consulta_atencion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tiempo_usuario_envia = datetime.now()
        # Obtener el usuario_id del cuerpo del mensaje
        id_usuario = tracker.sender_id
        dispatcher.utter_message(response="utter_consulta_atencion")

        respuesta = next(response['text'] for response in domain['responses']['utter_consulta_atencion'])

        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        tiempo_chatbot_responde = datetime.now()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Consulta disponibilidad atencion",
                                    mensaje_usuario,
                                    respuesta_chatbot, tiempo_usuario_envia, tiempo_chatbot_responde, id_usuario)

        return []


# class ActionFallback(Action):
#     def name(self) -> Text:
#         return "action_fallback"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="utter_fallback_message")
#         return []


class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_fallback_message")
        dispatcher.utter_message(response="utter_whatsapp_button")
        return []
        # Llamar al otro action directamente
        # return ActionMostrarBotonWhatsapp().run(dispatcher, tracker, domain)

# class ActionUtterConsultaReserva(Action):
#     def name(self) -> Text:
#         return "action_capturar_numero_habitacion"
#
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         # Capturar la respuesta del usuario y almacenarla en un slot temporal "respuesta_temporal"
#         respuesta_usuario = tracker.latest_message.get('text')
#         return [SlotSet("numero_habitacion", respuesta_usuario)]
