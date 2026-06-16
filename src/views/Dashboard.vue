<template>
  <div>

    <!-- MAPA DE ZONAS -->
    <h1>Selecione uma região</h1>
    <section class="mapa-section">
      <div class="container-mx-auto py-3 px-4">

        <div class="section-title">
          <i class="fas fa-map-marked-alt"></i> Buscar por zona — Maringá PR
        </div>

        <div class="row g-2 align-items-start">

          <!-- COL 1 — Botões de zona -->
          <div class="col-12 col-md-2 d-flex flex-column gap-2" style="min-width:140px;">
            <button v-for="(cfg, key) in ZONAS_CFG" :key="key" class="zona-btn w-100"
              :id="`zbtn-${key}`" :class="{ active: zonaAtiva === key }"
              :style="zonaAtiva === key ? BTNS_STYLE[key] : ''" @click="handleSelecionarZona(key)">
              <span class="zdot" :style="`background:${key === 'all' ? 'rgba(255,255,255,0.7)' : cfg.cor}`"></span>
              {{ key === 'all' ? 'Toda Maringá' : cfg.nome }}
            </button>
          </div>

          <!-- COL 2 — Mapa SVG -->
          <div class="col-12 col-md-7" style="position:relative;">
            <div ref="tooltipEl" class="mapa-tooltip"></div>
            <svg ref="svgEl" viewBox="0 -4 400 420" xmlns="http://www.w3.org/2000/svg"
              style="width:75%;height:auto;cursor:pointer;display:block;">
              <g class="zgrp" data-zona="norte">
                <rect class="zp" x="90" y="30" width="70" height="50" rx="4" data-b="Jd. Alvorada" />
                <rect class="zp" x="165" y="30" width="70" height="50" rx="4" data-b="Vila Operária" />
                <rect class="zp" x="240" y="30" width="70" height="50" rx="4" data-b="Pq. das Grevíleas" />
                <rect class="zp" x="90" y="85" width="70" height="45" rx="4" data-b="Cj. Inocente" />
                <rect class="zp" x="165" y="85" width="70" height="45" rx="4" data-b="Jd. Imperial" />
                <rect class="zp" x="240" y="85" width="70" height="45" rx="4" data-b="Pq. Res. Japão" />
                <text class="zlabel" x="125" y="59">Jd. Alvorada</text>
                <text class="zlabel" x="200" y="59">Vila Operária</text>
                <text class="zlabel" x="275" y="59">Pq. Grevíleas</text>
                <text class="zlabel" x="125" y="112">Cj. Inocente</text>
                <text class="zlabel" x="200" y="112">Jd. Imperial</text>
                <text class="zlabel" x="275" y="112">Pq. Japão</text>
              </g>
              <g class="zgrp" data-zona="leste">
                <rect class="zp" x="310" y="135" width="80" height="55" rx="4" data-b="Jd. Novo Horizonte" />
                <rect class="zp" x="310" y="195" width="80" height="55" rx="4" data-b="Jd. Borba Gato" />
                <rect class="zp" x="310" y="255" width="80" height="55" rx="4" data-b="Jd. Itaipu" />
                <text class="zlabel" x="350" y="163">Novo Horizonte</text>
                <text class="zlabel" x="350" y="223">Borba Gato</text>
                <text class="zlabel" x="350" y="283">Jd. Itaipu</text>
              </g>
              <g class="zgrp" data-zona="oeste">
                <rect class="zp" x="10" y="135" width="75" height="55" rx="4" data-b="Jd. Iguaçu" />
                <rect class="zp" x="10" y="195" width="75" height="55" rx="4" data-b="Jd. Universo" />
                <rect class="zp" x="10" y="255" width="75" height="55" rx="4" data-b="Pq. das Palmeiras" />
                <text class="zlabel" x="47" y="163">Jd. Iguaçu</text>
                <text class="zlabel" x="47" y="223">Jd. Universo</text>
                <text class="zlabel" x="47" y="283">Pq. Palmeiras</text>
              </g>
              <g class="zgrp" data-zona="centro">
                <rect class="zp" x="90" y="135" width="215" height="70" rx="4" data-b="Centro / Zonas 01-04" />
                <rect class="zp" x="90" y="210" width="100" height="55" rx="4" data-b="Zona 01 / Zona 02" />
                <rect class="zp" x="195" y="210" width="110" height="55" rx="4" data-b="Zona 03 / Zona 04" />
                <text class="zlabel" x="197" y="168" style="font-size:12px;font-weight:700;">C E N T R O</text>
                <text class="zlabel" x="197" y="183" style="font-size:9px;">⛪ Catedral de Maringá</text>
                <text class="zlabel" x="140" y="238">Zona 01/02</text>
                <text class="zlabel" x="250" y="238">Zona 03/04</text>
              </g>
              <g class="zgrp" data-zona="sul">
                <rect class="zp" x="90" y="275" width="65" height="50" rx="4" data-b="Jd. Pinheiros" />
                <rect class="zp" x="160" y="275" width="65" height="50" rx="4" data-b="Jd. Guanabara" />
                <rect class="zp" x="230" y="275" width="75" height="50" rx="4" data-b="Cj. Requião" />
                <rect class="zp" x="90" y="330" width="65" height="55" rx="4" data-b="Jd. Alpes" />
                <rect class="zp" x="160" y="330" width="65" height="55" rx="4" data-b="Jd. Liberdade" />
                <rect class="zp" x="230" y="330" width="75" height="55" rx="4" data-b="Cidade Alta" />
                <rect class="zp" x="90" y="390" width="215" height="25" rx="4" data-b="Sta. Felicidade / Cidade Industrial" />
                <text class="zlabel" x="122" y="301">Jd. Pinheiros</text>
                <text class="zlabel" x="192" y="301">Guanabara</text>
                <text class="zlabel" x="267" y="301">Cj. Requião</text>
                <text class="zlabel" x="122" y="358">Jd. Alpes</text>
                <text class="zlabel" x="192" y="358">Jd. Liberdade</text>
                <text class="zlabel" x="267" y="358">Cidade Alta</text>
                <text class="zlabel" x="197" y="405">Sta. Felicidade / Cidade Industrial</text>
              </g>
              <text x="197" y="20" style="font-size:10px;font-weight:700;text-anchor:middle;fill:#0077B6;font-family:'DM Sans',sans-serif;">↑ NORTE</text>
              <text x="197" y="390" style="font-size:10px;font-weight:700;text-anchor:middle;fill:#0077B6;font-family:'DM Sans',sans-serif;">↓ SUL</text>
              <text x="15" y="234" style="font-size:9px;font-weight:700;text-anchor:middle;fill:#0077B6;font-family:'DM Sans',sans-serif;" transform="rotate(-90 6 232)">OESTE</text>
              <text x="398" y="235" style="font-size:9px;font-weight:700;text-anchor:middle;fill:#0077B6;font-family:'DM Sans',sans-serif;" transform="rotate(90 398 218)">LESTE</text>
            </svg>
          </div>

          <!-- COL 3 — Info bairros -->
          <div class="col-12 col-md-3 d-flex flex-column gap-3 justify-content-start" style="min-width:200px;">
            <div class="mapa-info-box" :style="`border-left-color: ${cfgAtiva.cor}`" style="max-height:210px; overflow-y:auto;">
              <div class="zona-nome">{{ cfgAtiva.nome }}</div>
              <div class="zona-bairros">{{ cfgAtiva.bairros }}</div>
            </div>
            <div class="mapa-count-badge" style="max-height:210px;">
              <i class="fas fa-home"></i>
              <ul>
                <li><span>{{ imoveisFiltrados.length }}</span></li>
                <li>imóveis disponíveis</li>
              </ul>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- FILTROS -->
    <div class="container-main">
      <div class="sidebar">
        <h3><i class="fas fa-filter"></i> Filtros</h3>
        <div class="sidebar-fields">

          <div class="sidebar-field">
            <label>Modalidade</label>
            <select v-model="modalidade">
              <option value="venda">Compra</option>
              <option value="aluguel">Aluguel</option>
              <option value="rural">Imóveis Rurais</option>
            </select>
          </div>

          <div class="sidebar-field">
            <label>Tipo de Imóvel</label>
            <select v-model="tipoFiltro">
              <option value="">Todos</option>
              <option value="casa">Casa</option>
              <option value="apartamento">Apartamento</option>
              <option value="terreno">Terreno</option>
              <option value="sitio">Sítio / Chácara</option>
            </select>
          </div>

          <div class="sidebar-field">
            <label>Preço Mínimo (R$)</label>
            <input v-model="precoMin" type="number" placeholder="Ex: 100000" />
          </div>

          <div class="sidebar-field">
            <label>Preço Máximo (R$)</label>
            <input v-model="precoMax" type="number" placeholder="Ex: 2000000" />
          </div>

          <div class="sidebar-field">
            <label>Quartos</label>
            <select v-model="quartosFiltro">
              <option value="">Qualquer</option>
              <option value="1">1 ou mais</option>
              <option value="2">2 ou mais</option>
              <option value="3">3 ou mais</option>
              <option value="4">4 ou mais</option>
            </select>
          </div>

          <div class="sidebar-field sidebar-btn-wrap">
            <button class="btn-buscar" @click="buscar">
              <i class="fas fa-search"></i> Buscar Imóveis
            </button>
          </div>

        </div>
      </div>
    </div>

    <!-- LISTINGS -->
    <div class="container-main">
      <div>
        <div class="main-header">
          <h2 id="titulo-pagina">
            {{ modalidade === 'venda' ? 'Imóveis à Venda' : modalidade === 'aluguel' ? 'Imóveis para Alugar' : 'Imóveis Rurais' }}
          </h2>
          <p class="contagem">
            <span v-if="carregandoImoveis">Buscando...</span>
            <span v-else>Encontrei <strong>{{ imoveisFiltrados.length }}</strong> imóveis</span>
          </p>
        </div>

        <div v-if="erroImoveis" class="erro-lista">{{ erroImoveis }}</div>

        <UltimosVistos />

        <div class="listings">
          <div v-for="imovel in imoveisFiltrados" :key="imovel.id" class="card" @click="verImovel(imovel)" style="cursor:pointer;">
            <div class="card-img-wrap">
              <img :src="imovel.img || imovel.foto_capa || 'https://via.placeholder.com/600x400?text=GeoHouse'" :alt="imovel.titulo" loading="lazy" />
              <span v-if="imovel.tag" class="card-tag">{{ imovel.tag }}</span>
            </div>
            <div class="card-body">
              <h3>{{ imovel.titulo }}</h3>
              <div class="price">R$ {{ (imovel.preco || imovel.preco_venda || 0).toLocaleString('pt-BR') }}</div>
              <div class="details">
                <span><i class="fas fa-bed"></i> {{ imovel.quartos }}</span>
                <span><i class="fas fa-bath"></i> {{ imovel.banheiros }}</span>
                <span><i class="fas fa-ruler-combined"></i> {{ imovel.area || imovel.area_construida }}m²</span>
              </div>
              <p class="city-label">
                <i class="fas fa-map-marker-alt" style="color:var(--ceu-tecnologico)"></i>
                {{ imovel.cidade || imovel.bairro }}
              </p>
              <button class="btn-whats" @click="contatar(imovel.id)">
                <i class="fab fa-whatsapp"></i> Conversar
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useZona } from '@/composables/useZona'
import { useUltimosVistos } from '@/composables/useUltimosVistos'
import { getImoveis } from '@/services/api.js'
import { imoveis as imoveisEstaticos } from '@/data/imoveis'
import UltimosVistos from '@/components/UltimosVistos.vue'

const route = useRoute()

const {
  zonaAtiva, modalidade, tipoFiltro, precoMin, precoMax, quartosFiltro,
  cfgAtiva, selecionarZona, ZONAS_CFG, BTNS_STYLE,
} = useZona()

const { registrar: registrarVisto } = useUltimosVistos()

const tooltipEl        = ref(null)
const svgEl            = ref(null)
const imoveisAPI       = ref([])
const carregandoImoveis = ref(false)
const erroImoveis      = ref('')

const focusIds = computed(() => {
  const raw = route.query.focus || ''
  const ids = raw.toString().split(',').map(value => parseInt(value.trim(), 10)).filter(n => Number.isInteger(n) && n > 0)
  return ids.length ? ids : null
})

// Usa dados da API se disponível, senão usa os estáticos
const imoveisFonte = computed(() => imoveisAPI.value.length ? imoveisAPI.value : imoveisEstaticos)

const imoveisFiltrados = computed(() => {
  let lista = zonaAtiva.value === 'all'
    ? imoveisFonte.value
    : imoveisFonte.value.filter(i => i.zona === zonaAtiva.value)

  if (modalidade.value)
    lista = lista.filter(i => !i.modalidade || i.modalidade === modalidade.value)
  if (tipoFiltro.value)
    lista = lista.filter(i => i.tipo === tipoFiltro.value)
  if (precoMin.value)
    lista = lista.filter(i => (i.preco || i.preco_venda || 0) >= parseFloat(precoMin.value))
  if (precoMax.value)
    lista = lista.filter(i => (i.preco || i.preco_venda || 0) <= parseFloat(precoMax.value))
  if (quartosFiltro.value)
    lista = lista.filter(i => (i.quartos || 0) >= parseInt(quartosFiltro.value))

  if (focusIds.value)
    lista = lista.filter(i => focusIds.value.includes(i.id))

  return lista
})

function verImovel(imovel) {
  registrarVisto(imovel)
}

async function buscar() {
  carregandoImoveis.value = true
  erroImoveis.value = ''
  try {
    const params = {}
    if (tipoFiltro.value)    params.tipo       = tipoFiltro.value
    if (precoMin.value)      params.preco_min  = precoMin.value
    if (precoMax.value)      params.preco_max  = precoMax.value
    if (quartosFiltro.value) params.quartos    = quartosFiltro.value
    const dados = await getImoveis(params)
    imoveisAPI.value = Array.isArray(dados) ? dados : (dados.items || [])
  } catch (e) {
    erroImoveis.value = 'Não foi possível carregar da API. Exibindo dados locais.'
    imoveisAPI.value = []
  } finally {
    carregandoImoveis.value = false
  }
}

function aplicarCoresMapa() {
  document.querySelectorAll('.zgrp').forEach(g => {
    const z = g.dataset.zona
    const ativo = zonaAtiva.value === 'all' || zonaAtiva.value === z
    const cfg = ZONAS_CFG[z]
    g.querySelectorAll('.zp').forEach(el => {
      el.style.fill    = ativo ? cfg.fill   : '#f1f5f9'
      el.style.stroke  = ativo ? cfg.stroke : '#cbd5e1'
      el.style.opacity = ativo ? '1' : '0.3'
    })
    g.querySelectorAll('.zlabel').forEach(el => {
      el.style.fill    = ativo ? cfg.text : '#94a3b8'
      el.style.opacity = ativo ? '1' : '0.3'
    })
  })
}

function handleSelecionarZona(zona) {
  selecionarZona(zona)
  aplicarCoresMapa()
}

function contatar(id) {
  alert(`✅ Redirecionando para WhatsApp do anunciante (Imóvel #${id})`)
}

onMounted(async () => {
  aplicarCoresMapa()

  // Tenta carregar imóveis da API ao iniciar
  try {
    const dados = await getImoveis()
    imoveisAPI.value = Array.isArray(dados) ? dados : (dados.items || [])
  } catch {
    // Sem conexão com API — usa dados estáticos silenciosamente
  }

  document.querySelectorAll('.zp').forEach(el => {
    el.addEventListener('mouseenter', () => {
      const z = el.closest('.zgrp').dataset.zona
      el.style.fill    = ZONAS_CFG[z].hover
      el.style.opacity = '1'
      tooltipEl.value.style.display  = 'block'
      tooltipEl.value.textContent    = (el.dataset.b || '') + ' — ' + ZONAS_CFG[z].nome
    })
    el.addEventListener('mousemove', e => {
      const r = svgEl.value.parentElement.getBoundingClientRect()
      tooltipEl.value.style.left = (e.clientX - r.left + 12) + 'px'
      tooltipEl.value.style.top  = (e.clientY - r.top - 38) + 'px'
    })
    el.addEventListener('mouseleave', () => {
      aplicarCoresMapa()
      tooltipEl.value.style.display = 'none'
    })
    el.addEventListener('click', () => {
      const z = el.closest('.zgrp').dataset.zona
      handleSelecionarZona(z)
    })
  })
})
</script>

<style>
/* ── MAPA SECTION ─────────────────────────────── */
.mapa-section {
  background: var(--brisa-suave);
  border-top: var(--borda-g) solid var(--ceu-tecnologico);
  border-bottom: var(--borda-m) solid var(--brisa-suave);
  box-shadow: 0 4px 20px rgba(3,4,94,0.07);
}
.mapa-section .section-title {
  font-family: 'Syne', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--azul-corporativo);
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 14px;
}

/* ── BOTÕES DE ZONA ────────────────────────────── */
.zona-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 10px 14px;
  height: 44px;
  min-width: 120px;
  border-radius: 30px;
  border: 2px solid transparent;
  background: var(--branco);
  color: var(--azul-royal);
  font-size: 0.82rem;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: all 0.18s;
}
.zdot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ── SVG MAPA ──────────────────────────────────── */
.zp {
  stroke-width: 1.2;
  transition: fill 0.22s, opacity 0.22s, stroke 0.22s;
  cursor: pointer;
}
.zlabel {
  font-size: 9px;
  text-anchor: middle;
  dominant-baseline: middle;
  pointer-events: none;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
}
.mapa-tooltip {
  position: absolute;
  background: var(--azul-royal);
  color: var(--branco);
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
  pointer-events: none;
  display: none;
  white-space: nowrap;
  z-index: 10;
}

/* ── INFO BOX + BADGE ──────────────────────────── */
.mapa-info-box {
  background: var(--branco);
  border-radius: var(--border-radius-m);
  padding: 14px 16px;
  border-left: var(--borda-m) solid var(--ceu-tecnologico);
  flex: 1;
  min-width: 180px;
  max-height: 210px;
  overflow-y: auto;
}
.mapa-info-box .zona-nome {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--azul-royal);
  margin-bottom: 4px;
}
.mapa-info-box .zona-bairros {
  font-size: 0.8rem;
  color: var(--azul-corporativo);
  line-height: 1.6;
}
.mapa-count-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--gradient-diagonal);
  color: var(--branco);
  padding: 12px 20px;
  border-radius: var(--border-radius-m);
  font-size: 0.88rem;
  font-weight: 700;
  white-space: nowrap;
  min-width: 160px;
  max-height: 210px;
  box-shadow: 0 4px 14px rgba(0,119,182,0.3);
}
.mapa-count-badge ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}
.mapa-count-badge ul li span { font-size: 2.4rem; font-weight: 800; line-height: 1; }
.mapa-count-badge ul li { font-size: 0.85rem; }

/* ── LAYOUT PRINCIPAL ──────────────────────────── */
.container-main {
  max-width: 1400px !important;
  min-width: 320px;
  margin: 24px auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── SIDEBAR FILTROS ───────────────────────────── */
.sidebar {
  background: var(--branco);
  padding: 18px 22px;
  border-radius: var(--border-radius-g);
  box-shadow: 0 4px 20px rgba(3,4,94,0.08);
  border-top: var(--borda-g) solid var(--ceu-tecnologico);
  min-width: 280px;
}
.sidebar h3 {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 14px;
  color: var(--azul-royal);
  display: flex;
  align-items: center;
  gap: 8px;
}
.sidebar-fields {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 12px 16px;
}
.sidebar-field { flex: 1 1 160px; min-width: 140px; }
.sidebar-field label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--azul-corporativo);
  margin-bottom: 6px;
}
.sidebar-btn-wrap { flex: 0 0 auto; min-width: unset; align-self: flex-end; }
select, input[type=number], input[type=text] {
  width: 100%;
  padding: 10px 14px;
  border: var(--borda-p) solid var(--agua-cristalina);
  border-radius: var(--border-radius-m);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: var(--azul-royal);
  outline: none;
  background: var(--branco);
  transition: border-color 0.2s, box-shadow 0.2s;
}
select:focus, input[type=number]:focus, input[type=text]:focus {
  border-color: var(--azul-corporativo);
  box-shadow: 0 0 0 3px rgba(0,119,182,0.12);
}
.btn-buscar {
  padding: 11px 22px;
  background: var(--gradient-horizontal);
  color: var(--branco);
  border: none;
  border-radius: var(--border-radius-m);
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(0,119,182,0.3);
  transition: opacity 0.2s, transform 0.2s;
}
.btn-buscar:hover { opacity: 0.9; transform: translateY(-1px); }

/* ── HEADER DA LISTAGEM ────────────────────────── */
.main-header { display: flex; flex-wrap: wrap; }
.main-header h2 {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--azul-royal);
}
.contagem { font-size: 0.9rem; color: var(--azul-corporativo); }
.contagem strong { color: var(--ceu-tecnologico); font-weight: 700; }

/* ── CARDS DE IMÓVEIS ──────────────────────────── */
.listings {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  min-width: 280px;
}
.card {
  background: var(--branco);
  border-radius: var(--border-radius-g);
  overflow: hidden;
  box-shadow: 0 4px 18px rgba(3,4,94,0.09);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  border-bottom: var(--borda-m) solid transparent;
  min-width: 260px;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 14px 36px rgba(3,4,94,0.16);
  border-bottom-color: var(--ceu-tecnologico);
}
.card-img-wrap { position: relative; overflow: hidden; }
.card img {
  width: 100%;
  height: 210px;
  object-fit: cover;
  display: block;
  transition: transform 0.4s;
}
.card:hover img { transform: scale(1.04); }
.card-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--gradient-diagonal-royal);
  color: var(--branco);
  padding: 4px 12px;
  border-radius: var(--border-radius-gg);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.card-body { padding: 16px; }
.card-body h3 {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--azul-royal);
}
.price {
  font-family: 'Syne', sans-serif;
  font-size: 1.45rem;
  font-weight: 800;
  background: var(--gradient-horizontal);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
  margin-bottom: 8px;
}
.details {
  display: flex;
  gap: 14px;
  margin: 8px 0;
  font-size: 0.88rem;
  color: var(--azul-corporativo);
}
.details span { display: flex; align-items: center; gap: 5px; }
.details i { color: var(--ceu-tecnologico); }
.city-label {
  font-size: 0.85rem;
  color: var(--azul-corporativo);
  opacity: 0.8;
  margin-bottom: 12px;
}
.btn-whats {
  background: var(--gradient-noite-ate-ceu);
  color: var(--branco);
  border: none;
  padding: 10px;
  width: 100%;
  border-radius: var(--border-radius-m);
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.btn-whats:hover { opacity: 0.9; transform: translateY(-1px); }

/* ── ERROS ─────────────────────────────────────── */
.erro-lista {
  color: #d97706;
  font-size: 0.85rem;
  padding: 8px 0;
  margin-bottom: 12px;
}

/* ── RESPONSIVIDADE DASHBOARD ──────────────────── */
@media (max-width: 992px) {
  .col-12.col-md-7 svg { width: 100% !important; }
  .mapa-info-box { max-height: none; }
  .mapa-count-badge { max-height: none; }
}

@media (max-width: 768px) {
  /* Mapa */
  .col-12.col-md-2 { flex-direction: row !important; flex-wrap: wrap; top: 0 !important; }
  .zona-btn { height: 36px; font-size: 0.72rem; min-width: 90px; padding: 6px 10px; }
  .col-12.col-md-7 svg { width: 100% !important; }
  .mapa-info-box { min-width: 100%; max-height: none; }
  .mapa-count-badge { min-width: 100%; max-height: none; justify-content: center; }

  /* Sidebar filtros */
  .sidebar { min-width: 100%; padding: 14px 16px; }
  .sidebar-fields { gap: 8px 12px; }
  .sidebar-field { flex: 1 1 140px; min-width: 130px; }

  /* Container */
  .container-main { padding: 0 12px; margin: 16px auto; gap: 16px; }

  /* Listagem */
  .listings { grid-template-columns: 1fr; gap: 14px; }
  .card { min-width: 100%; }
  .main-header { flex-direction: column; gap: 4px; }
}

@media (max-width: 480px) {
  .zona-btn { font-size: 0.68rem; min-width: 80px; padding: 5px 8px; }
  .card img { height: 180px; }
  .price { font-size: 1.2rem; }
  .mapa-section .section-title { font-size: 0.75rem; }
}
</style>
