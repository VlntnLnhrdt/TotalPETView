<template>
    <div id="viewer">
        <div class="loading-status" :class="{ 'fade-away': !isLoading}">
            <div class="loading-symbol" :class="{ 'success' : !isLoading && loadingResult, 'error' : !isLoading && !loadingResult }"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>
            
        <div class="toolbar">
            <div class="category">
                <div class="tool" @click="newWorkSpace">
                    <img src="../assets/images/toolbar/newWorkspaceIcon.png" alt="NewWorkspace Icon" title="Öffnet ein neues Fenster mit dem selben Inhalt">
                </div>
            </div>
        </div>

        <div class="workspace">

            <div class="studylist">
                <div v-if="patientData" class="patientInfo">
                    <p>#{{ patientData.MainDicomTags.PatientID }} - {{ patientData.MainDicomTags.PatientName }}</p>
                    <p>Geb. {{ formatDate(patientData.MainDicomTags.PatientBirthDate) }}</p>
                </div>

                <div v-if="patientData" class="study" v-for="study in studies" :class="{ 'notOpen': openStudies.includes(study) }">
                    <div class="studyInfo" @click="toggleStudy(study)">
                        <p>Datum - {{ formatDate(study.MainDicomTags.StudyDate) }}</p>
                        <p>Beschreibung - {{ study.MainDicomTags.StudyDescription }}</p>
                    </div>

                    <div class="series">
                        <div class="serie" v-for="serieId in study.Series" :key="serieId" draggable="true" @dragstart="onDragStart(serieId)">
                            <div class="preview" v-if="seriesMap[serieId]">
                                <img v-if="previews[seriesMap[serieId].Instances[0]]"
                                    :src="previews[seriesMap[serieId].Instances[0]]"
                                    alt="Serie-Preview">
                            </div>
                            <div class="description" v-if="seriesMap[serieId]">
                                <p>{{ seriesMap[serieId].MainDicomTags.SeriesDescription || '_' }} - {{ seriesMap[serieId].MainDicomTags.PerformedProcedureStepDescription || 'Unbekannt' }}</p>
                                <p class="prod">{{ seriesMap[serieId].MainDicomTags.ProtocolName || 'Unbekannt' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="dicom-viewer" class="viewport">
                <div id="viewport-1" class="viewbox" @dragover.prevent @drop="onDrop('viewport-1')"></div>
            </div>
        </div>

    </div>
</template>

<script>
    import {
        useAuthStore
    } from '../store/auth'
    import {
        getPatientData,
        getPatientStudies,
        getPatientSeries,
        getPreview,
        getDicomFileUrl
    } from '../store/api'
    import {
        formatDate,
        setLoadingStatus
    } from '../store/utils'

    // Cornerstone Imports

    export default {
        setup() {
            const authStore = useAuthStore()
            return {
                authStore
            }
        },
        data () {
            return {
                isLoading: false,
                loadingText: 'Willkommen',
                loadingResult: true,
                patientId: '',
                patientData: null,
                studies: [],
                openStudies: [],
                seriesMap: {},
                previews: {},
                draggedSerie: null,
            }
        },
        mounted() {
            this.patientId = this.$route.query.patient
            this.loadPatientData()
            this.loadPatientStudies()
            this.loadPatientSeries()
        },
        methods: {
            async loadPatientData() {

                setLoadingStatus(this, true, "Lade Patientendaten", true)

                if (!this.patientId) {
                    console.error("Keine Patienten-Id gefunden")
                    setLoadingStatus(this, false, "Keine Patienten-Id gefunden", false)
                    return
                }

                try {
                    const data = await getPatientData(this.patientId)
                    this.patientData = data
                    setLoadingStatus(this, false, "Patientendaten erfolgreich geladen", true)
                } catch (error) {
                    console.error("Fehler beim Laden der Patientendaten:", error)
                    setLoadingStatus(this, false, "Fehler beim Laden der Patientendaten", false)
                }
            },
            async loadPatientStudies() {
                setLoadingStatus(this, true, "Lade Studien", true)
                try {
                    const response = await getPatientStudies(this.patientId)
                    this.studies = response
                    setLoadingStatus(this, false, "Studien erfolgreich geladen", true)
                } catch (error) {
                    console.error('Fehler bei Studiensuche:', error)
                    this.studies = []
                    setLoadingStatus(this, false, "Studien konnten nicht geladen werden", false)
                }

            },
            async loadPatientSeries() {
                setLoadingStatus(this, true, "Lade Series", true)

                this.seriesMap = {}

                try {
                    const response = await getPatientSeries(this.patientId)

                    for (const serie of response) {
                        const id = serie.ID
                        if (id) {
                            this.seriesMap[id] = serie
                        } else {
                            console.error('Serie hat keine ID', serie[0])
                        }
                    }

                    console.log('Serien:', response);
                    console.log('SeriesMap:', this.seriesMap);

                    setLoadingStatus(this, false, "Series erfolgreich geladen", true)

                    this.loadPreviewUrls()

                } catch (error) {
                    console.error('Fehler bei Seriessuche:', error)
                    this.seriesMap = {}
                    setLoadingStatus(this, false, "Series konnten nicht geladen werden", false)
                }
            },
            async loadPreviewUrls() {
                setLoadingStatus(this, true, "Lade Previews", true)

                const previewPromises = []

                for (const id in this.seriesMap) {
                    const serie = this.seriesMap[id]
                    const instanceId = serie.Instances[0]
                    if (instanceId) {

                        const promise = getPreview(instanceId)
                            .then(blobUrl => {
                                this.previews[instanceId] = blobUrl
                            })
                            .catch(error => {
                                console.error('Laden der Previews fehlgeschlagen:', e);
                            setLoadingStatus(this, false, "Laden der Preview von Instance" + instanceId + " fehlgeschlagen", false)
                            })
                        previewPromises.push(promise)
                    }
                } 

                try {
                    await Promise.all(previewPromises)
                    setLoadingStatus(this, false, "Previews wurden erfolgreich geladen", true)
                } catch {
                    setLoadingStatus(this, false, "Laden der Previews fehlgeschlagen", false)
                }
            },
            toggleStudy(study) {
                const index = this.openStudies.findIndex(s => s.ID === study.ID)
                if (index !== -1) {
                    this.openStudies.splice(index, 1)
                } else {
                    this.openStudies.push(study)
                }
            },

            // The following are the functions used only for the DragAndDrop
            onDragStart(serieId) {
                this.draggedSerie = serieId
            },
            onDrop(viewportId) {
                const serieId = this.draggedSerie
                if (serieId && this.seriesMap[serieId]) {
                    console.log("Serie", serieId, " in viewport ", viewportId, " gelegt", this.seriesMap[serieId])
                }

                this.initViewport(viewportId, this.seriesMap[serieId])
                this.draggedSerie = null
            },
            

            // The following are the function used in the toolbar
            newWorkSpace() {
                const features = 'height=0,width=0,scrollbars=yes,status=yes'
                window.open(window.location.href, '_blank', features)
            },

            async initViewport(viewportid, serie) {

            },


            // Calls the formatDate in Utils.js
            formatDate(dateString) {
                return formatDate(dateString)
            }
        },
    }
</script>