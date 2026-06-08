<template>
  <div>

    <!-- MAPA DE ZONAS -->
    <h1> Selecione 1 regiao   <h1>
    <section class="mapa-section">
      <div class="container-mx-auto py-3 px-4">

        <div class="section-title">
          <i class="fas fa-map-marked-alt"></i> Buscar por zona — Maringá PR
        </div>

        <div class="row g-2 align-items-start">

          <!-- COL 1 — Botões de zona -->
          <div class="col-12 col-md-2 d-flex flex-column gap-2">
            <button v-for="(cfg, key) in ZONAS_CFG" :key="key" class="zona-btn w-100" style='height: 10vh;'
              :id="`zbtn-${key}`" :class="{ active: zonaAtiva === key }"
              :style="zonaAtiva === key ? BTNS_STYLE[key] : ''" @click="handleSelecionarZona(key)" Novo Horizonte>
              <span class="zdot" :style="`background:${key === 'all' ? 'rgba(255,255,255,0.7)' : cfg.cor}`"></span>
              {{ key === 'all' ? 'Toda Maringá' : cfg.nome }}
            </button>
          </div>

          <!-- COL 2 — Mapa SVG -->
          <div class="col-12 col-md-7" style="position:relative;">
            <div ref="tooltipEl" class="mapa-tooltip"></div>
            <svg ref="svgEl" viewBox="0 -4 400 420" xmlns="http://www.w3.org/2000/svg"
              style="width:75%; height:auto; cursor:pointer; display:block;">

              <!-- NORTE -->
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

              <!-- LESTE -->
              <g class="zgrp" data-zona="leste">
                <rect class="zp" x="310" y="135" width="80" height="55" rx="4" data-b="Jd. Novo Horizonte" />
                <rect class="zp" x="310" y="195" width="80" height="55" rx="4" data-b="Jd. Borba Gato" />
                <rect class="zp" x="310" y="255" width="80" height="55" rx="4" data-b="Jd. Itaipu" />
                <text class="zlabel" x="350" y="163">Novo Horizonte</text>
                <text class="zlabel" x="350" y="223">Borba Gato</text>
                <text class="zlabel" x="350" y="283">Jd. Itaipu</text>
              </g>

              <!-- OESTE -->
              <g class="zgrp" data-zona="oeste">
                <rect class="zp" x="10" y="135" width="75" height="55" rx="4" data-b="Jd. Iguaçu" />
                <rect class="zp" x="10" y="195" width="75" height="55" rx="4" data-b="Jd. Universo" />
                <rect class="zp" x="10" y="255" width="75" height="55" rx="4" data-b="Pq. das Palmeiras" />
                <text class="zlabel" x="47" y="163">Jd. Iguaçu</text>
                <text class="zlabel" x="47" y="223">Jd. Universo</text>
                <text class="zlabel" x="47" y="283">Pq. Palmeiras</text>
              </g>

              <!-- CENTRO -->
              <g class="zgrp" data-zona="centro">
                <rect class="zp" x="90" y="135" width="215" height="70" rx="4" data-b="Centro / Zonas 01-04" />
                <rect class="zp" x="90" y="210" width="100" height="55" rx="4" data-b="Zona 01 / Zona 02" />
                <rect class="zp" x="195" y="210" width="110" height="55" rx="4" data-b="Zona 03 / Zona 04" />
                <text class="zlabel" x="197" y="168" style="font-size:12px;font-weight:700;">C E N T R O</text>
                <text class="zlabel" x="197" y="183" style="font-size:9px;">⛪ Catedral de Maringá</text>
                <text class="zlabel" x="140" y="238">Zona 01/02</text>
                <text class="zlabel" x="250" y="238">Zona 03/04</text>
              </g>

              <!-- SUL -->
              <g class="zgrp" data-zona="sul">
                <rect class="zp" x="90" y="275" width="65" height="50" rx="4" data-b="Jd. Pinheiros" />
                <rect class="zp" x="160" y="275" width="65" height="50" rx="4" data-b="Jd. Guanabara" />
                <rect class="zp" x="230" y="275" width="75" height="50" rx="4" data-b="Cj. Requião" />
                <rect class="zp" x="90" y="330" width="65" height="55" rx="4" data-b="Jd. Alpes" />
                <rect class="zp" x="160" y="330" width="65" height="55" rx="4" data-b="Jd. Liberdade" />
                <rect class="zp" x="230" y="330" width="75" height="55" rx="4" data-b="Cidade Alta" />
                <rect class="zp" x="90" y="390" width="215" height="25" rx="4"
                  data-b="Sta. Felicidade / Cidade Industrial" />
                <text class="zlabel" x="122" y="301">Jd. Pinheiros</text>
                <text class="zlabel" x="192" y="301">Guanabara</text>
                <text class="zlabel" x="267" y="301">Cj. Requião</text>
                <text class="zlabel" x="122" y="358">Jd. Alpes</text>
                <text class="zlabel" x="192" y="358">Jd. Liberdade</text>
                <text class="zlabel" x="267" y="358">Cidade Alta</text>
                <text class="zlabel" x="197" y="405">Sta. Felicidade / Cidade Industrial</text>
              </g>

              <!-- Setas cardinais -->
              <text x="197" y="20" style="font-size:10px;font-weight:700;
          text-anchor:middle;fill:#0077B6;
          font-family:'DM Sans',sans-serif;">↑ NORTE</text>

              <text x="197" y="390" style="font-size:10px;font-weight:700;
           text-anchor:middle;fill:#0077B6;
           font-family:'DM Sans',sans-serif;">↓ SUL</text>

              <text x="15" y="234" style="font-size:9px;font-weight:700;
          text-anchor:middle;fill:#0077B6;
          font-family:'DM Sans',sans-serif;" transform="rotate(-90 6 232)">OESTE</text>

              <text x="398" y="235" style="font-size:9px;font-weight:700;
          text-anchor:middle;fill:#0077B6;
          font-family:'DM Sans',sans-serif;" transform="rotate(90 398 218)">LESTE</text>
            </svg>
          </div>

          <!-- COL 3 — Info bairros -->
          <div class="col-12 col-md-3 d-flex flex-column gap-3 justify-content-start">
            <div class="mapa-info-box" :style="`border-left-color: ${cfgAtiva.cor}`">
              <div class="zona-nome">{{ cfgAtiva.nome }}</div>
              <div class="zona-bairros">{{ cfgAtiva.bairros }}</div>
            </div>
            <div class="mapa-count-badge">
              <i class="fas fa-home"></i>
              <ul>

              <li><span>{{ cfgAtiva.count }}</span> </li>
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
            <button class="btn-buscar">
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
            {{ modalidade === 'venda' ? 'Imóveis à Venda' : modalidade === 'aluguel' ? 'Imóveis para Alugar' : 'ImóveisRurais' }}
          </h2>
          <p class="contagem">Encontrei <strong>{{ imoveisFiltrados.length }}</strong> imóveis</p>
        </div>

        <div class="listings">
          <div v-for="imovel in imoveisFiltrados" :key="imovel.id" class="card">
            <div class="card-img-wrap">
              <img :src="imovel.img" :alt="imovel.titulo" loading="lazy" />
              <span v-if="imovel.tag" class="card-tag">{{ imovel.tag }}</span>
            </div>
            <div class="card-body">
              <h3>{{ imovel.titulo }}</h3>
              <div class="price">R$ {{ imovel.preco.toLocaleString('pt-BR') }}</div>
              <div class="details">
                <span><i class="fas fa-bed"></i> {{ imovel.quartos }}</span>
                <span><i class="fas fa-bath"></i> {{ imovel.banheiros }}</span>
                <span><i class="fas fa-ruler-combined"></i> {{ imovel.area }}m²</span>
              </div>
              <p class="city-label">
                <i class="fas fa-map-marker-alt" style="color:var(--ceu-tecnologico)"></i>
                {{ imovel.cidade }}
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
import { ref, onMounted } from 'vue'
import { useZona } from '@/composables/useZona'

const {
  zonaAtiva,
  modalidade,
  tipoFiltro,
  precoMin,
  precoMax,
  quartosFiltro,
  imoveisFiltrados,
  cfgAtiva,
  selecionarZona,
  ZONAS_CFG,
  BTNS_STYLE,
} = useZona()

const tooltipEl = ref(null)
const svgEl = ref(null)

function aplicarCoresMapa() {
  document.querySelectorAll('.zgrp').forEach(g => {
    const z = g.dataset.zona
    const ativo = zonaAtiva.value === 'all' || zonaAtiva.value === z
    const cfg = ZONAS_CFG[z]
    g.querySelectorAll('.zp').forEach(el => {
      el.style.fill = ativo ? cfg.fill : '#f1f5f9'
      el.style.stroke = ativo ? cfg.stroke : '#cbd5e1'
      el.style.opacity = ativo ? '1' : '0.3'
    })
    g.querySelectorAll('.zlabel').forEach(el => {
      el.style.fill = ativo ? cfg.text : '#94a3b8'
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

onMounted(() => {
  aplicarCoresMapa()

  document.querySelectorAll('.zp').forEach(el => {
    el.addEventListener('mouseenter', () => {
      const z = el.closest('.zgrp').dataset.zona
      el.style.fill = ZONAS_CFG[z].hover
      el.style.opacity = '1'
      tooltipEl.value.style.display = 'block'
      tooltipEl.value.textContent = (el.dataset.b || '') + ' — ' + ZONAS_CFG[z].nome
    })
    el.addEventListener('mousemove', e => {
      const r = svgEl.value.parentElement.getBoundingClientRect()
      tooltipEl.value.style.left = (e.clientX - r.left + 12) + 'px'
      tooltipEl.value.style.top = (e.clientY - r.top - 38) + 'px'
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
.zona-btn {
  font-size: 25px !important;
  font-weight: auto;
  text-align: center;
  padding-left: 25%;
  position: relative;
  top: 10vh;
}
.mapa-info-box{
  margin: 0 auto;
  position: relative;
  top: 50vh;
}
.mapa-count-badge{
  font-size: 30px;


}


.mapa-count-badge span{
  font-size: 80px;
}
</style>
