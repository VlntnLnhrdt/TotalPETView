# Offizielles Python 3.11 slim Image
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY . .

# Port freigeben (Django-Devserver)
EXPOSE 8000

# Kommando zum Starten des Devservers (kann in docker-compose.yml überschrieben werden)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
