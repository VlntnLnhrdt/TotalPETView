from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # Nur nötig, falls kein CSRF-Schutz – hier NICHT genutzt
from django.contrib.auth.decorators import login_required
import requests
import json

ORTHANC_URL = 'http://orthanc:8042'  # Orthanc-URL
ORTHANC_AUTH = ('alice', 'alicePassword')  # Falls Basic Auth benötigt wird # FIXME sollte in prod geändert werden

# Retrieves the patient data from orthanc
@login_required
def get_patient_data(request, orthancId):
    try:
        orthanc_response = requests.get(
            f"{ORTHANC_URL}/patients/{orthancId}",
            auth=ORTHANC_AUTH,
            headers={'Content-Type': 'application/json'},
        )

        if orthanc_response.status_code != 200:
            return JsonResponse({'error': 'Fehler bei der Verbindung zu Orthanc'}, status=orthanc_response.status_code)

        patient = orthanc_response.json()

        return JsonResponse(patient, safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Retrieves the patient search results
@require_POST
@login_required
def search_patients(request):
    print("hallo welt")
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

        print("Orthanc Rsponse:")
        print(orthanc_response.json())


        if orthanc_response.status_code != 200:
            return JsonResponse({'error': 'Fehler bei der Verbindung zu Orthanc'}, status=orthanc_response.status_code)

        patients = orthanc_response.json()

        return JsonResponse(patients, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Retrieves the patient's studies from orthanc
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

# Retrieves the study's series from orthanc
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
    
# Retrieves the patient's series from orthanc
@login_required
def patient_series(request, orthancId):
    try:
        orthanc_response = requests.get(
            f"{ORTHANC_URL}/patients/{orthancId}/series",
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
    
# Retrieves the preview of a given instance
@login_required
def instance_preview(request, orthancId):
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

# Legacy code but is being kept as a possible starting point for future development
# @require_POST
# @login_required
# def instance_file(request, instance_id):
#     print("instance file request ###############################################")
#     try:
#         orthanc_response = requests.get(
#             f"{ORTHANC_URL}/instances/{instance_id}/file",
#             auth=ORTHANC_AUTH,
#             stream=True
#         )

#         if orthanc_response.status_code != 200:
#             return JsonResponse({'error': 'Fehler bei der Verbindung zu ORthanc'}, status=orthanc_response.status_code)
        
#         response['Content-Disposition'] = f'inline; filename="{instance_id}.dcm"'
#         return response 

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# uploads dicom files to orthanc
@require_POST
@login_required
def upload_dicom_files(request):
    if not request.FILES:
        return JsonResponse({'error': 'Keine Dateien zum Hochladen gefunden'}, status=400)

    files = request.FILES.getlist('files')
    successful_uploads = []
    failed_uploads = []

    for file in files:
        try:
            # Datei an Orthanc senden
            orthanc_response = requests.post(
                f"{ORTHANC_URL}/instances",
                auth=ORTHANC_AUTH,
                headers={'Content-Type': 'application/dicom'},
                data=file.read()
            )

            if orthanc_response.status_code == 200:
                successful_uploads.append(file.name)
            else:
                failed_uploads.append({
                    'filename': file.name,
                    'status': orthanc_response.status_code,
                    'error': orthanc_response.text
                })
        except Exception as e:
            failed_uploads.append({
                'filename': file.name,
                'error': str(e)
            })

    if not failed_uploads:
        return JsonResponse({
            'message': f'{len(successful_uploads)} Dateien erfolgreich hochgeladen.',
            'successful_uploads': successful_uploads
        }, status=200)
    else:
        return JsonResponse({
            'message': 'Einige Dateien konnten nicht hochgeladen werden.',
            'successful_uploads': successful_uploads,
            'failed_uploads': failed_uploads
        }, status=207) # Multi-Status














