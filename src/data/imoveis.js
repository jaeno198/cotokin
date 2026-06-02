export const imoveis = [
  { id: 1, titulo: 'Casa moderna com piscina',           preco: 850000, tipo: 'casa',        quartos: 4, banheiros: 3, area: 280, cidade: 'Jd. Alvorada — Zona Norte',       zona: 'norte',  img: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=70', tag: 'Destaque' },
  { id: 2, titulo: 'Apartamento 3 quartos vista parque', preco: 620000, tipo: 'apartamento', quartos: 3, banheiros: 2, area: 95,  cidade: 'Centro — Zona Central',           zona: 'centro', img: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=70' },
  { id: 3, titulo: 'Terreno residencial 800m²',          preco: 245000, tipo: 'terreno',     quartos: 0, banheiros: 0, area: 800, cidade: 'Jd. Guanabara — Zona Sul',        zona: 'sul',    img: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&q=70' },
  { id: 4, titulo: 'Casa 4 quartos com área gourmet',    preco: 980000, tipo: 'casa',        quartos: 4, banheiros: 3, area: 320, cidade: 'Jd. Novo Horizonte — Zona Leste', zona: 'leste',  img: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&q=70', tag: 'Novo' },
  { id: 5, titulo: 'Apartamento compacto 2 quartos',     preco: 320000, tipo: 'apartamento', quartos: 2, banheiros: 1, area: 62,  cidade: 'Jd. Universo — Zona Oeste',       zona: 'oeste',  img: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600&q=70' },
  { id: 6, titulo: 'Sobrado 3 quartos com suíte',        preco: 740000, tipo: 'casa',        quartos: 3, banheiros: 2, area: 190, cidade: 'Cj. Requião — Zona Sul',          zona: 'sul',    img: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600&q=70' },
]

export const ZONAS_CFG = {
  all:    { cor: '#0077B6', fill: '#e0f3fa', stroke: '#90E0EF', text: '#03045e', hover: '#00B4D8', nome: 'Toda Maringá',  bairros: 'Todos os bairros disponíveis em Maringá.', count: '1.248' },
  centro: { cor: '#2563eb', fill: '#bfdbfe', stroke: '#93c5fd', text: '#1e40af', hover: '#2563eb', nome: 'Centro',        bairros: 'Centro, Zona 01, Zona 02, Zona 03, Zona 04.', count: '342' },
  norte:  { cor: '#059669', fill: '#a7f3d0', stroke: '#6ee7b7', text: '#065f46', hover: '#059669', nome: 'Zona Norte',    bairros: 'Jd. Alvorada, Vila Operária, Pq. das Grevíleas, Jd. Imperial, Pq. Res. Japão, Cj. Inocente.', count: '287' },
  sul:    { cor: '#dc2626', fill: '#fecaca', stroke: '#f87171', text: '#991b1b', hover: '#dc2626', nome: 'Zona Sul',      bairros: 'Jd. Pinheiros, Jd. Guanabara, Cj. Requião, Jd. Alpes, Jd. Liberdade, Cidade Alta, Cidade Industrial.', count: '315' },
  leste:  { cor: '#d97706', fill: '#fde68a', stroke: '#fbbf24', text: '#92400e', hover: '#d97706', nome: 'Zona Leste',    bairros: 'Jd. Novo Horizonte, Jd. Borba Gato, Jd. Itaipu.', count: '168' },
  oeste:  { cor: '#7c3aed', fill: '#ddd6fe', stroke: '#c4b5fd', text: '#4c1d95', hover: '#7c3aed', nome: 'Zona Oeste',   bairros: 'Jd. Iguaçu, Jd. Universo, Pq. das Palmeiras.', count: '136' },
}

export const BTNS_STYLE = {
  all:    'background:#0077B6;color:#fff;border-color:#0077B6;',
  centro: 'background:#2563eb;color:#fff;border-color:#2563eb;',
  norte:  'background:#059669;color:#fff;border-color:#059669;',
  sul:    'background:#dc2626;color:#fff;border-color:#dc2626;',
  leste:  'background:#d97706;color:#fff;border-color:#d97706;',
  oeste:  'background:#7c3aed;color:#fff;border-color:#7c3aed;',
}
