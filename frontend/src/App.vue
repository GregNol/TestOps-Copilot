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
const showModeSelector = ref(true)
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
  
  // Не создаём чат автоматически - ждём выбора режима
  setTimeout(() => {
    document.documentElement.classList.add('initialized')
    isInitialized.value = true
  }, 50)
})

const selectMode = (mode: 'ui' | 'api' | 'general') => {
  appStore.createNewChat(mode)
  showModeSelector.value = false
}

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
    
    // Показываем красивое уведомление об ошибке
    $q.notify({
      type: 'negative',
      message: '⚠️ Ошибка запроса',
      caption: message,
      position: 'top',
      timeout: 6000,
      icon: 'error_outline',
      textColor: 'white',
      actions: [
        { label: 'Закрыть', color: 'white', handler: () => {} }
      ],
      classes: 'error-notification'
    })
    appStore.addMessage({ role: 'assistant', content: `**Ошибка:**\n\n${message}` })
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
  <q-dialog v-model="showModeSelector" persistent>
    <q-card class="mode-selector-card">
      <q-card-section class="bg-primary text-white text-center">
        <h6 class="q-my-md">Выберите режим работы</h6>
      </q-card-section>
      <q-card-section class="mode-grid">
        <q-btn
          class="mode-btn"
          label="UI Тестирование"
          color="info"
          icon="web"
          size="lg"
          padding="md"
          @click="selectMode('ui')"
        />
        <q-btn
          class="mode-btn"
          label="API Тестирование"
          color="warning"
          icon="api"
          size="lg"
          padding="md"
          @click="selectMode('api')"
        />
        <q-btn
          class="mode-btn"
          label="Общий режим"
          color="secondary"
          icon="chat"
          size="lg"
          padding="md"
          @click="selectMode('general')"
        />
      </q-card-section>
    </q-card>
  </q-dialog>

  <Layout
    v-if="isInitialized && !showModeSelector"
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
.mode-selector-card {
  min-width: 500px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.mode-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 2rem;
}

.mode-btn {
  border-radius: 12px !important;
  font-weight: 600;
  transition: all 0.3s ease;
}

.mode-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

:global(.error-notification) {
  border-radius: 12px !important;
  box-shadow: 0 8px 24px rgba(239, 68, 68, 0.2) !important;
}
</style>
