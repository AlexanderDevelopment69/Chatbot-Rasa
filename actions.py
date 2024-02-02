# actions.py
import webbrowser
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import ActionExecuted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
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

        # Almacena la información del usuario en la base de datos
        db_utils = DBUtils()
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = f"Gracias, {nombres_usuario}!."

        # Registra la interacción en la base de datos
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Registro", mensaje_usuario, respuesta_chatbot)

        # dispatcher.utter_message(text=respuesta_chatbot)

        return []


class ActionConsultaDisponibilidad(Action):
    def name(self) -> Text:
        return "action_consulta_disponibilidad"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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
        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Disponibilidad", mensaje_usuario,
                                     respuesta_chatbot)

        return []


class ActionConsultaPrecios(Action):
    def name(self) -> Text:
        return "action_consulta_precios"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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
        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Precios", mensaje_usuario,
                                     respuesta_chatbot)

        return []


class ActionConsultaServicios(Action):
    def name(self) -> Text:
        return "action_consulta_servicios"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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
        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Servicios", mensaje_usuario,
                                     respuesta_chatbot)

        return []


class ActionMostrarBotonesReserva(Action):
    def name(self) -> Text:
        return "action_mostrar_botones_reserva"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_reserva_buttons")
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
        # Abre el enlace en el navegador
        url = "https://wa.link/w653qw"
        webbrowser.open_new_tab(url)
        dispatcher.utter_message(text="¡Abriendo WhatsApp en el navegador!")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = url

        db_utils = DBUtils()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_wsp", mensaje_usuario,
                                    respuesta_chatbot)

        return []


class ActionRedirigirReserva(Action):
    def name(self) -> Text:
        return "action_redirigir_reserva"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Abre el enlace en el navegador
        url = "http://localhost:80/habitaciones"
        webbrowser.open_new_tab(url)
        dispatcher.utter_message(text="¡Abriendo la pagina de reservas en el navegador!")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = url

        db_utils = DBUtils()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_reserva", mensaje_usuario,
                                    respuesta_chatbot)

        return []


class ActionRedirigirEncuesta(Action):
    def name(self) -> Text:
        return "action_redirigir_encuesta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Abre el enlace en el navegador
        url = "https://docs.google.com/forms/d/e/1FAIpQLSctnNrx4mcbVfAepsClb6zoXN3xBwaycCjj70FXPWrt2W8m3A/viewform"
        webbrowser.open_new_tab(url)
        dispatcher.utter_message(text="¡Abriendo encuenta en el navegador!")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = url

        db_utils = DBUtils()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "redirigir_encuenta", mensaje_usuario,
                                    respuesta_chatbot)

        return []


class ActionInformacionPago(Action):
    def name(self) -> Text:
        return "action_info_pago"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        respuesta = dispatcher.utter_message(response="utter_asistencia_pago")

        # Registra la interacción en la base de datos
        nombres_usuario = tracker.get_slot("nombres_usuario")
        correo_usuario = tracker.get_slot("correo_usuario")
        mensaje_usuario = tracker.latest_message['text']
        respuesta_chatbot = respuesta

        db_utils = DBUtils()
        db_utils.insert_interaccion(nombres_usuario, correo_usuario, "Información pagos", mensaje_usuario,
                                    respuesta_chatbot)

        return []





