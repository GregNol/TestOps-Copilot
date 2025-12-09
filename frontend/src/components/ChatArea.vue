<template>
  <div class="chat-area column no-wrap q-pa-none">
    <div class="messages-scroll" ref="scrollAreaRef">
      <MessageList :messages="messages" :is-loading="isLoading" />
    </div>
    <div class="input-wrapper">
      <PromptInput :is-loading="isLoading" @send-message="$emit('sendMessage', $event)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MessageList from './MessageList.vue'
import PromptInput from './PromptInput.vue'

interface ChatAreaProps {
  messages: any[]
  isLoading: boolean
}

const props = defineProps<ChatAreaProps>()

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
  border-radius: 16px;
  margin: 1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.messages-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1.5rem 1rem;
}

.input-wrapper {
  flex-shrink: 0;
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  border-radius: 0 0 16px 16px;
}

@media (max-width: 768px) {
  .input-wrapper {
    border-top: 1px solid var(--color-border);
  }
}
</style>