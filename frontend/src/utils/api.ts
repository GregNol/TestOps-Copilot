import { Notify } from 'quasar'

// Normalize base URL to avoid duplicated /api/v1/ai prefixes from env
const RAW_BASE = import.meta.env.VITE_API_BASE || 'http://localhost'
// Для localhost убираем явный порт: http://localhost:8080 -> http://localhost
const NORMALIZED_HOST = RAW_BASE.replace(/^(https?:\/\/localhost)(:\d+)?/i, '$1')
const CLEAN_BASE = NORMALIZED_HOST
  .replace(/\/api\/v1\/ai\/?$/, '')
  .replace(/\/api\/v1\/?$/, '')
  .replace(/\/$/, '')

const AI_BASE = `${CLEAN_BASE}/api/v1/ai`
const PING_URL = `${CLEAN_BASE}/api/v1/ping`

async function handleResponse(response: Response): Promise<string> {
  let text: string
  try {
    text = await response.text()
  } catch (error) {
    const errorMsg = 'Не удалось прочитать ответ сервера'
    Notify.create({
      type: 'negative',
      message: 'Ошибка сети',
      caption: errorMsg,
      position: 'top-right',
      timeout: 5000,
      icon: 'cloud_off',
    })
    throw new Error(errorMsg)
  }

  if (!response.ok) {
    const message = text || response.statusText || 'Сервер вернул ошибку'
    Notify.create({
      type: 'negative',
      message: `Ошибка ${response.status}`,
      caption: message,
      position: 'top-right',
      timeout: 5000,
      icon: 'error',
    })
    throw new Error(message)
  }

  try {
    const json = JSON.parse(text)
    if (json && typeof json === 'object' && 'message' in json) {
      return String(json.message)
    }
    return JSON.stringify(json, null, 2)
  } catch (_) {
    return text
  }
}

async function safeFetch(url: string, options: RequestInit): Promise<Response> {
  try {
    return await fetch(url, options)
  } catch (error) {
    if (error instanceof TypeError) {
      const msg = 'Сервер недоступен. Проверьте подключение к API.'
      Notify.create({
        type: 'negative',
        message: 'Ошибка подключения',
        caption: msg,
        position: 'top-right',
        timeout: 6000,
        icon: 'cloud_off',
      })
      throw new Error(msg)
    }
    throw error
  }
}

export async function generateUiTests(body: {
  url: string
  general_description: string
  modules: string
  buttons_description?: string
  special_scenarios?: string
}): Promise<string> {
  const response = await safeFetch(`${AI_BASE}/generate-ui-tests`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return handleResponse(response)
}

export async function generateApiTests(body: {
  file: File
  general_description?: string
  modules?: string
}): Promise<string> {
  const formData = new FormData()
  formData.append('file', body.file)
  formData.append('general_description', body.general_description || 'API спецификация')
  formData.append('modules', body.modules || 'Auto-detected')

  const response = await safeFetch(`${AI_BASE}/generate-api-tests`, {
    method: 'POST',
    body: formData,
  })
  return handleResponse(response)
}

export async function redactContent(body: {
  original_content: string
  edit_instructions: string
}): Promise<string> {
  const response = await safeFetch(`${AI_BASE}/redact-content`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return handleResponse(response)
}

export async function optimizeTests(body: {
  modules: string
  test_cases: string
}): Promise<string> {
  const response = await safeFetch(`${AI_BASE}/optimize-tests`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return handleResponse(response)
}

export async function generateCodePytest(body: {
  url: string
  general_description: string
  approved_test_plan: string
}): Promise<string> {
  const response = await safeFetch(`${AI_BASE}/generate-code-pytest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return handleResponse(response)
}

export async function reviewCode(body: {
  code_snippet: string
  rules: string
}): Promise<string> {
  const response = await safeFetch(`${AI_BASE}/review-code`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return handleResponse(response)
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(PING_URL, { method: 'GET' })
    return response.ok
  } catch (error) {
    console.warn('Health check failed:', error)
    return false
  }
}
export { AI_BASE }
