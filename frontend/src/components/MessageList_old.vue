<template>
  <div class="messageList">
    <div v-if="messages.length === 0 && !isLoading" class="emptyState">
      <div class="emptyIcon">💬</div>
      <h3 class="emptyTitle">{{ i18n.noMessagesYet }}</h3>
      <p class="emptyDescription">
        {{ i18n.startConversation }}
      </p>
    </div>

    <template v-else>
      <MessageItem
        v-for="message in messages"
        :key="message.id"
        :message="message"
      />
    </template>

    <LoadingIndicator v-if="isLoading" />
    
    <div ref="endRef"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUpdated, nextTick, onMounted } from 'vue'
import { useAppStore } from '../stores/appStore'
import { i18n } from '../utils/i18n'
import MessageItem from './MessageItem.vue'
import LoadingIndicator from './LoadingIndicator.vue'

const appStore = useAppStore()
const endRef = ref<HTMLDivElement | null>(null)

const messages = computed(() => appStore.messages)
const isLoading = computed(() => appStore.isLoading)

const scrollToBottom = () => {
  if (endRef.value) {
    endRef.value.scrollIntoView({ behavior: 'smooth' })
  }
}

onUpdated(() => {
  scrollToBottom()
})

// Initial scroll to bottom
onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* Message List Container */
.messageList {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
  padding: 2rem 1.75rem;
  gap: 1rem;
  transition: background-color var(--transition-base);
}

/* Empty State Container */
.emptyState {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  gap: 1.25rem;
}

/* Empty State Icon */
.emptyIcon {
  font-size: 3.5rem;
  color: var(--color-text-tertiary);
  opacity: 0.6;
}

/* Empty State Title */
.emptyTitle {
  font-size: 1.375rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.6;
}

/* Empty State Description */
.emptyDescription {
  color: var(--color-text-secondary);
  max-width: 340px;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
  opacity: 0.85;
}

/* Custom Scrollbar Styling */
.messageList::-webkit-scrollbar {
  width: 8px;
}

.messageList::-webkit-scrollbar-track {
  background: transparent;
}

.messageList::-webkit-scrollbar-thumb {
  background: var(--color-gray-300);
  border-radius: 4px;
  transition: background-color var(--transition-base);
}

.messageList::-webkit-scrollbar-thumb:hover {
  background: var(--color-gray-400);
}

.dark .messageList::-webkit-scrollbar-thumb {
  background: var(--color-gray-600);
}

.dark .messageList::-webkit-scrollbar-thumb:hover {
  background: var(--color-gray-500);
}

/* Firefox Scrollbar */
.messageList {
  scrollbar-color: var(--color-gray-300) transparent;
  scrollbar-width: thin;
}

.dark .messageList {
  scrollbar-color: var(--color-gray-600) transparent;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .messageList {
    padding: 1.75rem 1.5rem;
  }

  .emptyIcon {
    font-size: 3rem;
  }

  .emptyTitle {
    font-size: 1.25rem;
  }

  .emptyDescription {
    font-size: 0.9125rem;
    max-width: 320px;
  }
}

@media (max-width: 768px) {
  .messageList {
    padding: 1.5rem 1rem;
    gap: 0.875rem;
  }

  .emptyIcon {
    font-size: 2.5rem;
  }

  .emptyTitle {
    font-size: 1.125rem;
  }

  .emptyDescription {
    font-size: 0.875rem;
    max-width: 280px;
  }
}
</style>
