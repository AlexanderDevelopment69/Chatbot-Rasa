# Chatbot-Rasa
# instalar rasa
pip install rasa==2.8.17 
# instalar complemento conector con base de datos 
mysql-connector-python 
# corre las acciones
rasa run actions 
# habilita la api para consumir en otra aplicaciones
rasa run --enable-api --cors "*" --debug  