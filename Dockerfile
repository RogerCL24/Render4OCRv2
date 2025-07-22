FROM python:3.10-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y poppler-utils

# Crea directorio de la app
WORKDIR /app

# Copia código y dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto (opcional)
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]
