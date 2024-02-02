# Utiliza una imagen base de Python
FROM python:3.7

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios (asegúrate de tener tu modelo en la carpeta /models)
COPY ./models /app/models

# Instala las dependencias de RASA
RUN pip install rasa
RUN pip install mysql-connector-python

# Expone el puerto 5005 para la API de RASA
EXPOSE 5005

# Comando para iniciar el servidor RASA
CMD ["rasa", "run", "-m", "models", "--enable-api"]
