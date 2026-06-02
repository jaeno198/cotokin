<template>
  <div id="app">

    <!-- TOP BAR — fora do container para ocupar 100% da largura -->
    <div class="top-bar">
      Milhares de imóveis à venda e aluguel em todo o Brasil
    </div>

    <div class="container-fluid">

      <!-- NAVBAR -->
      <header>
        <nav>
          <router-link to="/">
            <img src="@/assets/img/logos/logo.jpeg" alt="GeoHouse" />
          </router-link>
          <div class="nav-actions">
            <router-link to="/login">Entrar</router-link>
            <router-link to="/cadastro">Cadastrar</router-link>
            <router-link to="/perfil">Meu Perfil</router-link>
            <button class="btn-anunciar" @click="modalAberto = true">
              <i class="fas fa-plus"></i> Anunciar Grátis
            </button>
          </div>
        </nav>
      </header>

      <!-- CONTEÚDO DA ROTA -->
      <router-view :search-query="searchQuery" />

      <!-- FOOTER -->
      <footer>
        <p>© 2025 GEOHOUSE — Imóveis com Confiança. Todos os direitos reservados.</p>
      </footer>

    </div>

    <!-- MODAL — fora do container para sobrepor tudo -->
    <div v-if="modalAberto" class="modal-overlay" @click.self="modalAberto = false">
      <div class="modal-box">
        <h2>Anunciar Imóvel — Grátis</h2>
        <input v-model="novoAnuncio.titulo" type="text" placeholder="Título do anúncio" />
        <textarea v-model="novoAnuncio.descricao" placeholder="Descrição completa" rows="4"></textarea>
        <div class="modal-grid">
          <input v-model="novoAnuncio.tipo" type="text" placeholder="Tipo (Casa, Apt, etc)" />
          <input v-model="novoAnuncio.preco" type="number" placeholder="Preço R$" />
        </div>
        <button class="btn-publicar" @click="publicarAnuncio">Publicar Anúncio</button>
        <button class="btn-fechar" @click="modalAberto = false">Fechar</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchQuery = ref('')
const modalAberto = ref(false)

const novoAnuncio = ref({
  titulo: '',
  descricao: '',
  tipo: '',
  preco: null,
})

function publicarAnuncio() {
  alert('✅ Anúncio publicado com sucesso!')
  novoAnuncio.value = { titulo: '', descricao: '', tipo: '', preco: null }
  modalAberto.value = false
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
</style>