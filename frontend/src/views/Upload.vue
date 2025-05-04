<template>
    <div>
      <h1>Upload DICOM-Dateien</h1>
      <input type="file" @change="handleFileUpload">
    </div>
</template>

<script setup>
    const handleFileUpload = (event) => {
        console.log("Datei hochgeladen:", event.target.files[0]);
    };
</script>
