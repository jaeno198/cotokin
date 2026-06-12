<template>
  <div class="page">
    <div class="card-form">
      <h2>Meu Perfil</h2>

      <div v-if="carregando" class="loading">Carregando...</div>

      <form v-else @submit.prevent="salvar">
        <label>Nome completo</label>
        <input v-model="usuario.nome" type="text" required />

        <label>E-mail</label>
        <input v-model="usuario.email" type="email" required />

        <label>Perfil</label>
        <input :value="usuario.role" type="text" disabled />

        <p v-if="mensagem" class="mensagem">{{ mensagem }}</p>
        <p v-if="erro" class="erro">{{ erro }}</p>

        <div class="btn-group">
          <button type="submit" :disabled="salvando">
            {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
          <button type="button" class="btn-sair" @click="sair">Sair da Conta</button>
        </div>
      </form>

      <!-- MEUS ANÚNCIOS -->
      <div v-if="!carregando" class="anuncios">
        <h3>Meus Anúncios</h3>

        <div v-if="carregandoAnuncios" class="loading">Buscando anúncios...</div>

        <p v-else-if="!anuncios.length" class="vazio">Você ainda não tem anúncios.</p>

        <div v-else>
          <div v-for="anuncio in anuncios" :key="anuncio.id" class="anuncio-item">
            <div>
              <strong>{{ anuncio.titulo || anuncio.tipo }}</strong>
              <span>R$ {{ (anuncio.preco_venda || anuncio.preco || 0).toLocaleString('pt-BR') }}</span>
              <small>{{ anuncio.bairro || anuncio.cidade }}</small>
            </div>
            <button class="btn-remover" @click="removerAnuncio(anuncio.id)">Remover</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMe, logout, getImoveisUsuario } from '@/services/api.js'

const router           = useRouter()
const carregando       = ref(true)
const salvando         = ref(false)
const carregandoAnuncios = ref(false)
const mensagem         = ref('')
const erro             = ref('')
const anuncios         = ref([])
const usuario          = ref({ nome: '', email: '', role: '' })

onMounted(async () => {
  if (!localStorage.getItem('access_token')) {
    router.push('/login')
    return
  }
  try {
    const dados = await getMe()
    usuario.value = dados

    // Carrega anúncios do usuário
    carregandoAnuncios.value = true
    try {
      const lista = await getImoveisUsuario(dados.id)
      anuncios.value = Array.isArray(lista) ? lista : (lista.items || [])
    } catch {
      anuncios.value = []
    } finally {
      carregandoAnuncios.value = false
    }

  } catch (e) {
    erro.value = 'Sessão expirada. Faça login novamente.'
    setTimeout(() => { logout(); router.push('/login') }, 2000)
  } finally {
    carregando.value = false
  }
})

function salvar() {
  mensagem.value = '✅ Perfil atualizado com sucesso!'
  setTimeout(() => mensagem.value = '', 3000)
}

function removerAnuncio(id) {
  anuncios.value = anuncios.value.filter(a => a.id !== id)
}

function sair() {
  logout()
  router.push('/login')
}
</script>

<style scoped>
.page {
  min-height: 80vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: var(--brisa-suave);
  padding: 40px 16px;
}

.card-form {
  background: var(--branco);
  border-radius: var(--border-radius-g);
  border-top: var(--borda-g) solid var(--ceu-tecnologico);
  box-shadow: 0 4px 24px rgba(3,4,94,0.10);
  padding: 40px 36px;
  width: 100%;
  max-width: 520px;
}

h2 {
  font-family: 'Syne', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--azul-royal);
  margin-bottom: 24px;
}

h3 {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--azul-royal);
  margin-bottom: 14px;
}

.loading {
  color: var(--azul-corporativo);
  font-size: 0.95rem;
  padding: 1rem 0;
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

input:focus { border-color: var(--azul-corporativo); box-shadow: 0 0 0 3px rgba(0,119,182,0.12); }
input:disabled { background: var(--brisa-suave); opacity: 0.7; cursor: not-allowed; }

.mensagem { color: #059669; font-size: 0.9rem; margin-top: 12px; }
.erro { color: #dc2626; font-size: 0.9rem; margin-top: 12px; }

.btn-group { display: flex; gap: 12px; margin-top: 24px; }

button[type="submit"] {
  flex: 1;
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

button[type="submit"]:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
button[type="submit"]:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-sair {
  flex: 1;
  padding: 14px;
  background: transparent;
  color: var(--azul-corporativo);
  border: var(--borda-p) solid var(--agua-cristalina);
  border-radius: var(--border-radius-m);
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-sair:hover { background: var(--brisa-suave); }

.anuncios {
  margin-top: 36px;
  border-top: var(--borda-p) solid var(--agua-cristalina);
  padding-top: 24px;
}

.anuncio-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: var(--borda-p) solid var(--brisa-suave);
}

.anuncio-item strong {
  display: block;
  font-size: 0.95rem;
  color: var(--azul-royal);
}

.anuncio-item span {
  font-size: 0.85rem;
  color: var(--azul-corporativo);
}

.anuncio-item small {
  display: block;
  font-size: 0.78rem;
  color: var(--azul-corporativo);
  opacity: 0.7;
}

.btn-remover {
  padding: 6px 14px;
  background: transparent;
  color: #dc2626;
  border: 2px solid #dc2626;
  border-radius: var(--border-radius-p);
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.btn-remover:hover { background: #dc2626; color: var(--branco); }

.vazio {
  color: var(--azul-corporativo);
  font-size: 0.9rem;
  opacity: 0.7;
}
</style>
