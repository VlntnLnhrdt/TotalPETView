# Projektdokumentation: TotalPETView

## 1. Allgemeine Projektdaten

### 1.1 Titel: TotalPETView

Angelehnt an die ursprünglich angedachte integration des Total Segmentator's und den PET-Viewer. Im Rahmen des Projektes wird die Anwendung mit TPV abekürzt.

### 1.2 Projektbeschreibung

Der TotalPETViewer ist ein web-basiertes System zur Verwaltung und Visualisierung von medizinischen Bilddaten im in der Medizin üblichen DICOM-Format. Es ermöglich den Upload, Verwaltung, Suche und die Anzeige von medizinischen Bilddatenen über eine benutzerfreundliche Weboberfläche.

### 1.3 Projektziel

Ziel des Projekts ist die Entwicklung eines webbasierten DICOM-Viewers zur Darstellung von bis zu vier sequenziellen PET/CT-Scans. Zudem soll eine DICOM-Schnittstelle geschaffen werden, die eine standardisierte Anbindung an externe Systeme ermöglicht. Ursprünglich sollte auch der Total Segmentator zur Organsegmentierung integriert werden, jedoch war dies aus zeittechnischen Gründen nicht möglich.

## 2. Anforderungen

Nachfolgend sind die Anforderungen aufgelistet, und auch ob diese erfüllt wurden.

### 2.1 Funktionale Anforderungen

- [X] Upload von DICOM-Dateien
- [X] Anzeige und Suche von Patienten in einem PACS
- [X] Zugriffskontrolle durch Loginmöglichkeit
- [ ] Visualisierung im Viewer mit entsprechenden Werkzeugen

### 2.2 Nicht-funktionale Anforderungen

- [X] Performance: Schnelle Ladezeiten für Bilder und Suchergebnisse
- [ ] Sicherheit: Sicher Authentifizierung und verschlüsselte Datenübertragung (letzteres nur durch Systemadministratoren möglich)
- [X] Erweiterbarkeit: Modulare Architektur zur einfache Integration neuer Funktionen


### 2.3 Gründe für unerfüllte Anforderungen

Aufgrund der fehlenden Praxis-Erfahrung mit Django, PACS im Allgemeinen sowie Vuejs, musste ich mehrere Entwicklungsansätze nach stundenlanger Arbeit wieder verwerfen und größtenteils von Null anfangen. Hierdurch hatte ich gegen Ende der Projektphase zu wenig Zeit meine Implementierungsprobleme mit der Library Cornerstone, welche die Basis für die Darstellung von medizinischen Bildern ist, zu lösen. Daher habe ich mich darauf konzentriert, alles Andere fertig zu bekommen und ordentlich zu implementieren, damit ein möglicher Nachfolger von mir, sich vollständig auf den tatsächlichen Viewer konzentrieren kann.

## 3. Architektur

Nachfolgend wir die gesamte Architektur des Projektes beschrieben, um einen detaillierten Überblick über die Struktur zu schaffen.

### 3.1 Übersicht

Der TPV besteht aus drei großen Komponenten: Dem PACS, Django Backend, Vuejs Frontend.

Zur Speicherung und Verwaltung der medizinischen Daten wird als PACS "Orthanc" verwendet. Orthanc ist ein kostenloser, open-source leichtgewichtiger DICOM-Server. Auf diesem werden die DICOM Dateien gespeichert und entsprechend abgerufen.

Für die Weboberfläche wird Vuejs verwendet, ist ein clientseitiges JavaScript-Webframework zur Erstellung von Webanwendungen. Hierüber wird der Anwender ausschließlich mit dem TPV interagierend.

Als Zwischenglied und Backend zwischen diesen beiden Services wird Django, ein high-level Python web framework, eingesetzt. Django kann auch zur Darstellung vom Webseiten genutzt werden, wird im Rahmen dieses Projektes aber als reine Schnittstelle zwischen dem Frontend und Orthanc verwendet, sowie zur Benutzerverwaltung.

### 3.2 Orthanc

## Projektumfang

1. Entwicklung eines webbasierten DICOM-Viewers
    - Implementierung einer Benutzeroberfläche zur Visualisierung von DICOM- Daten.
    - Unterstützung für mehrere (bis zu vier) sequenzielle PET/CT-Scans pro Patient.
    - Möglichkeit zur parallelen Darstellung und Überlagerung der Scans.
    - Integration grundlegender Bildbearbeitungsfunktionen (Zoom, Kontrastanpassung, Schichtnavigation).
2. Erstellung einer DICOM-Schnittstelle
    - Implementierung einer serverseitigen Schnittstelle zur Verarbeitung von DICOM-Dateien.
    - Unterstützung für den DICOM-Standard (DICOMweb oder DICOM C-Store).
    - Upload-, Abruf- und Speicherfunktionen für PET/CT-Daten.
    - Einbindung eines PACS (Picture Archiving and Communication System) zur Datenspeicherung und -verwaltung.
3. Integration des TotalSegmentators (optional, falls zeitlich möglich)
    - Implementierung des TotalSegmentators im Backend zur automatisierten Organsegmentierung.
    - Bereitstellung der Segmentierungsergebnisse für die Visualisierung im Frontend.
    - Overlay-Funktion für segmentierte Organe zur verbesserten Analyse.
    - Optimierung der Performance für eine flüssige Darstellung der segmentierten Organe.
  
## Technische Anforderungen

  - Frontend: React, Vue.js oder Angular für eine performante und interaktive UI.
  - Backend: Python (Django oder Flask), Node.js oder eine vergleichbare serverseitige Lösung.
  - DICOM-Verarbeitung: Verwendung von Libraries wie Cornerstone.js, DICOMweb, pydicom oder OHIF Viewer.
  - Datenbank: Speicherung der DICOM-Daten in einer PACS-kompatiblen Lösung wie Orthanc oder DCM4CHEE.
  - TotalSegmentator: Einbindung über eine Python-Backend-Pipeline mit TensorFlow oder PyTorch.
  - Hosting: Lokale oder cloudbasierte Bereitstellung (z. B. AWS, Azure, oder On-Premises-Server).

> Dieses Projekt ermöglicht eine effiziente und benutzerfreundliche Betrachtung von PET/CT-
Scans und kann zukünftig weiter ausgebaut werden.
