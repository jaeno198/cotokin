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

const router       = useRouter()
const searchQuery  = ref('')
const modalAberto  = ref(false)
const enviando     = ref(false)
const erroModal    = ref('')
const sucessoModal = ref('')

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
  height: 48px;
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
</style>
