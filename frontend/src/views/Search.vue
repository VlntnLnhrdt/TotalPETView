<template>
    <div id="search">
        <div class="loading-status" :class="{ 'fade-away': !isLoading}">
            <div class="loading-symbol" :class="{ 'success' : !isLoading && loadingResult, 'error' : !isLoading && !loadingResult }"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>

        <div class="searchbar">
            <img src="../assets/images/searchicon.png" alt="Searchicon">
            <input
                type="text"
                v-model="query"
                @input="searchPatients"
                placeholder="Max, Mustermann, G:15.03.1997, BF:Freitext"
                autofocus/>
        </div>

        <div class="filterandcontent">

            <div class="searchfilters">
                <p>Hier kommen weitere Filter und ggf. Informationen rein.</p>
            </div>

            <div class="searchresults" >                
                <div class="resultlist">
                    <div class="headrow">
                        <p>Patienten-ID</p>
                        <p>Name</p>
                        <p>Geburtsdatum</p>
                        <p>Geschlecht</p>
                        <p>Letzte Änderung</p>
                    </div>

                    <div v-if="patients.length == 0">
                        <p class="noResultsText">Keine passenden Ergebnisse gefunden.</p>
                    </div>

                    <div v-for="patient in patients" :key="patient.ID"
                        class="patient" 
                        @click="selectPatient(patient.ID)"
                        @dblclick="loadViewer(patient.ID)"
                        :class="{ 'active': activePatient === patient }">

                        <div class="patientInfo">
                            <p>{{ patient.MainDicomTags.PatientID }}</p>
                            <p>{{ patient.MainDicomTags.PatientName }}</p>
                            <p>{{ formatDate(patient.MainDicomTags.PatientBirthDate) }}</p>
                            <p>{{ patient.MainDicomTags.PatientSex }}</p>
                            <p>{{ formatDate(patient.LastUpdate) }}</p>
                        </div>

                        <div v-if="activePatient === patient.ID"
                            class="studies">

                            <div class="studyHead">
                                <p class="listhead">Datum</p>
                                <p class="listhead">Beschreibung</p>
                            </div>
                            
                            <div v-for="study in studies" :key="study.OrthancID"
                                class="study" 
                                @click.stop="selectStudy(study)"
                                :class="{ 'active': activeStudy === study.ID }">

                                <div class="studyInfo">
                                    <p>{{ formatDate(study.MainDicomTags.StudyDate) || 'Kein Datum' }}</p>
                                    <p>{{ study.MainDicomTags.StudyDescription || 'Keine Beschreibung' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>   
                </div>

                <div class="seriesResults">
                    <p class="seriesHead">Studie: {{ activeStudy ? activeStudy.MainDicomTags.StudyDescription || 'Keine Beschreibung' : 'Keine Studie ausgewählt'}}</p>

                    <div v-if="activeStudy" class="series">
                        <div v-for="serie in series" :key="serie.ID" class="serie" >
                            <div class="preview">
                                <img v-if="previews[serie.Instances[0]]"
                                :src="previews[serie.Instances[0]]"
                                alt="Serie-Preview">
                            </div>

                            <div class="description">
                                <p>{{ serie.MainDicomTags.SeriesDescription || '_' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import {
        useAuthStore
    } from '../store/auth'
    import {
        useRouter
    } from 'vue-router'
    import {
        searchPatients,
        getPatientStudies,
        getStudySeries,
        getPreview
    } from '../store/api';


    export default {
        setup() {
            const authStore = useAuthStore()
            const router = useRouter()

            return {
                authStore,
                router
            }
        },
        data () {
            return {
                isLoading: false,
                loadingText: 'Willkommen',
                loadingResult: true,
                query: '',
                patients: [],
                studies: [],
                series: [],
                activePatient: '',
                activeStudy: '',
                previews: {},
            }
        },
        methods: {
            // The following are request-functions
            async searchPatients() {

                this.series = []

                if (this.query.length < 2) {
                    this.patients = []
                    return
                }

                try {
                    const response = await searchPatients(this.query)
                    this.patients = response
                    this.setLoadingStatus(false, "Patienten gefunden")
                } catch (error) {
                    console.error('Fehler bei der Suche:', error)
                    this.patients = []
                    this.setLoadingStatus(false, "Suche nach Patienten fehlgeschlagen", false)
                }
            },
            async selectPatient(orthancId) {
                this.setLoadingStatus(true, "Lade Studien")
                try {
                    const response = await getPatientStudies(orthancId)
                    this.studies = response
                    this.setLoadingStatus(false, "Studien geladen")
                } catch (error) {
                    console.error('Fehler bei Studiensuche:', error)
                    this.studies = []
                    this.setLoadingStatus(false, "Studien konnten nicht geladen werden", false)
                }

                this.activePatient = orthancId
            },
            async selectStudy(study) {
                this.setLoadingStatus(true, "Lade Series")

                try {
                    const response = await getStudySeries(study.ID)
                    this.series = response
                    this.setLoadingStatus(false, "Series geladen")
                } catch (error) {
                    console.error('Fehler bei Studiensuche:', error)
                    this.series = []
                    this.setLoadingStatus(false, "Series konnten nicht geladen werden", false)
                }

                this.activeStudy = study
                this.previews = {}

                this.loadPreviewUrls()
                
            },

            async loadPreviewUrls() {
                this.setLoadingStatus(true, "Lade Previews")

                for (const serie of this.series) {
                    const instanceId = serie.Instances[0]
                    if (instanceId) {
                        try {
                            const blobUrl = await getPreview(instanceId)
                            this.previews[instanceId] = blobUrl
                        } catch (e) {
                            console.error('Laden der Previews fehlgeschlagen:', e);
                        }
                    }
                }

                this.setLoadingStatus(false, "Ende")
            },
            loadViewer(orthancId) {
                this.router.push({
                    path: '/viewer',
                    query: { patient : orthancId}
                })
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
        }
    }
</script>