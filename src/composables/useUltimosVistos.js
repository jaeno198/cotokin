const CHAVE = 'geohouse_ultimos_vistos'
const MAX = 10

export function useUltimosVistos() {
  function carregar() {
    try {
      return JSON.parse(localStorage.getItem(CHAVE) || '[]')
    } catch {
      return []
    }
  }

  function registrar(imovel) {
    const lista = carregar().filter(i => i.id !== imovel.id)
    lista.unshift({
      id: imovel.id,
      titulo: imovel.titulo,
      preco: imovel.preco || imovel.preco_venda || 0,
      cidade: imovel.cidade || imovel.bairro || '',
      quartos: imovel.quartos || 0,
      img: imovel.img || imovel.foto_capa || '',
      visto_em: Date.now(),
    })
    localStorage.setItem(CHAVE, JSON.stringify(lista.slice(0, MAX)))
  }

  function limpar() {
    localStorage.removeItem(CHAVE)
  }

  return { carregar, registrar, limpar }
}
