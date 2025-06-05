<template>
    <div>
        <div id="header">
            <div class="info">
                <img src="../assets/images/mri_logo.png" alt="MRI-Logo">
                <p class="progname">TotalPETView</p>
                <p class="version">v0.3</p>

            </div>

            <div v-if="authStore.isAuthenticated" class="navbar">
                <router-link to="/search"><img src="../assets/images/icon_search.png" alt="Search-Icon"></router-link>
                <router-link to="/upload"><img src="../assets/images/icon_upload.png" alt="Upload-Icon"></router-link>
                <router-link @click="logout" to="/login"><img src="../assets/images/icon_logout.png" alt="User-Icon"></router-link>
            </div>
        </div>

        <main>
            <slot></slot>
        </main>
    </div>
</template>

<script>
    import {
        useAuthStore
    } from '../store/auth.js'
    import {
        useRouter
    } from 'vue-router'

    export default {
        setup() {
            const authStore = useAuthStore()
            const router = useRouter()

            return {
                authStore,
                router
            }
        },
        methods: {
            async logout() {
                try {
                    await this.authStore.logout(this.$router)
                } catch (error) {
                    console.error("Failed to logout properly.")   
                }
            },
        },
        async mounted() {
            await this.authStore.fetchUser();
        }
    }
</script>