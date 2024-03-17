import requests
import json


def verificar_mensaje(mensaje, usuario_id):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "message": mensaje,
        "sender" : usuario_id

    }
    headers = {"Content-Type": "application/json"}

    # Imprimir el JSON antes de enviar la solicitud
    print("JSON enviado al servidor Rasa:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        print("Contenido del cuerpo de la solicitud:")
        print(response_data)
    else:
        print("Error al enviar el mensaje:", response.status_code)


mensaje = "precios"
usuario_id = "123456789"
verificar_mensaje(mensaje, usuario_id)
