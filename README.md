# TotalPETView

> Ein Web-basiertes Framework eines DICOM-Viewers mit DICOM-Schnittstelle

## Projektziel

Ziel des Projekts ist die Entwicklung eines webbasierten DICOM-Viewers zur Darstellung von bis zu vier sequenziellen PET/CT-Scans. Zudem soll eine DICOM-Schnittstelle geschaffen werden, die eine standardisierte Anbindung an externe Systeme ermöglicht. Falls die Umsetzung innerhalb eines Monats realistisch ist, soll der Total Segmentator zur Organsegmentierung sowohl im Backend als auch im Frontend integriert werden.

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
