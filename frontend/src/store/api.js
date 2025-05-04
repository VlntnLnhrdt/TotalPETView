import { getCSRFToken } from "./auth"

const apiURL = "http://localhost:8000/api"

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
        method: 'POST',
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
        method: 'POST',
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

export async function getPreview(instanceOrthancId) {
    try {
        const response = await fetch(apiURL + '/instance/' + instanceOrthancId + '/preview', {
        method: 'POST',
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