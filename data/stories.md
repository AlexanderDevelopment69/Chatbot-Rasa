## Historia de Bienvenida e Inicio de Conversación

## historia_registro_usuario

* saludar
    - utter_saludar
    - utter_preguntar_nombre
* informar_nombre
    - utter_preguntar_correo
* informar_correo
    - action_store_user_info
    - utter_agradecer_registro

## Historia de Consulta de Servicios después de la Bienvenida

* consultar_servicios
    - utter_consultar_servicios
    - action_consulta_servicios

## Historia de Consulta de precios después de la Bienvenida

* consultar_precios
    - utter_consultar_precios
    - action_consulta_precios

## Historia de Consulta de disponibilidad después de la Bienvenida

* consultar_disponibilidad
    - utter_preguntar_fecha_llegada
* informar_fecha_llegada
    - utter_preguntar_fecha_salida
* informar_fecha_salida
    - utter_consultar_disponibilidad
    - action_consulta_disponibilidad

## Despedida

* despedirse
    - utter_despedida