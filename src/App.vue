<template>
  <div id="app">

    <div class="top-bar">
      Milhares de imóveis à venda e aluguel em todo o Brasil
    </div>

    <div class="container-fluid">

      <header>
        <nav>
          <router-link to="/">
            <img src="@/assets/img/logos/logo.jpeg" alt="GeoHouse" />
          </router-link>
          <div class="nav-actions">
            <template v-if="!usuarioLogado">
              <router-link to="/login">Entrar</router-link>
              <router-link to="/cadastro">Cadastrar</router-link>
            </template>
            <template v-else>
              <router-link to="/perfil">Meu Perfil</router-link>
              <button class="btn-sair-nav" @click="fazerLogout">Sair</button>
            </template>
            <button class="btn-anunciar" @click="modalAberto = true">
              <i class="fas fa-plus"></i> Anunciar Grátis
            </button>
          </div>
        </nav>
      </header>

      <router-view :search-query="searchQuery" />

      <footer>
        <p>© 2026 GEOHOUSE — Imóveis com Confiança. Todos os direitos reservados.</p>
      </footer>

    </div>

    <!-- POPUP INSTALAR PWA -->
    <div v-if="mostrarInstalar" class="pwa-banner">
      <img src="@/assets/img/logos/logo.jpeg" alt="GeoHouse" class="pwa-logo" />
      <div class="pwa-texto">
        <strong>Instalar GeoHouse</strong>
        <span>Acesse imóveis offline, direto da tela inicial</span>
      </div>
      <button class="pwa-btn-instalar" @click="instalarPwa">Instalar</button>
      <button class="pwa-btn-fechar" @click="mostrarInstalar = false">✕</button>
    </div>

    <!-- MODAL ANUNCIAR -->
    <div v-if="modalAberto" class="modal-overlay" @click.self="modalAberto = false">
      <div class="modal-box">
        <h2>Anunciar Imóvel</h2>

        <div v-if="!usuarioLogado" class="modal-aviso">
          <p>Você precisa estar logado para anunciar.</p>
          <router-link to="/login" @click="modalAberto = false">Fazer login</router-link>
        </div>

        <template v-else>
          <input v-model="novoAnuncio.titulo"   type="text"   placeholder="Título do anúncio" />
          <textarea v-model="novoAnuncio.descricao" placeholder="Descrição completa" rows="4"></textarea>
          <div class="modal-grid">
            <input v-model="novoAnuncio.tipo"  type="text"   placeholder="Tipo (Casa, Apt, etc)" />
            <input v-model="novoAnuncio.preco" type="number" placeholder="Preço R$" />
          </div>
          <p v-if="erroModal" class="erro-modal">{{ erroModal }}</p>
          <p v-if="sucessoModal" class="sucesso-modal">{{ sucessoModal }}</p>
          <button class="btn-publicar" @click="publicarAnuncio" :disabled="enviando">
            {{ enviando ? 'Publicando...' : 'Publicar Anúncio' }}
          </button>
        </template>

        <button class="btn-fechar" @click="modalAberto = false">Fechar</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { logout } from '@/services/api.js'

const router          = useRouter()
const searchQuery     = ref('')
const modalAberto     = ref(false)
const enviando        = ref(false)
const erroModal       = ref('')
const sucessoModal    = ref('')
const mostrarInstalar = ref(false)
let   deferredPrompt  = null

onMounted(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt = e
    mostrarInstalar.value = true
  })
  window.addEventListener('appinstalled', () => {
    mostrarInstalar.value = false
    deferredPrompt = null
  })
})

async function instalarPwa() {
  if (!deferredPrompt) return
  deferredPrompt.prompt()
  const { outcome } = await deferredPrompt.userChoice
  if (outcome === 'accepted') mostrarInstalar.value = false
  deferredPrompt = null
}

const novoAnuncio = ref({
  titulo: '', descricao: '', tipo: '', preco: null,
})

const usuarioLogado = computed(() => !!localStorage.getItem('access_token'))

async function publicarAnuncio() {
  erroModal.value = ''
  if (!novoAnuncio.value.titulo || !novoAnuncio.value.preco) {
    erroModal.value = 'Preencha pelo menos o título e o preço.'
    return
  }
  enviando.value = true
  try {
    // Por hora redireciona para o backend quando integração de imóveis estiver pronta
    sucessoModal.value = '✅ Anúncio enviado! Em breve aparecerá na listagem.'
    novoAnuncio.value = { titulo: '', descricao: '', tipo: '', preco: null }
    setTimeout(() => { modalAberto.value = false; sucessoModal.value = '' }, 2000)
  } catch (e) {
    erroModal.value = e.message || 'Erro ao publicar.'
  } finally {
    enviando.value = false
  }
}

function fazerLogout() {
  logout()
  router.push('/login')
}
</script>

<style>
header nav a img {
  display: block;
  height: 60px;
  max-width: 160px;
  width: auto;
  object-fit: contain;
}
.btn-sair-nav {
  background: transparent;
  border: 1px solid var(--agua-cristalina, #ccc);
  border-radius: 6px;
  padding: 6px 14px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: var(--azul-corporativo, #0077B6);
  transition: background 0.2s;
}
.btn-sair-nav:hover { background: var(--brisa-suave, #f0f8ff); }
.modal-aviso { text-align: center; padding: 1rem 0; }
.modal-aviso p { margin-bottom: 12px; color: var(--azul-corporativo, #555); }
.modal-aviso a { color: var(--ceu-tecnologico, #0077B6); font-weight: 700; text-decoration: none; }
.erro-modal { color: #dc2626; font-size: 0.85rem; margin-top: 8px; }
.sucesso-modal { color: #16a34a; font-size: 0.85rem; margin-top: 8px; }

/* PWA install banner */
.pwa-banner {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 14px 18px;
  z-index: 9999;
  max-width: 380px;
  width: calc(100% - 32px);
  border-left: 4px solid #0077B6;
}
.pwa-logo {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
}
.pwa-texto {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}
.pwa-texto strong {
  font-size: 0.9rem;
  color: #0f172a;
}
.pwa-texto span {
  font-size: 0.76rem;
  color: #64748b;
  margin-top: 2px;
}
.pwa-btn-instalar {
  background: #0077B6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}
.pwa-btn-instalar:hover { background: #005f8e; }
.pwa-btn-fechar {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1rem;
  cursor: pointer;
  padding: 0 4px;
  flex-shrink: 0;
}
.pwa-btn-fechar:hover { color: #dc2626; }
</style>
