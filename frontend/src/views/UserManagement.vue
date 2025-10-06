<template>
    <div id="usermanagement">
        <div class="loading-status" :class="{ 'fade-away': !isLoading}">
            <div class="loading-symbol" :class="{ 'success' : !isLoading && loadingResult, 'error' : !isLoading && !loadingResult }"></div>
            <p v-if="loadingText">{{ loadingText }}</p>
        </div>

        <div class="content-wrapper">
            <div class="user-list-container">
                <h2>Benutzerliste</h2>
                <div class="user-list">
                    <div class="headrow">
                        <p>Benutzername</p>
                        <p>Registriert am</p>
                    </div>
                    <div v-if="users.length === 0">
                        <p class="no-results-text">Keine Benutzer gefunden.</p>
                    </div>
                    <div v-for="user in users" :key="user.username" class="user-row">
                        <p>{{ user.username }}</p>
                        <p>{{ formatDate(user.date_joined) }}</p>
                    </div>
                </div>
            </div>

            <div v-if="authStore.isSuperuser" class="add-user-container">
                <h2>Neuen Benutzer anlegen</h2>
                <form @submit.prevent="addUser" class="add-user-form">
                    <input type="text" v-model="newUser.username" placeholder="Benutzername" required>
                    <input type="password" v-model="newUser.password" placeholder="Passwort" required>
                    <input type="password" v-model="newUser.password2" placeholder="Passwort bestätigen" required>
                    <button type="submit">Benutzer anlegen</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import { useAuthStore } from '../store/auth'
    import { getAllUsers, registerUser } from '../store/api'
    import { formatDate, setLoadingStatus } from '../store/utils'

    export default {
        setup() {
            const authStore = useAuthStore()
            return { authStore }
        },
        data () {
            return {
                isLoading: false,
                loadingText: 'Willkommen',
                loadingResult: true,
                users: [],
                newUser: {
                    username: '',
                    password: '',
                    password2: ''
                }
            }
        },
        mounted() {
            this.loadUsers();
        },
        methods: {
            // Retrieves all registered users
            async loadUsers() {
                setLoadingStatus(this, true, "Lade Benutzer...", true)
                try {
                    const users = await getAllUsers();
                    this.users = users;
                    setLoadingStatus(this, false, "Benutzer geladen", true)
                } catch (error) {
                    console.error("Fehler beim Laden der Benutzer:", error)
                    setLoadingStatus(this, false, "Fehler beim Laden der Benutzer", false)
                }
            },
            // Adds user to the django backend
            async addUser() {
                if (this.newUser.password !== this.newUser.password2) {
                    setLoadingStatus(this, false, "Passwörter stimmen nicht überein", false);
                    return;
                }
                setLoadingStatus(this, true, "Lege neuen Benutzer an...", true);
                try {
                    await registerUser(this.newUser);
                    setLoadingStatus(this, false, "Benutzer erfolgreich angelegt", true);
                    this.newUser = { username: '', password: '', password2: '' };
                    await this.loadUsers();
                } catch (error) {
                    console.error("Fehler beim Anlegen des Benutzers:", error);
                    setLoadingStatus(this, false, "Fehler beim Anlegen des Benutzers", false);
                }
            },

            formatDate(dateString) {
                return formatDate(dateString);
            }
        },
    }
</script>

<style scoped>
#usermanagement {
    padding: 20px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.content-wrapper {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
    height: 100%;
}

.user-list-container, .add-user-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    overflow-y: auto;
}

h2 {
    margin-top: 0;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

.user-list .headrow, .user-list .user-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 10px;
    border-bottom: 1px solid #eee;
    align-items: center;
}

.user-list .headrow {
    font-weight: bold;
}

.no-results-text {
    padding: 20px;
    text-align: center;
    color: #888;
}

.add-user-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.add-user-form input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.add-user-form button {
    padding: 12px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.add-user-form button:hover {
    background-color: #45a049;
}

/* Loading Status from Search.vue */
.loading-status {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    z-index: 1000;
    display: flex;
    align-items: center;
    opacity: 1;
    transition: opacity 0.5s ease-in-out;
}

.loading-status.fade-away {
    opacity: 0;
}

.loading-symbol {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    margin-right: 10px;
    background-color: #f3f3f3; /* Placeholder */
    animation: spin 2s linear infinite;
}

.loading-symbol.success {
    background-color: #4CAF50;
    animation: none;
}

.loading-symbol.error {
    background-color: #f44336;
    animation: none;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>