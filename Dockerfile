# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y los instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente de tu proyecto en el contenedor
COPY . .

# Configura las variables de entorno necesarias
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ejecuta las migraciones y recoge los archivos estáticos
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Comando para iniciar el servidor de desarrollo Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
