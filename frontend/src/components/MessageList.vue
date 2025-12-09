<template>
  <div class="message-list">
    <!-- Empty state with choice buttons -->
    <div v-if="messages.length === 0 && !isLoading" class="empty-state q-pa-md">
      <div class="welcome-section">
        <q-icon name="smart_toy" size="64px" color="primary" />
        <div class="text-h5 q-mt-md text-weight-bold">TestOps Copilot</div>
        <div class="text-body1 text-grey-7 q-mt-sm">Выберите тип тестирования</div>
      </div>

      <div class="buttons-container q-mt-lg">
        <q-card class="choice-card" @click="handleChooseUI">
          <q-card-section>
            <div class="card-icon">
              <q-icon name="design_services" size="48px" color="primary" />
            </div>
            <div class="card-title">Тестировать UI</div>
            <div class="card-description">Генерируйте тест-кейсы для веб-интерфейсов</div>
          </q-card-section>
        </q-card>

        <q-card class="choice-card" @click="handleChooseAPI">
          <q-card-section>
            <div class="card-icon">
              <q-icon name="api" size="48px" color="positive" />
            </div>
            <div class="card-title">Тестировать API</div>
            <div class="card-description">Генерируйте тест-кейсы для REST API</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
    
    <!-- Messages when chat has content -->
    <div v-else class="messages-wrapper q-pa-md">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-item"
      >
        <MessageItem :message="msg" />
      </div>

      <!-- Loading indicator -->
      <div v-if="isLoading" class="message-item">
        <div class="loading-message">
          <q-spinner-dots size="1.5rem" color="primary" />
          <span class="q-ml-md">Генерирую результаты...</span>
        </div>
      </div>

      <!-- Scroll anchor -->
      <div ref="messagesEndRef" style="height: 1px;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { QSpinnerDots, QIcon, QCard, QCardSection } from 'quasar'
import { ref, watch, nextTick } from 'vue'
import MessageItem from './MessageItem.vue'
import { useAppStore } from '../stores/appStore'
import type { Message } from '../stores/appStore'

interface MessageListProps {
  messages: Message[]
  isLoading?: boolean
}

const props = defineProps<MessageListProps>()
const appStore = useAppStore()

const messagesEndRef = ref<HTMLElement | null>(null)

const handleChooseUI = () => {
  appStore.createNewChat('ui')
  appStore.addMessage({
    role: 'assistant',
    content: 'Отлично! Я помогу вам генерировать тесты для UI. Опишите страницу или компонент, который нужно протестировать.',
  })
}

const handleChooseAPI = () => {
  appStore.createNewChat('api')
  appStore.addMessage({
    role: 'assistant',
    content: 'Отлично! Я помогу вам генерировать тесты для API. Загрузите OpenAPI/Swagger спецификацию или опишите API endpoints.',
  })
}

const scrollToEnd = async () => {
  await nextTick()
  messagesEndRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Auto-scroll when messages change
watch(
  () => props.messages.length,
  async () => {
    await scrollToEnd()
  }
)

// Auto-scroll when loading state changes
watch(
  () => props.isLoading,
  async () => {
    await scrollToEnd()
  }
)
</script>

<style scoped>
.message-list {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.welcome-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.buttons-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
}

.choice-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  border-radius: 12px;
}

.choice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 185, 86, 0.2);
  border-color: var(--color-primary);
}

.dark .choice-card {
  background: var(--color-surface-alt);
  border-color: var(--color-border);
}

.dark .choice-card:hover {
  box-shadow: 0 8px 24px rgba(0, 200, 83, 0.25);
  border-color: var(--color-primary);
}

.card-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.card-description {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.messages-wrapper {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-item {
  display: flex;
  width: 100%;
}

.loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: var(--color-surface-alt);
  border-radius: 12px;
  width: 100%;
  font-size: 15px;
  color: var(--color-text-secondary);
}

@media (max-width: 768px) {
  .buttons-container {
    grid-template-columns: 1fr;
    gap: 1rem;
    max-width: 100%;
  }

  .card-title {
    font-size: 16px;
  }

  .card-description {
    font-size: 13px;
  }
}
</style>
