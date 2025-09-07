import { getCSRFToken } from "./auth"

const apiURL = "http://localhost:8000/api"

export async function getPatientData(patientOrthancId) {
    try {
        const response = await fetch(apiURL + '/patient/' + patientOrthancId, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Fehler beim Abrufen des Patienten: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Fehler bei der Patientabfrage:', error)
      throw error
    }
}

export async function searchPatients(query) {
    try {
        const response = await fetch(apiURL + '/patient/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify({ query }),
      })
  
      if (!response.ok) {
        throw new Error(`Fehler beim Abrufen der Patienten: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Fehler bei der Patientensuche:', error)
      throw error
    }
}

export async function getPatientStudies(patientOrthancId) {
    try {
        const response = await fetch(apiURL + '/patient/' + patientOrthancId + '/studies', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Fehler beim Abrufen der Patienten: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Fehler bei der Patientensuche:', error)
      throw error
    }
}

export async function getStudySeries(studyOrthancId) {
    try {
        const response = await fetch(apiURL + '/study/' + studyOrthancId + '/series', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Fehler beim Abrufen der Study: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Fehler bei der Seriensuche:', error)
      throw error
    }
}

export async function getPatientSeries(patientOrthancId) {
    try {
        const response = await fetch(apiURL + '/patient/' + patientOrthancId + '/series', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Fehler beim Abrufen der Series: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Fehler bei der Seriensuche:', error)
      throw error
    }
}

export async function getPreview(instanceOrthancId) {
    try {
        const response = await fetch(apiURL + '/instance/' + instanceOrthancId + '/preview', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Fehler beim Abrufen der Preview: ${response.status}`)
      }

      const blob = await response.blob()
  
      return URL.createObjectURL(blob)
    } catch (error) {
      console.error('Fehler beim Laden Previews:', error)
      throw error
    }
}

export function getDicomFileUrl(instanceOrthancId) {
  return `${apiURL}/instance/${instanceOrthancId}/file`
}


export async function uploadDicomFiles(files) {
  const formData = new FormData();
  // Vue 3 ref object -> .value
  files.forEach(file => {
      formData.append('files', file);
  });

  try {
      const response = await fetch(`${apiURL}/upload`, {
          method: 'POST',
          headers: {
              // 'Content-Type': 'multipart/form-data' wird vom Browser automatisch mit Boundary gesetzt
              'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: formData
      });

      const data = await response.json();

      if (!response.ok) {
          // Wir werfen einen Fehler, der die Server-Antwort enthält
          const error = new Error(data.message || 'Fehler beim Hochladen');
          error.response = { data }; // Hängen die Daten für die UI an den Fehler an
          throw error;
      }

      return data;
  } catch (error) {
      console.error('Fehler beim Hochladen der Daten:', error);
      // Stellen sicher, dass der Fehler weitergeworfen wird, damit die UI ihn fangen kann
      throw error;
  }
}