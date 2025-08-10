# Projektdokumentation: [Titel des Projekts]

## 1. Einleitung
### 1.1 Projektziel
Beschreibe kurz, was dein Projekt macht und welchen Zweck es erfüllt.

### 1.2 Motivation
Warum hast du Django, Orthanc und Vue.js gewählt?

### 1.3 Use Case
Wer nutzt das System und in welchem Szenario?

---

## 2. Anforderungen
### 2.1 Funktionale Anforderungen
- [ ] Upload von DICOM-Dateien
- [ ] Anzeige und Suche in PACS
- [ ] Visualisierung im Viewer
- [ ] Benutzerverwaltung

### 2.2 Nicht-funktionale Anforderungen
- [ ] Performance
- [ ] Sicherheit
- [ ] Erweiterbarkeit

---

## 3. Architektur
### 3.1 Architekturübersicht
*Diagramm einfügen (Backend ↔ Orthanc ↔ Frontend)*

### 3.2 Technologiestack
- **Backend**: Django, Django REST Framework
- **PACS**: Orthanc
- **Frontend**: Vue.js
- **Weitere Tools**: Docker, Axios, etc.

### 3.3 Kommunikationsfluss
Beschreibe den Weg einer Datei von Upload bis Anzeige.

---

## 4. Installation & Setup
### 4.1 Voraussetzungen
- Python >= 3.x
- Node.js >= 18.x
- Orthanc installiert
- Optional: Docker

### 4.2 Installationsschritte
```bash
# Backend installieren
pip install -r requirements.txt
python manage.py migrate

# Frontend installieren
cd frontend
npm install

# Orthanc starten (lokal oder via Docker)
```

### 4.3 Starten der Anwendung
```bash
# Backend
python manage.py runserver

# Frontend
npm run dev
```

---

## 5. Backend (Django)
### 5.1 Projektstruktur
```
backend/
    manage.py
    settings.py
    apps/
        api/
        auth/
```

### 5.2 API-Endpunkte
| Endpoint        | Methode | Beschreibung         | Auth erforderlich |
|-----------------|---------|----------------------|-------------------|
| `/api/upload/`  | POST    | DICOM-Upload         | Ja                |
| `/api/search/`  | GET     | Suche nach Scans     | Ja                |

### 5.3 Integration mit Orthanc
Beschreibe die REST-API-Aufrufe und ggf. Plugins.

### 5.4 Datenbankmodell
*ER-Diagramm oder Models zeigen*

---

## 6. PACS (Orthanc)
### 6.1 Konfiguration
- Speicherpfad
- API-Settings
- Zugriffskontrolle

### 6.2 Verbindung zu Django
Beschreibe, wie Django mit Orthanc spricht (REST-Aufrufe, Auth).

### 6.3 Beispiel-API-Aufruf
```bash
curl -X POST http://localhost:8042/instances --data-binary @image.dcm
```

---

## 7. Frontend (Vue.js)
### 7.1 Projektstruktur
```
frontend/
    src/
        components/
        views/
        router.js
```

### 7.2 Routing
- `/upload` – Upload-Seite
- `/viewer/:id` – Viewer für DICOM-Dateien

### 7.3 Komponenten
- Upload-Komponente
- Suchliste
- Viewer

### 7.4 Kommunikation mit Backend
Beispiel mit Axios:
```javascript
axios.post('/api/upload/', formData, { headers: { 'Authorization': 'Bearer ...' } })
```

---

## 8. Sicherheit
- Authentifizierung (Django-Auth, JWT, Session)
- Rechtekonzept
- Schutz vor CSRF, XSS, SQL Injection

---

## 9. Deployment
- Umgebungen: Development, Staging, Production
- Docker-Setup
- Logging & Monitoring

---

## 10. Bekannte Probleme & Grenzen
- Feature XYZ noch nicht implementiert
- Performance bei großen Dateien

---

## 11. Ausblick
- Erweiterter Viewer
- KI-gestützte Analyse
- Cloud-Speicherung

---

## 12. Anhang
- API-Schema (Swagger/OpenAPI)
- Beispielkonfigurationsdateien (`settings.py`, `orthanc.json`)
- Codebeispiele
