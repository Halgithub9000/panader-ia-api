# Usa una imagen base de Python oficial
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto en el que Uvicorn se ejecutará
# Cloud Run espera que tu aplicación escuche en el puerto $PORT
# que le proporciona la variable de entorno. Por defecto es 8080.
EXPOSE 8080

# Comando para ejecutar la aplicación con Uvicorn
# El puerto se obtiene de la variable de entorno $PORT proporcionada por Cloud Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
# Si prefieres que el puerto sea dinámico basado en la var de entorno $PORT:
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]