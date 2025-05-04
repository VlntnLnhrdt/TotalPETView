<template>
    <div id="login">
        <form @submit.prevent="login">
            <h1>Login</h1>
            <input v-model="email" id="email" type="text" required @input="resetError" placeholder="Email">
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

export default {
    setup() {
        const authStore = useAuthStore()
        return {
            authStore
        }
    },
    data() {
        return {
            email: "",
            password: "",
            error: ""
        }
    },
    methods: {
        async login() {
            await this.authStore.login(this.email, this.password, this.$router)
            if (!this.authStore.isAuthenticated) {
                this.error = 'Login failed. Please check your credentials.'
            }
        },
        resetError() {
            this.error = ""
        }
    }
}
</script>