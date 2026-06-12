// src/services/api.js
// Centraliza todas as chamadas à API do GEO HOUSE

const BASE_URL = '/api'

// ── Helpers ──────────────────────────────────────────────────────────────────

function getToken() {
  return localStorage.getItem('access_token')
}

function setTokens(access, refresh) {
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}

function clearTokens() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

async function request(method, path, body = null, auth = false) {
  const headers = { 'Content-Type': 'application/json' }

  if (auth) {
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`
  }

  const opts = { method, headers }
  if (body) opts.body = JSON.stringify(body)

  const res = await fetch(`${BASE_URL}${path}`, opts)

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Erro desconhecido' }))
    throw new Error(err.detail || `Erro ${res.status}`)
  }

  return res.json()
}

// ── Auth ──────────────────────────────────────────────────────────────────────

export async function login(email, senha) {
  // FastAPI OAuth2 usa form-data, não JSON
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', senha)

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    body: form,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'E-mail ou senha incorretos' }))
    throw new Error(err.detail || 'Erro ao fazer login')
  }

  const data = await res.json()
  setTokens(data.access_token, data.refresh_token)
  return data
}

export async function logout() {
  clearTokens()
}

export async function getMe() {
  return request('GET', '/auth/me', null, true)
}

// ── Usuários ──────────────────────────────────────────────────────────────────

export async function cadastrar(dados) {
  // POST /usuarios — auto-registro público
  return request('POST', '/usuarios/', dados)
}

// ── Imóveis ───────────────────────────────────────────────────────────────────

export async function getImoveis(params = {}) {
  const query = new URLSearchParams(params).toString()
  return request('GET', `/imoveis/?${query}`)
}

export async function getImovel(id) {
  return request('GET', `/imoveis/${id}`)
}

// ── Contatos ──────────────────────────────────────────────────────────────────

export async function enviarContato(dados) {
  return request('POST', '/contatos/', dados)
}
