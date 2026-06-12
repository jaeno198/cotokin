*<template>
  <div class="page">
    <div class="card-form">
      <h2>Entrar</h2>

      <form @submit.prevent="fazerLogin">
        <label>E-mail</label>
        <input v-model="email" type="email" placeholder="seu@email.com" required />

        <label>Senha</label>
        <input v-model="senha" type="password" placeholder="Sua senha" required />

        <p v-if="erro" class="erro">{{ erro }}</p>

        <button type="submit" :disabled="carregando">
          {{ carregando ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>

      <p>Não tem conta? <router-link to="/cadastro">Cadastre-se</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/api.js'

const router = useRouter()
const email      = ref('')
const senha      = ref('')
const erro       = ref('')
const carregando = ref(false)

async function fazerLogin() {
  erro.value = ''
  carregando.value = true
  try {
    await login(email.value, senha.value)
    router.push('/')
  } catch (e) {
    erro.value = e.message || 'Erro ao fazer login.'
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
.page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--brisa-suave);
}

.card-form {
  background: var(--branco);
  border-radius: var(--border-radius-g);
  border-top: var(--borda-g) solid var(--ceu-tecnologico);
  box-shadow: 0 4px 24px rgba(3,4,94,0.10);
  padding: 40px 36px;
  width: 100%;
  max-width: 420px;
}

h2 {
  font-family: 'Syne', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--azul-royal);
  margin-bottom: 24px;
}

label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--azul-corporativo);
  margin-bottom: 6px;
  margin-top: 16px;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: var(--borda-p) solid var(--agua-cristalina);
  border-radius: var(--border-radius-m);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  color: var(--azul-royal);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

input:focus {
  border-color: var(--azul-corporativo);
  box-shadow: 0 0 0 3px rgba(0,119,182,0.12);
}

.erro {
  color: #dc2626;
  font-size: 0.85rem;
  margin-top: 10px;
}

button[type="submit"] {
  width: 100%;
  margin-top: 24px;
  padding: 14px;
  background: var(--gradient-horizontal);
  color: var(--branco);
  border: none;
  border-radius: var(--border-radius-m);
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}

button[type="submit"]:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

button[type="submit"]:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

p {
  margin-top: 20px;
  font-size: 0.9rem;
  color: var(--azul-corporativo);
  text-align: center;
}

a {
  color: var(--ceu-tecnologico);
  font-weight: 700;
  text-decoration: none;
}

a:hover { color: var(--azul-royal); }
</style>
