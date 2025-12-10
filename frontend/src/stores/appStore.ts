import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// UUID v4 generator fallback for browsers without crypto.randomUUID
function generateUUID(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  // Fallback: simple UUID v4 implementation
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

// Workflow steps: 1=ping, 2=generate-ui, 3=generate-api, 4=redact, 5=generate-code, 6=optimize, 7=review
export type WorkflowStep = 'idle' | 'generate-ui' | 'generate-api' | 'redact' | 'generate-code' | 'optimize' | 'review' | 'complete'

interface ChatHistory {
  id: string
  title: string
  type?: 'ui' | 'api' | 'general'
  messages: Message[]
  createdAt: number
  updatedAt: number
  workflowStep?: WorkflowStep
  workflowData?: {
    testPlan?: string
    code?: string
    lastStep?: WorkflowStep
  }
}

export const useAppStore = defineStore('app', () => {
  const messages = ref<Message[]>([])
  const chatHistories = ref<ChatHistory[]>([])
  const currentChatId = ref<string | null>(null)
  const currentChatType = ref<'ui' | 'api' | 'general' | null>(null)
  const isLoading = ref(false)
  const theme = ref<'light' | 'dark'>('light')
  const showModeDialog = ref(false)
  const currentWorkflowStep = ref<WorkflowStep>('idle')

  const initializeTheme = () => {
    const stored = localStorage.getItem('testops-theme')
    if (stored === 'dark' || stored === 'light') {
      theme.value = stored
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      theme.value = 'dark'
    }
    applyTheme()
  }

  const initializeChatHistory = () => {
    const stored = localStorage.getItem('testops-chat-history')
    if (stored) {
      try {
        const parsed = JSON.parse(stored)
        if (Array.isArray(parsed)) {
          chatHistories.value = parsed
          if (chatHistories.value.length > 0) {
            currentChatId.value = chatHistories.value[0].id
            currentChatType.value = chatHistories.value[0].type || 'general'
            messages.value = [...(chatHistories.value[0].messages || [])]
          }
        }
      } catch (e) {
        console.error('Failed to parse chat history:', e)
      }
    }

    // Если истории нет, создаём чат без приветствия для выбора типа
    if (chatHistories.value.length === 0) {
      createNewChat('general')
    }
  }

  const applyTheme = () => {
    if (theme.value === 'dark') document.documentElement.classList.add('dark')
    else document.documentElement.classList.remove('dark')
    localStorage.setItem('testops-theme', theme.value)
  }

  const currentChat = computed(() => {
    if (!currentChatId.value) return null
    return chatHistories.value.find(chat => chat.id === currentChatId.value) || null
  })

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    document.documentElement.classList.add('disable-transitions')
    setTimeout(() => {
      applyTheme()
      setTimeout(() => document.documentElement.classList.remove('disable-transitions'), 50)
    }, 50)
  }

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      id: generateUUID(),
      timestamp: Date.now(),
      ...message,
    }
    
    messages.value = [...messages.value, newMessage]
    
    if (currentChatId.value) {
      const chat = chatHistories.value.find(c => c.id === currentChatId.value)
      if (chat) {
        chat.messages = [...messages.value]
        chat.updatedAt = Date.now()
        saveChatHistory()
      }
    }
  }

  const clearMessages = () => { 
    messages.value = [] 
  }

  const createNewChat = (type: 'ui' | 'api' | 'general' = 'general') => {
    const chatId = generateUUID()
    const typeNames = { ui: 'UI Тестирование', api: 'API Тестирование', general: 'Общий чат' }
    const newChat: ChatHistory = {
      id: chatId,
      title: typeNames[type],
      type,
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
      workflowStep: 'idle',  // Всегда начинаем с idle
      workflowData: {}
    }
    chatHistories.value = [newChat, ...chatHistories.value]
    currentChatId.value = chatId
    currentChatType.value = type
    currentWorkflowStep.value = 'idle'  // Сброс workflow
    messages.value = []
    saveChatHistory()
    return chatId
  }

  const addChatHistory = (chat: ChatHistory) => { chatHistories.value.unshift(chat); saveChatHistory() }

  const removeChatHistory = (chatId: string) => {
    chatHistories.value = chatHistories.value.filter(c => c.id !== chatId)
    if (currentChatId.value === chatId) {
      currentChatId.value = chatHistories.value.length > 0 ? chatHistories.value[0].id : null
      if (currentChatId.value) {
        const chat = chatHistories.value.find(c => c.id === currentChatId.value)
        currentChatType.value = chat?.type || 'general'
        messages.value = chat?.messages || []
      } else {
        currentChatType.value = null
        messages.value = []
      }
    }
    saveChatHistory()
  }

  const setCurrentChatId = (chatId: string | null) => {
    currentChatId.value = chatId
    if (chatId) {
      const chat = chatHistories.value.find(c => c.id === chatId)
      if (chat) {
        currentChatType.value = chat.type || 'general'
        currentWorkflowStep.value = chat.workflowStep || 'idle'
        messages.value = [...chat.messages]
      }
    } else {
      currentChatType.value = null
      currentWorkflowStep.value = 'idle'
      messages.value = []
    }
  }

  const setWorkflowStep = (step: WorkflowStep) => {
    currentWorkflowStep.value = step
    if (currentChatId.value) {
      const chat = chatHistories.value.find(c => c.id === currentChatId.value)
      if (chat) {
        chat.workflowStep = step
        saveChatHistory()
      }
    }
  }

  const updateWorkflowData = (data: Partial<ChatHistory['workflowData']>) => {
    if (currentChatId.value) {
      const chat = chatHistories.value.find(c => c.id === currentChatId.value)
      if (chat) {
        chat.workflowData = { ...chat.workflowData, ...data }
        saveChatHistory()
      }
    }
  }

  const setShowModeDialog = (show: boolean) => {
    showModeDialog.value = show
  }

  const setIsLoading = (loading: boolean) => { isLoading.value = loading }

  const saveChatHistory = () => { localStorage.setItem('testops-chat-history', JSON.stringify(chatHistories.value)) }

  return {
    messages,
    chatHistories,
    currentChatId,
    currentChatType,
    isLoading,
    theme,
    currentChat,
    showModeDialog,
    currentWorkflowStep,
    workflowData: computed(() => currentChat.value?.workflowData || {}),
    initializeTheme,
    initializeChatHistory,
    toggleTheme,
    addMessage,
    clearMessages,
    createNewChat,
    addChatHistory,
    removeChatHistory,
    setCurrentChatId,
    setIsLoading,
    saveChatHistory,
    setWorkflowStep,
    updateWorkflowData,
    setShowModeDialog,
  }
})
