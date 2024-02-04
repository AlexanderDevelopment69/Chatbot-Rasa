## Historia de Bienvenida e Inicio de Conversación

## historia_registro_usuario

* saludar
    - utter_saludar
    - utter_ask_nombres_usuario
* informar_nombre
    - utter_ask_correo_usuario
* informar_correo
    - action_store_user_info
    - utter_agradecer_registro
    - utter_inicio_conversacion

## Historia de Consulta de Servicios

* consultar_servicios
    - utter_consultar_servicios
    - action_consulta_servicios
    - action_mostrar_boton_continuar_conversacion



## Historia de Consulta de precios

* consultar_precios
    - utter_consultar_precios
    - action_consulta_precios
    - action_mostrar_boton_continuar_conversacion

## Historia de Consulta de habitaciones

* consultar_habitaciones
    - utter_consultar_habitaciones
    - action_consulta_habitaciones
    - action_mostrar_boton_continuar_conversacion

## consultar costos de tipo de habitaciones por evento
* consultar_costo_tipo_habitaciones_evento
  - utter_consultar_costo_habitaciones_evento
  - action_consulta_costo_habitaciones_evento
  - action_mostrar_boton_continuar_conversacion



## Historia de Consulta de disponibilidad

* consultar_disponibilidad
    - utter_preguntar_fecha_llegada
* informar_fecha_llegada
    - utter_preguntar_fecha_salida
* informar_fecha_salida
    - utter_consultar_disponibilidad
    - action_consulta_disponibilidad
    - action_mostrar_boton_continuar_conversacion

## Despedida

* despedirse
    - utter_despedida

## story_reserva

* reserva
    - action_mostrar_botones_reserva

## Redirigir_wsp

* redirigir_wsp
    - action_redirigir_wsp
    - action_mostrar_boton_continuar_conversacion

## Redirigir_reserva

* redirigir_reserva
    - action_redirigir_reserva
    - action_mostrar_boton_continuar_conversacion

## story_encuesta

* encuesta
    - action_mostrar_boton_encuesta

## Redirigir_Encuesta

* redirigir_encuesta
    - action_redirigir_encuesta

## Redirigir_cotinuar_conversacion

* redirigir_continuar_conversacion
    - action_redirigir_continuar_conversacion

## Redirigir_no

* redirigir_no
    - action_mostrar_boton_encuesta
    - utter_despedida

## story_asistencia_pago

* asistencia_pago
    - action_info_pago
    - action_mostrar_boton_continuar_conversacion

## Consulta de Registro y Salida

* consultar_registro_salida
    - utter_consulta_registro_salida
    - action_mostrar_boton_continuar_conversacion

## Consulta de Depósito

* consultar_deposito
    - utter_consulta_deposito
    - action_mostrar_boton_continuar_conversacion

## Consulta de Cancelaciones

* consultar_cancelaciones
    - utter_consulta_cancelaciones
    - action_mostrar_boton_continuar_conversacion

## Consulta de Política de Edad

* consultar_politica_edad
    - utter_consulta_politica_edad
    - action_mostrar_boton_continuar_conversacion

## Consulta de Cargo por Daños

* consultar_cargo_danios
    - utter_consulta_cargo_danios
    - action_mostrar_boton_continuar_conversacion

## Consulta de Política de Limpieza

* consultar_limpieza
    - utter_consulta_limpieza
    - action_mostrar_boton_continuar_conversacion

## Consulta de Restricciones de Bebidas Alcohólicas

* consultar_restricciones_bebidas
    - utter_consulta_restricciones_bebidas
    - action_mostrar_boton_continuar_conversacion

## Consulta de Horario de Silencio

* consultar_horario_silencio
    - utter_consulta_horario_silencio
    - action_mostrar_boton_continuar_conversacion

## Consulta de Mascotas

* consultar_mascotas
    - utter_consulta_mascotas
    - action_mostrar_boton_continuar_conversacion

## Consulta de Comportamiento Inapropiado

* consultar_comportamiento_inapropiado
    - utter_consulta_comportamiento_inapropiado
    - action_mostrar_boton_continuar_conversacion

## Consulta de Perdidas

* consultar_perdidas
    - utter_consulta_perdidas
    - action_mostrar_boton_continuar_conversacion
