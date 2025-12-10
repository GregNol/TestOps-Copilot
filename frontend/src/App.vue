<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import Layout from './components/Layout.vue'
import ModeSelectionDialog from './components/ModeSelectionDialog.vue'
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
const showModeDialog = computed({
  get: () => appStore.showModeDialog,
  set: (val) => appStore.setShowModeDialog(val)
})

onMounted(() => {
  appStore.initializeTheme()
  appStore.initializeChatHistory()
  
  // Don't create a chat automatically - wait for mode selection
  if (!appStore.chatHistories || appStore.chatHistories.length === 0) {
    appStore.setShowModeDialog(true)
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

// Проверка, хочет ли пользователь утвердить план
const isApprovalMessage = (text: string): boolean => {
  const lower = text.toLowerCase().trim()
  const approvalKeywords = ['готово', 'ок', 'да', 'утверждаю', 'одобряю', 'генерируй код', 'давай код', 'кодом']
  return approvalKeywords.some(keyword => lower.includes(keyword))
}

// Извлечение данных из первого сообщения для UI тестов
const parseUiTestRequest = (text: string) => {
  const urlMatch = text.match(/https?:\/\/\S+/)
  return {
    url: urlMatch?.[0] || '',
    general_description: text,
    modules: '',
    buttons_description: '',
    special_scenarios: '',
  }
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
    const chatType = currentChatType.value
    const currentStep = appStore.currentWorkflowStep

    // ============ WORKFLOW STATE MACHINE ============
    
    if (currentStep === 'idle' && chatType) {
      // Шаг 1: Генерация начального тест-плана (таблицы)
      
      if (chatType === 'ui') {
        const uiData = parseUiTestRequest(trimmed)
        responseText = await generateUiTests(uiData)
        appStore.setWorkflowStep('generate-ui')
        appStore.updateWorkflowData({ testPlan: responseText })
        
        // Добавляем подсказку для пользователя
        responseText += '\n\n---\n**Вы можете:**\n- Попросить отредактировать план\n- Написать "готово" для генерации кода'
        
      } else if (chatType === 'api') {
        if (!hasFile || !payload.file) {
          responseText = '⚠️ Пожалуйста, прикрепите файл OpenAPI спецификации (JSON/YAML)'
        } else {
          responseText = await generateApiTests({
            file: payload.file,
            general_description: trimmed || 'API спецификация',
            modules: 'Auto-detected',
          })
          appStore.setWorkflowStep('generate-api')
          appStore.updateWorkflowData({ testPlan: responseText })
          
          // Добавляем подсказку для пользователя
          responseText += '\n\n---\n**Вы можете:**\n- Попросить отредактировать план\n- Написать "готово" для генерации кода'
        }
      }
      
    } else if (currentStep === 'generate-ui' || currentStep === 'generate-api') {
      // Шаг 2: Редактирование плана или утверждение
      
      if (isApprovalMessage(trimmed)) {
        // Пользователь утвердил план - переходим к генерации кода
        const testPlan = appStore.workflowData.testPlan || ''
        
        if (!testPlan) {
          responseText = '⚠️ Не найден тест-план для генерации кода. Начните сначала.'
          appStore.setWorkflowStep('idle')
        } else {
          // Извлекаем URL из истории сообщений
          const firstUserMsg = appStore.messages.find(m => m.role === 'user')?.content || ''
          const urlMatch = firstUserMsg.match(/https?:\/\/\S+/)
          
          responseText = await generateCodePytest({
            url: urlMatch?.[0] || '',
            general_description: trimmed,
            approved_test_plan: testPlan,
          })
          
          appStore.setWorkflowStep('complete')
          appStore.updateWorkflowData({ code: responseText })
          
          responseText += '\n\n---\n✅ **Код сгенерирован!** Можете начать новый чат для другого проекта.'
        }
        
      } else {
        // Пользователь хочет отредактировать план
        const originalPlan = appStore.workflowData.testPlan || ''
        
        if (!originalPlan) {
          responseText = '⚠️ Не найден план для редактирования. Начните сначала.'
          appStore.setWorkflowStep('idle')
        } else {
          responseText = await redactContent({
            original_content: originalPlan,
            edit_instructions: trimmed,
          })
          
          // Обновляем план в store
          appStore.updateWorkflowData({ testPlan: responseText })
          
          // Добавляем подсказку
          responseText += '\n\n---\n**План обновлён. Вы можете:**\n- Попросить ещё правки\n- Написать "готово" для генерации кода'
        }
      }
      
    } else if (currentStep === 'complete') {
      // Шаг 3: Работа завершена - можно только начать новый чат
      responseText = '✅ Работа по текущему проекту завершена.\n\nСоздайте новый чат для другого проекта или используйте команды:\n- `/review <код>` - проверить код\n- `/optimize` - оптимизировать тесты'
      
      // Разрешаем команды ревью и оптимизации даже после завершения
      if (trimmed.startsWith('/review')) {
        const detail = trimmed.replace('/review', '').trim()
        const code = detail || appStore.workflowData.code || 'print("Hello")'
        responseText = await reviewCode({
          code_snippet: code,
          rules: 'Стандарты TestOps',
        })
      } else if (trimmed.startsWith('/optimize')) {
        const detail = trimmed.replace('/optimize', '').trim()
        const cases = appStore.workflowData.testPlan || detail
        responseText = await optimizeTests({
          modules: detail || 'Общие модули',
          test_cases: cases,
        })
      }
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
  // Show mode selection dialog instead of creating a general chat
  appStore.setShowModeDialog(true)
}

const handleModeSelected = (mode: 'ui' | 'api') => {
  appStore.createNewChat(mode)
}

const handleClearAllChats = () => {
  const chats = [...appStore.chatHistories]
  chats.forEach(chat => {
    appStore.removeChatHistory(chat.id)
  })
  // Show mode dialog after clearing all
  appStore.setShowModeDialog(true)
}
</script>

<template>
  <ModeSelectionDialog
    v-model="showModeDialog"
    @mode-selected="handleModeSelected"
  />
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
