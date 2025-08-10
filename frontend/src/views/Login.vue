<template>
    <div id="login">
        <div class="loading-status" :class="{ 'fade-away': !isLoading}">
            <div class="loading-symbol" :class="{ 'success' : !isLoading && loadingResult, 'error' : !isLoading && !loadingResult }"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>
        <form @submit.prevent="login">
            <h1>Login</h1>
            <input v-model="username" id="username" type="text" required @input="resetError" placeholder="Benutzername">
            <input v-model="password" id="password" type="password" required @input="resetError" placeholder="Passwort">
            <button type="submit">Login</button>
        </form>
        <p v-if="error" class="error">{{ error }}</p>
    </div>
</template>

<script>
    import {
        useAuthStore
    } from '../store/auth'
    import {
        setLoadingStatus
    } from '../store/utils'

export default {
    setup() {
        const authStore = useAuthStore()
        return {
            authStore
        }
    },
    data() {
        return {
            username: "",
            password: "",
            error: "",

            isLoading: false,
            loadingText: "Willkommen",
            loadingResult: true
        }
    },
    methods: {
        async login() {
            setLoadingStatus(this, true, "Prüfe Logindaten", true)

            await this.authStore.login(this.username, this.password, this.$router)
            if (!this.authStore.isAuthenticated) {
                this.error = 'Login failed. Please check your credentials.'
                setLoadingStatus(this, false, "Login fehlgeschlagen", false)
            } else {
                setLoadingStatus(this, false, "Login erfolgreich", true)
            }
        },
        resetError() {
            this.error = ""
        }
    }
}
</script>