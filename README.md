# 1. Projektdokumentation des TotalPETViewers

## 1.1 Projektinformationen

Dieses Projekt wurde im Rahmen des Moduls **Klinisches Anwendungsprojekt** der Technischen Universität München geschaffen. Dieses wurde von mir (Valentin Linhardt) eigenständig geplant, entwickelt und installiert, und ist auf [GitHub](https://github.com/VlntnLnhrdt/TotalPETView) frei verfügbar. Sollte das Projekt hier nicht mehr abrufbar sein, ist das Projekt zudem auf meiner persönlichen Webseite [vlntn.de](vlntn.de) gelistet, oder zumindest sind dort mögliche Kontaktdaten einsehbar.

## 1.2 Projektbeschreibung

Der TotalPETViewer ist ein web-basiertes System zur Verwaltung und Visualisierung von medizinischen Bilddaten im in der Medizin üblichen DICOM-Format. Es ermöglich den Upload, Verwaltung, Suche und die Anzeige von medizinischen Bilddatenen über eine benutzerfreundliche Weboberfläche. Angelehnt an die ursprünglich angedachte integration des Total Segmentator's und den PET-Viewer. Im Rahmen des Projektes wird die Anwendung mit TPV abekürzt.

## 1.3 Projektziel

Ziel des Projekts ist die Entwicklung eines webbasierten DICOM-Viewers zur Darstellung von bis zu vier sequenziellen PET/CT-Scans. Zudem soll eine DICOM-Schnittstelle geschaffen werden, die eine standardisierte Anbindung an externe Systeme ermöglicht. Ursprünglich sollte auch der Total Segmentator zur Organsegmentierung integriert werden, jedoch war dies aus zeittechnischen Gründen nicht möglich.

<div style="page-break-after: always;"></div>

# 2. Anforderungen

Nachfolgend sind die Anforderungen aufgelistet, welche vor Projektbeginn gestellt wurden, als auch im Laufe der Entwicklung hinzukamen.

## 2.1 Funktionale Anforderungen

- [X] Upload von DICOM-Dateien
- [X] Anzeige und Suche von Patienten in einem PACS
- [X] Zugriffskontrolle durch Loginmöglichkeit
- [X] Schaffen einer standardisierten Schnittstelle 
- [ ] Visualisierung von DICOM Dateien im Viewer mit entsprechenden Werkzeugen

## 2.2 Nicht-funktionale Anforderungen

- [X] Performance: Schnelle Ladezeiten für Bilder und Suchergebnisse
- [ ] Sicherheit: Sicher Authentifizierung und verschlüsselte Datenübertragung (letzteres nur durch Systemadministratoren möglich)
- [X] Erweiterbarkeit: Modulare Architektur zur einfache Integration neuer Funktionen

## 2.3 Technische Anforderungen

  - [X] Frontend: React, **Vue.js** oder Angular für eine performante und interaktive UI.
  - [X] Backend: Python (**Django** oder Flask), Node.js oder eine vergleichbare serverseitige Lösung.
  - [ ] DICOM-Verarbeitung: Verwendung von Libraries wie Cornerstone.js, DICOMweb, pydicom oder OHIF Viewer.
  - [X] Datenbank: Speicherung der DICOM-Daten in einer PACS-kompatiblen Lösung wie **Orthanc** oder DCM4CHEE.
  - [ ] TotalSegmentator: Einbindung über eine Python-Backend-Pipeline mit TensorFlow oder PyTorch.
  - [X] Hosting: Lokale oder **cloudbasierte Bereitstellung** (z. B. AWS, Azure, oder On-Premises-Server).


## 2.3 Gründe für unerfüllte Anforderungen

Aufgrund der fehlenden Praxis-Erfahrung mit Django, PACS im Allgemeinen sowie Vuejs, musste ich mehrere Entwicklungsansätze nach zeitintensiver Arbeit wieder verwerfen und größtenteils von Null anfangen. Hierdurch hatte ich gegen Ende der Projektphase zu wenig Zeit meine Implementierungsprobleme mit der Library Cornerstone, welche die Basis für die Darstellung von medizinischen Bildern ist, zu lösen. Daher habe ich mich darauf konzentriert, alles Andere fertig zu bekommen und ordentlich zu implementieren, damit ein möglicher Nachfolger von mir, sich vollständig auf den tatsächlichen Viewer konzentrieren kann.

<div style="page-break-after: always;"></div>

# 3. Architektur

Nachfolgend wir die gesamte Architektur des Projektes beschrieben, um einen detaillierten Überblick über die Struktur zu schaffen. Die einzelnen Komponenten wurden mittels Docker Containern implementiert und über eine gemeinsame Docker-Compose Datei gestartet, um eine systemunabhängige Ausführung zu ermöglichen.

## 3.1 Übersicht

Der TPV besteht aus drei großen Komponenten: Dem PACS, Django Backend, Vuejs Frontend.

Zur Speicherung und Verwaltung der medizinischen Daten wird als PACS "Orthanc" verwendet. Orthanc ist ein kostenloser, open-source leichtgewichtiger DICOM-Server. Auf diesem werden die DICOM Dateien gespeichert, verwaltet und abgerufen.

Für die Weboberfläche wird Vuejs verwendet, ein clientseitiges JavaScript-Webframework zur Erstellung von dynamischen Webanwendungen. Hierüber wird der Anwender ausschließlich mit dem TPV interagieren, ohne direkt auf Orthanc zuzugreifen.

Als Zwischenglied und Backend zwischen diesen beiden Services wird Django, ein high-level Python web framework, eingesetzt. Django kann auch zur Darstellung vom Webseiten genutzt werden, wird im Rahmen dieses Projektes aber als reine Schnittstelle zwischen dem Frontend und Orthanc verwendet, sowie zur Benutzerverwaltung.

## 3.2 Orthanc

TODO: Was ist Orthanc allgemein? Wie wird es in diesem Projekt verwendet? Welche Abfrage werden in diesem Projekt an Orthanc gesendet?

## 3.3 Vuejs

TODO: Was ist vuejs im allgemeinen? Wie wird es in diesem Projekt verwendet? Welche Seiten sind abrufbar?

## 3.4 Django

TODO: Was ist Django im allgemeinen? Wie wird es in diesem Projekt verwendet? Welche Endpunkte sind abrufbar und was machen diese?

<div style="page-break-after: always;"></div>

# 4. Installation

TODO: Hier erklären, wie man das Repo pullt und "installiert" bzw. startet

<div style="page-break-after: always;"></div>

# 5. Benutzung

TODO: Hier kurz einen typischen Usecase-Verlauf erläutern (Anmelden, Daten hochladen, Patienten Suchen, Viewer öffnen)

<div style="page-break-after: always;"></div>

# 6. Abschließende Worte

## 6.1 Sicherheit

## 6.2 Integration in ein KIS

## 6.3 Stabilität und Testing

## 6.4 Meine Meinung zum Projekt