<template>
    <div id="upload">
        <div class="loading-status" :class="{ 'fade-away': !isLoading}">
            <div class="loading-symbol" :class="{ 'success' : !isLoading && loadingResult, 'error' : !isLoading && !loadingResult }"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>

        <div class="inputContainer">
            <h1>Upload DICOM-Dateien</h1>
            <input type="file" webkitdirectory multiple @change="handleFilesUpload">
        </div>

        <div class="results">
            
        </div>
    </div>

    <div v-if="uploading"></div>
</template>

<script>
    import {
        useAuthStore
    } from '../store/auth'
    import {
        uploadDicomFiles
    } from '../store/api';

    export default{
        setup() {
            const authStore = useAuthStore()

            return {
                authStore
            }
        },
    }
</script>
