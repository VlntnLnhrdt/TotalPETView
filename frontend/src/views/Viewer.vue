<template>
    <div id="viewer">
        <div class="loading-status" :class="{ 'fade-away': !isLoading}">
            <div class="loading-symbol" :class="{ 'success' : !isLoading && loadingResult, 'error' : !isLoading && !loadingResult }"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>
            
        <div class="toolbar">
            <p>Werkzeugleiste</p>
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
                        <div class="serie" v-for="serie in study.Series" @click="addSeries(serie)">
                            <div class="preview">
                                <img :src="'http://localhost:8042/instances/' + serie.Instances[0].OrthancID + '/preview'" alt="Serie-Preview">
                            </div>
                            <div class="description">
                                <p>{{ serie.SeriesNumber || '_' }} - {{ serie.Modality || 'Unbekannt' }}</p>
                                <p class="prod">{{ serie.Manufacturer || 'Unbekannt' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="dicom-viewer" class="viewport">
                <div id="viewport-1" class="viewbox"></div>
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
        getPatientSeries
    } from '../store/api';
    // import {
    //     formatDate,
    //     setLoadingStatus
    // } from '../store/utils'


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
                studies: null,
                openStudies: [],
                series: null,
                previews: {},
            }
        },
        mounted() {
            this.patientId = this.$route.query.patient,
            this.loadPatientData(),
            this.loadPatientStudies(),
            this.loadPatientSeries()
        },
        methods: {
            async loadPatientData() {

                if (!this.patientId) {
                    console.error("Keine Patienten-Id gefunden")
                    return
                }

                this.setLoadingStatus(this, true, "Lade Patientendaten")

                try {
                    const data = await getPatientData(this.patientId)
                    this.patientData = data
                    this.setLoadingStatus(false, "Patientendaten geladen")
                } catch (error) {
                    console.error("Fehler beim Laden der Patientendaten:", error)
                    this.setLoadingStatus(false, "Fehler beim Laden", false)
                }
            },
            async loadPatientStudies() {
                this.setLoadingStatus(true, "Lade Studien")
                try {
                    const response = await getPatientStudies(this.patientId)
                    this.studies = response
                    this.setLoadingStatus(false, "Studien geladen")
                } catch (error) {
                    console.error('Fehler bei Studiensuche:', error)
                    this.studies = []
                    this.setLoadingStatus(false, "Studien konnten nicht geladen werden", false)
                }

            },
            async loadPatientSeries() {
                this.setLoadingStatus(true, "Lade Series")
                try {
                    const response = await getPatientSeries(this.patientId)
                    this.series = response
                    this.setLoadingStatus(false, "Series geladen")
                } catch (error) {
                    console.error('Fehler bei Seriessuche:', error)
                    this.series = []
                    this.setLoadingStatus(false, "Series konnten nicht geladen werden", false)
                }
            },

            // The following are helper-functions
            formatDate(dateString) {
                if (!dateString) return ""
                return `${dateString.slice(6, 8)}.${dateString.slice(4, 6)}.${dateString.slice(0, 4)}`
            },
            setLoadingStatus(status, text, result=true) {
                this.isLoading = status
                this.loadingText = text
                this.loadingResult = result
            }
        },
    }
</script>