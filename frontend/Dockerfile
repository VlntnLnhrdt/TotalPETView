# Node.js Alpine Image (leichtgewichtig)
FROM node:18-alpine

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY package*.json ./
RUN npm install

# Quellcode kopieren
COPY . .

# Port freigeben (dev server läuft standardmäßig auf 8080)
EXPOSE 8080

# Kommando zum Starten des Devservers (kann in docker-compose.yml überschrieben werden)
CMD ["npm", "run", "dev"]
