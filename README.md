# Chatbot-Rasa
# instalar rasa
pip install rasa==2.8.17 
# instalar complemento conector con base de datos 
pip install mysql-connector-python
# corre las acciones
rasa run actions 
# Habilita la api del modelo entrenado
rasa run --enable-api --cors "*" --debug  