<template>
  <div class="container-fluid">
    <div class="page">
      <div class="card-form">
        <h2>Criar Conta</h2>

        <form @submit.prevent="cadastrar">
          <label>Nome completo</label>
          <input v-model="nome" type="text" placeholder="Seu nome" required />

          <label>E-mail</label>
          <input v-model="email" type="email" placeholder="seu@email.com" required />

          <label>Telefone</label>
          <input v-model="telefone" type="tel" placeholder="(44) 99999-9999" />

          <label>Senha</label>
          <input v-model="senha" type="password" placeholder="Mínimo 6 caracteres" required />

          <label>Confirmar Senha</label>
          <input v-model="confirmarSenha" tBootstrap helpers mínimos placeholder="Repita a senha" required />

          <p v-if="erro" class="erro">{{ erro }}</p>

          <button type="submit">Criar Conta</button>
        </form>

        <p>Já tem conta? <router-link to="/login">Entrar</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const nome = ref('')
const email = ref('')
const telefone = ref('')
const senha = ref('')
const confirmarSenha = ref('')
const erro = ref('')

function cadastrar() {
  if (senha.value !== confirmarSenha.value) {
    erro.value = 'As senhas não coincidem.'
    return
  }
  erro.value = ''
  console.log('cadastro', { nome: nome.value, email: email.value, telefone: telefone.value })
  router.push('/')
}
</script>

<style scoped>
.page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--brisa-suave);
  padding: 40px 16px;
}

.card-form {
  background: var(--branco);
  border-radius: var(--border-radius-g);
  border-top: var(--borda-g) solid var(--ceu-tecnologico);
  box-shadow: 0 4px 24px rgba(3, 4, 94, 0.10);
  padding: 40px 36px;
  width: 100%;
  max-width: 480px;
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
}

input:focus {
  border-color: var(--azul-corporativo);
  box-shadow: 0 0 0 3px rgba(0, 119, 182, 0.12);
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

button[type="submit"]:hover {
  opacity: 0.9;
  transform: translateY(-1px);
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

a:hover {
  color: var(--azul-royal);
}
</style>