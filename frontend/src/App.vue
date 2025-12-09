<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import Layout from './components/Layout.vue'
import { useAppStore } from './stores/appStore'
import { useQuasar } from 'quasar'
import {
  generateApiTests,
  generateCodePytest,
  generateUiTests,
  optimizeTests,
  redactContent,
  reviewCode,
} from './utils/api'

const appStore = useAppStore()
const isInitialized = ref(false)
const $q = useQuasar()

// Computed для реактивности
const messages = computed(() => appStore.messages)
const isLoading = computed(() => appStore.isLoading)
const chatHistories = computed(() => appStore.chatHistories)
const currentChatId = computed(() => appStore.currentChatId)
const currentChatType = computed(() => appStore.currentChatType)

onMounted(() => {
  appStore.initializeTheme()
  appStore.initializeChatHistory()
  
  if (!appStore.chatHistories || appStore.chatHistories.length === 0) {
    appStore.createNewChat('general')
  }
  setTimeout(() => {
    document.documentElement.classList.add('initialized')
    isInitialized.value = true
  }, 50)
})

const getLastAssistantContent = () => {
  const reversed = [...appStore.messages].reverse()
  const lastAssistant = reversed.find(message => message.role === 'assistant')
  return lastAssistant?.content || ''
}

const handleSendMessage = async (payload: { text: string; file: File | null }) => {
  const trimmed = payload.text?.trim() || ''
  const hasFile = Boolean(payload.file)

  if (!trimmed && !hasFile) return

  if (!appStore.currentChatId) {
    appStore.createNewChat('general')
  }

  const userContent = [trimmed, hasFile ? `\n\nФайл: ${payload.file?.name}` : ''].filter(Boolean).join('')
  appStore.addMessage({ role: 'user', content: userContent })
  appStore.setIsLoading(true)

  try {
    let responseText = ''

    // Определяем метод в зависимости от типа чата и команд
    const chatType = currentChatType.value

    if (hasFile && payload.file) {
      // Загрузка файла спецификации
      responseText = await generateApiTests({
        file: payload.file,
        general_description: trimmed || 'API спецификация',
        modules: 'Auto-detected',
      })
    } else if (trimmed.startsWith('/redact')) {
      const instructions = trimmed.replace('/redact', '').trim() || 'Обнови контент'
      const originalContent = getLastAssistantContent() || instructions
      responseText = await redactContent({
        original_content: originalContent,
        edit_instructions: instructions,
      })
    } else if (trimmed.startsWith('/optimize')) {
      const detail = trimmed.replace('/optimize', '').trim()
      const cases = getLastAssistantContent() || detail
      responseText = await optimizeTests({
        modules: detail || 'Общие модули',
        test_cases: cases,
      })
    } else if (trimmed.startsWith('/code')) {
      const detail = trimmed.replace('/code', '').trim()
      const plan = getLastAssistantContent() || detail
      const urlMatch = detail.match(/https?:\/\/\S+/)?.[0] || ''
      responseText = await generateCodePytest({
        url: urlMatch,
        general_description: detail || 'Генерация кода из плана',
        approved_test_plan: plan,
      })
    } else if (trimmed.startsWith('/review')) {
      const detail = trimmed.replace('/review', '').trim()
      const code = detail || getLastAssistantContent() || 'print("Hello, TestOps")'
      responseText = await reviewCode({
        code_snippet: code,
        rules: 'Стандарты TestOps',
      })
    } else if (chatType === 'api') {
      // API тестирование
      responseText = await generateApiTests({
        file: new File([], 'spec.json'),
        general_description: trimmed,
        modules: 'Auto-detected',
      })
    } else {
      // UI тестирование (по умолчанию)
      responseText = await generateUiTests({
        url: '',
        general_description: trimmed,
        modules: '',
        buttons_description: '',
        special_scenarios: '',
      })
    }

    appStore.addMessage({ role: 'assistant', content: responseText })
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Неизвестная ошибка'
    
    // Показываем уведомление об ошибке
    $q.notify({
      type: 'negative',
      message: 'Не удалось получить ответ от API',
      caption: message,
      position: 'top-right',
      timeout: 5000,
      icon: 'error_outline',
      actions: [
        { label: 'Закрыть', color: 'white', handler: () => {} }
      ]
    })
    appStore.addMessage({ role: 'assistant', content: `Ошибка запроса: ${message}` })
  } finally {
    appStore.setIsLoading(false)
  }
}

const handleSelectChat = (id: string) => {
  appStore.setCurrentChatId(id)
}

const handleRemoveChat = (id: string) => {
  appStore.removeChatHistory(id)
}

const handleNewChat = () => {
  appStore.createNewChat('general')
}

const handleClearAllChats = () => {
  const chats = [...appStore.chatHistories]
  chats.forEach(chat => {
    appStore.removeChatHistory(chat.id)
  })
}
</script>

<template>
  <Layout
    v-if="isInitialized"
    :messages="messages"
    :is-loading="isLoading"
    :chat-histories="chatHistories"
    :current-chat-id="currentChatId"
    @send-message="handleSendMessage"
    @select-chat="handleSelectChat"
    @remove-chat="handleRemoveChat"
    @new-chat="handleNewChat"
    @clear-all-chats="handleClearAllChats"
  />
</template>

<style scoped>
/* empty - styling in global CSS */
</style>
