# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
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
        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Disponibilidad", mensaje_usuario, respuesta_chatbot)

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
        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Precios", mensaje_usuario, respuesta_chatbot)

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
        db_utils2.insert_interaccion(nombres_usuario, correo_usuario, "Consulta_Servicios", mensaje_usuario, respuesta_chatbot)

        return []