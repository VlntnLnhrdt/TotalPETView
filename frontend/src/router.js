import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './store/auth.js'
import NotFound from './views/NotFound.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Search from './views/Search.vue'
import Viewer from './views/Viewer.vue'

const routes = [
    {
        path: '/',
        redirect: '/search',
        meta: {
            needsAuth: false,
        },
    },
    {
        path: '/search',
        name: 'search',
        component: Search,
        meta: {
            needsAuth: true,
        },
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
        meta: {
            needsAuth: false,
        },
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
        meta: {
            needsAuth: false,
        },
    },
    {
        path: '/viewer',
        name: 'viewer',
        component: Viewer,
        meta: {
            needsAuth: true,
        },
    },
    {
        path: '/:pathMatch(.*)*',
        name: '404 Not Found',
        component: NotFound
    },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Gets executed before routing
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    // Checks if Authentication is required
    if(to.meta.needsAuth) { 
        // Checks if user is authenticated
        if (authStore.isAuthenticated) {
            next();
        } else {
            next('/login');
        }
    } else {
        next();
    }
})

export default router