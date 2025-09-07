<template>
    <div id="upload">
        <div class="loading-status" :class="{ 'fade-in': isLoading || uploadJustFinished }" v-if="isLoading || uploadJustFinished">
            <div class="loading-symbol" :class="{ 'success' : uploadSuccess, 'error' : !uploadSuccess }" v-if="!isLoading"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>

        <div class="inputContainer">
            <h1>Upload DICOM-Dateien</h1>
            <p class="upload-info">Wählen Sie einen Ordner mit DICOM-Dateien (.dcm) zum Hochladen aus.</p>
            <label for="file-upload" class="custom-file-upload">
                <i class="fa fa-folder-open"></i> Ordner auswählen
            </label>
            <input id="file-upload" type="file" webkitdirectory multiple @change="handleFilesUpload">
        </div>

        <div class="results" v-if="selectedFiles.length > 0">
            <h2>Ausgewählte Dateien ({{ selectedFiles.length }})</h2>
            <ul>
                <li v-for="file in selectedFiles" :key="file.name">{{ file.name }}</li>
            </ul>
            <button @click="uploadFiles" :disabled="uploading" class="upload-button">
                {{ uploading ? 'Lade hoch...' : 'Hochladen starten' }}
            </button>
        </div>

        <div class="upload-summary" v-if="uploadSummary">
            <h3>Upload-Ergebnis</h3>
            <p>{{ uploadSummary.message }}</p>
            <div v-if="uploadSummary.failed_uploads && uploadSummary.failed_uploads.length > 0">
                <h4>Fehlgeschlagene Uploads:</h4>
                <ul>
                    <li v-for="fail in uploadSummary.failed_uploads" :key="fail.filename">
                        {{ fail.filename }} - Fehler: {{ fail.error }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
    import {
        ref
    } from 'vue';
    import {
        uploadDicomFiles
    } from '../store/api';

    export default {
        name: 'Upload',
        setup() {
            const selectedFiles = ref([]);
            const uploading = ref(false);
            const isLoading = ref(false);
            const loadingText = ref('');
            const uploadSuccess = ref(false);
            const uploadJustFinished = ref(false);
            const uploadSummary = ref(null);


            const handleFilesUpload = (event) => {
                selectedFiles.value = Array.from(event.target.files).filter(file => file.name.endsWith('.dcm'));
                uploadSummary.value = null; // Reset summary when new files are selected
                if (selectedFiles.value.length === 0) {
                    alert("Bitte wählen Sie einen Ordner aus, der DICOM-Dateien (.dcm) enthält.");
                }
            };

            const uploadFiles = async () => {
                if (selectedFiles.value.length === 0) {
                    alert("Keine DICOM-Dateien zum Hochladen ausgewählt.");
                    return;
                }

                uploading.value = true;
                isLoading.value = true;
                loadingText.value = `Lade ${selectedFiles.value.length} Dateien hoch...`;
                uploadJustFinished.value = false;
                uploadSummary.value = null;


                try {
                    const response = await uploadDicomFiles(selectedFiles.value);
                    uploadSuccess.value = true;
                    loadingText.value = response.message || 'Upload erfolgreich!';
                    uploadSummary.value = response;
                } catch (error) {
                    uploadSuccess.value = false;
                    loadingText.value = error.message || 'Upload fehlgeschlagen!';
                    uploadSummary.value = error.response?.data || { message: 'Ein unerwarteter Fehler ist aufgetreten.' };
                } finally {
                    uploading.value = false;
                    isLoading.value = false;
                    uploadJustFinished.value = true;
                    selectedFiles.value = []; // Clear selection after upload
                    setTimeout(() => {
                        uploadJustFinished.value = false;
                    }, 5000); // Hide status after 5 seconds
                }
            };

            return {
                selectedFiles,
                uploading,
                isLoading,
                loadingText,
                uploadSuccess,
                uploadJustFinished,
                uploadSummary,
                handleFilesUpload,
                uploadFiles,
            };
        },
    };
</script>

<style scoped>
    #upload {
        padding: 2rem;
        text-align: center;
    }

    .inputContainer {
        margin-bottom: 2rem;
    }
    
    .upload-info {
        color: #666;
        margin-bottom: 1.5rem;
    }

    .custom-file-upload {
        border: 1px solid #ccc;
        display: inline-block;
        padding: 10px 18px;
        cursor: pointer;
        background-color: #f9f9f9;
        border-radius: 5px;
        transition: background-color 0.3s;
    }

    .custom-file-upload:hover {
        background-color: #e6e6e6;
    }

    input[type="file"] {
        display: none;
    }

    .results {
        margin-top: 2rem;
        text-align: left;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .results ul {
        list-style-type: none;
        padding: 0;
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }

    .results li {
        padding: 8px;
        border-bottom: 1px solid #eee;
    }

    .upload-button {
        padding: 12px 25px;
        font-size: 1rem;
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .upload-button:disabled {
        background-color: #aaa;
        cursor: not-allowed;
    }

    .upload-button:hover:not(:disabled) {
        background-color: #45a049;
    }

    .loading-status {
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #333;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 1000;
        display: flex;
        align-items: center;
        opacity: 0;
        transition: opacity 0.5s ease-in-out;
    }

    .loading-status.fade-in {
        opacity: 1;
    }
    
    .loading-symbol {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 10px;
    }

    .loading-symbol.success {
        background-color: #4CAF50;
    }

    .loading-symbol.error {
        background-color: #f44336;
    }
    
    .upload-summary {
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        text-align: left;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
