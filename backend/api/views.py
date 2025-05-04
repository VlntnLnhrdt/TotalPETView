from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # Nur nötig, falls kein CSRF-Schutz – hier NICHT genutzt
from django.contrib.auth.decorators import login_required
import requests
import json

ORTHANC_URL = 'http://localhost:8042'  # Orthanc-URL
ORTHANC_AUTH = ('alice', 'alicePassword')  # Falls Basic Auth benötigt wird # FIXME sollte in prod geändert werden

@require_POST
@login_required
def search_patients(request):
    try:
        body = json.loads(request.body)
        query = body.get('query', '').strip()

        if not query:
            return JsonResponse({'error': 'Suchanfrage fehlt'}, status=400)
        
        print(f"Searching for {query}")

        # Suche in Orthanc durchführen
        orthanc_response = requests.post(
            f"{ORTHANC_URL}/tools/find",
            auth=ORTHANC_AUTH,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "CaseSensitive": False,
                "Level": "Patient",
                "Expand": True,
                "Query": {
                    "PatientName": f"*{query}*"
                }
            })
        )


        if orthanc_response.status_code != 200:
            return JsonResponse({'error': 'Fehler bei der Verbindung zu Orthanc'}, status=orthanc_response.status_code)

        patients = orthanc_response.json()

        return JsonResponse(patients, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@login_required
def patient_studies(request, orthancId):
    try:
        orthanc_response = requests.get(
            f"{ORTHANC_URL}/patients/{orthancId}/studies",
            auth=ORTHANC_AUTH,
            headers={'Content-Type': 'application/json'},
            # data=json.dumps({
                
            # })
        )

        if orthanc_response.status_code != 200:
            return JsonResponse({'error': 'Fehler bei der Verbindung zu Orthanc'}, status=orthanc_response.status_code)

        studies = orthanc_response.json()

        return JsonResponse(studies, safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
@login_required
def study_series(request, orthancId):
    try:
        orthanc_response = requests.get(
            f"{ORTHANC_URL}/studies/{orthancId}/series",
            auth=ORTHANC_AUTH,
            headers={'Content-Type': 'application/json'},
        )

        if orthanc_response.status_code != 200:
            return JsonResponse({'error': 'Fehler bei der Verbindung zu Orthanc'}, status=orthanc_response.status_code)

        series = orthanc_response.json()

        return JsonResponse(series, safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_POST
@login_required
def instance_preview(request, orthancId):
    print(orthancId)
    try:
        orthanc_response = requests.get(
            f"{ORTHANC_URL}/instances/{orthancId}/preview",
            auth=ORTHANC_AUTH,
        )

        if orthanc_response.status_code != 200:
            return JsonResponse({'error': 'Fehler bei der Verbindung zu Orthanc'}, status=orthanc_response.status_code)


        return HttpResponse(orthanc_response.content, content_type="image/png")
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)















