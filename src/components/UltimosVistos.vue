<template>
  <section v-if="lista.length" class="ultimos-vistos">
    <div class="uv-header">
      <h3><i class="fas fa-history"></i> Vistos recentemente</h3>
      <button class="uv-limpar" @click="limparTudo">Limpar</button>
    </div>
    <div class="uv-scroll">
      <div v-for="imovel in lista" :key="imovel.id" class="uv-card">
        <img
          :src="imovel.img || 'https://via.placeholder.com/120x80?text=GeoHouse'"
          :alt="imovel.titulo"
          class="uv-img"
        />
        <div class="uv-info">
          <p class="uv-titulo">{{ imovel.titulo }}</p>
          <p class="uv-preco">R$ {{ imovel.preco.toLocaleString('pt-BR') }}</p>
          <p class="uv-cidade"><i class="fas fa-map-marker-alt"></i> {{ imovel.cidade }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUltimosVistos } from '@/composables/useUltimosVistos'

const { carregar, limpar } = useUltimosVistos()
const lista = ref([])

onMounted(() => { lista.value = carregar() })

function limparTudo() {
  limpar()
  lista.value = []
}
</script>

<style scoped>
.ultimos-vistos {
  padding: 16px 24px 0;
}

.uv-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.uv-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--azul-corporativo, #0077B6);
  margin: 0;
}

.uv-limpar {
  background: none;
  border: none;
  font-size: 0.8rem;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
}

.uv-limpar:hover { color: #dc2626; }

.uv-scroll {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
  scrollbar-width: thin;
}

.uv-card {
  flex: 0 0 180px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}

.uv-img {
  width: 100%;
  height: 90px;
  object-fit: cover;
  display: block;
}

.uv-info {
  padding: 8px 10px;
}

.uv-titulo {
  font-size: 0.78rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.uv-preco {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--azul-corporativo, #0077B6);
  margin: 0 0 2px;
}

.uv-cidade {
  font-size: 0.72rem;
  color: #64748b;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
