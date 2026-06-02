import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/styles.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import Login    from './views/Login.vue'
import Cadastro from './views/Cadastro.vue'
import Perfil   from './views/Perfil.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',         component: Dashboard },
    { path: '/login',    component: Login     },
    { path: '/cadastro', component: Cadastro  },
    { path: '/perfil',   component: Perfil    },
  ]
})

createApp(App).use(router).mount('#app')