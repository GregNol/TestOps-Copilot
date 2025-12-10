<template>
  <div class="chat-area column no-wrap q-pa-none">
    <div v-if="workflowIndicatorText" class="workflow-indicator">
      <q-icon name="info" size="18px" />
      <span>{{ workflowIndicatorText }}</span>
    </div>
    <div class="messages-scroll" ref="scrollAreaRef">
      <MessageList :messages="messages" :is-loading="isLoading" />
    </div>
    <div v-if="hasChatActive" class="input-wrapper">
      <PromptInput :is-loading="isLoading" @send-message="$emit('sendMessage', $event)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import MessageList from './MessageList.vue'
import PromptInput from './PromptInput.vue'
import { useAppStore } from '../stores/appStore'

interface ChatAreaProps {
  messages: any[]
  isLoading: boolean
}

const props = defineProps<ChatAreaProps>()
const appStore = useAppStore()

const hasChatActive = computed(() => {
  return appStore.currentChatId !== null && appStore.currentChatType !== null
})

const workflowIndicatorText = computed(() => {
  const step = appStore.currentWorkflowStep
  const chatType = appStore.currentChatType
  
  if (!chatType || chatType === 'general') return ''
  
  const indicators = {
    'idle': '🎯 Шаг 1: Опишите проект для генерации тест-плана',
    'generate-ui': '📝 Шаг 2: Редактируйте план или напишите "готово" для генерации кода',
    'generate-api': '📝 Шаг 2: Редактируйте план или напишите "готово" для генерации кода',
    'generate-code': '⚙️ Генерация кода...',
    'complete': '✅ Работа завершена! Можете создать новый чат',
    'optimize': '🔧 Оптимизация тестов',
    'review': '👀 Проверка кода',
    'redact': '✏️ Редактирование контента'
  }
  
  return indicators[step] || ''
})

defineEmits<{
  (e: 'sendMessage', payload: { text: string; file: File | null }): void
}>()

const scrollAreaRef = ref<HTMLElement | null>(null)
</script>

<style scoped>

.chat-area {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  background-color: var(--color-background);
  overflow: hidden;
}

.workflow-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dark .workflow-indicator {
  background: linear-gradient(135deg, #4c5fd7 0%, #5a3a7a 100%);
}

.messages-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1rem 0.5rem;
}

.input-wrapper {
  flex-shrink: 0;
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
}

@media (max-width: 768px) {
  .input-wrapper {
    border-top: 1px solid var(--color-border);
  }
}
</style>
