import { ref, computed } from 'vue'
import { imoveis, ZONAS_CFG, BTNS_STYLE } from '@/data/imoveis'

export function useZona() {
  const zonaAtiva    = ref('all')
  const modalidade   = ref('venda')
  const tipoFiltro   = ref('')
  const precoMin     = ref(null)
  const precoMax     = ref(null)
  const quartosFiltro = ref('')

  const imoveisFiltrados = computed(() => {
    let lista = zonaAtiva.value === 'all'
      ? imoveis
      : imoveis.filter(i => i.zona === zonaAtiva.value)

    if (tipoFiltro.value)
      lista = lista.filter(i => i.tipo === tipoFiltro.value)
    if (precoMin.value)
      lista = lista.filter(i => i.preco >= parseFloat(precoMin.value))
    if (precoMax.value)
      lista = lista.filter(i => i.preco <= parseFloat(precoMax.value))
    if (quartosFiltro.value)
      lista = lista.filter(i => i.quartos >= parseInt(quartosFiltro.value))

    return lista
  })

  const cfgAtiva = computed(() => ZONAS_CFG[zonaAtiva.value])

  function selecionarZona(zona) {
    zonaAtiva.value = zona
  }

  function buscarTexto(texto) {
    const t = texto.toLowerCase()
    return imoveis.filter(i =>
      i.titulo.toLowerCase().includes(t) || i.cidade.toLowerCase().includes(t)
    )
  }

  return {
    zonaAtiva,
    modalidade,
    tipoFiltro,
    precoMin,
    precoMax,
    quartosFiltro,
    imoveisFiltrados,
    cfgAtiva,
    selecionarZona,
    buscarTexto,
    ZONAS_CFG,
    BTNS_STYLE,
  }
}
