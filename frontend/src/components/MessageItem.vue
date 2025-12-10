<template>
  <div :class="['message', isUser ? 'user-message' : 'assistant-message']">
    <div class="message-header">
      <span class="message-author">{{ isUser ? 'Вы' : 'TestOps Bot' }}</span>
      <span class="message-time">{{ formatTime(message.timestamp) }}</span>
    </div>
    <div class="content">
      <div v-if="isUser" class="text-content" v-text="message.content"></div>
      <div v-else class="markdown-content" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import { renderMarkdown } from '../utils/markdown'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

interface Props {
  message: Message
}

const props = defineProps<Props>()

const isUser = computed(() => props.message.role === 'user')
const renderedContent = ref<string>('')

const formatTime = (timestamp: number): string => {
  const date = new Date(timestamp)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

watch(
  () => props.message,
  async (newMessage) => {
    if (!newMessage) return

    if (newMessage.role === 'assistant') {
      try {
        renderedContent.value = await renderMarkdown(newMessage.content)
      } catch (error) {
        console.error('Failed to render markdown:', error)
        renderedContent.value = newMessage.content
      }
    }
  },
  { immediate: true }
)
</script>

<style scoped>
/* Message Container */
.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  animation: fadeIn 0.3s ease;
  gap: 0.375rem;
  width: 100%;
}

.user-message {
  align-items: flex-end;
  gap: 0.375rem;
}

.assistant-message {
  align-items: flex-start;
  gap: 0.375rem;
}

.message-header {
  display: flex;
  align-items: center;
  padding: 0 1rem;
  font-size: 0.75rem;
  gap: 0.5rem;
  width: 100%;
  box-sizing: border-box;
}

.user-message .message-header {
  justify-content: flex-end;
}

.assistant-message .message-header {
  justify-content: flex-start;
}

.message-author {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.message-time {
  font-size: 0.7rem;
  color: var(--color-text-tertiary);
  margin-left: 0.5rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Message Content Box */
.content {
  max-width: 90%;
  padding: 1rem 1.25rem;
  border-radius: 16px;
  word-wrap: break-word;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  line-height: 1.6;
  font-size: 15px;
  font-weight: 400;
}

/* User Message Styling */
.user-message .content {
  background-color: #f5f5f5;
  color: #1f2937;
  border: 1.5px solid var(--color-primary);
  border-radius: 20px 20px 4px 20px;
  box-shadow: 0 2px 10px rgba(0, 185, 86, 0.12);
}

.dark .user-message .content {
  background-color: #2d3748;
  color: #e4e8f0;
  border: 1.5px solid var(--color-primary);
  box-shadow: 0 2px 8px rgba(0, 200, 83, 0.2);
}

/* Assistant Message Styling */
.assistant-message .content {
  background-color: #f5f5f5;
  color: #1f2937;
  border: 1.5px solid var(--color-primary);
  border-radius: 20px 20px 20px 4px;
  box-shadow: 0 2px 10px rgba(0, 185, 86, 0.12);
}

.dark .assistant-message .content {
  background-color: #2d3748;
  color: #e4e8f0;
  border: 1.5px solid var(--color-primary);
  box-shadow: 0 2px 8px rgba(0, 200, 83, 0.2);
}

/* Text Content */
.text-content {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Markdown Content Styling */
.markdown-content :deep(p) {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.6;
  color: inherit;
}

.markdown-content :deep(p + p) {
  margin-top: 0.75rem;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 0.75rem 0 0 1.5rem;
  padding: 0;
  color: inherit;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5rem;
  color: inherit;
  font-size: 0.95rem;
  line-height: 1.6;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid var(--color-primary);
  padding-left: 1rem;
  margin: 0.75rem 0;
  color: inherit;
  font-style: italic;
  opacity: 0.85;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin: 1rem 0 0.5rem 0;
  font-weight: 700;
  color: inherit;
}

.markdown-content :deep(h1) {
  font-size: 1.5rem;
  line-height: 1.8;
  margin-top: 1.5rem;
}

.markdown-content :deep(h2) {
  font-size: 1.25rem;
  line-height: 1.7;
  margin-top: 1.25rem;
}

.markdown-content :deep(h3) {
  font-size: 1.125rem;
  line-height: 1.6;
  margin-top: 1rem;
}

.markdown-content :deep(pre) {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  margin: 0.75rem 0;
}

.dark .markdown-content :deep(pre) {
  background-color: #1e2632;
  border: 1px solid #354151;
}

.markdown-content :deep(code) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}

.markdown-content :deep(code:not(pre code)) {
  background-color: #f0f0f0;
  color: #374151;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

.dark .markdown-content :deep(code:not(pre code)) {
  background-color: #3f4a57;
  color: #e4e8f0;
}

.markdown-content :deep(a) {
  color: inherit;
  text-decoration: underline;
  opacity: 0.8;
  font-weight: 500;
}

.markdown-content :deep(a:hover) {
  opacity: 1;
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1rem 0;
  opacity: 0.5;
}

.dark .markdown-content :deep(hr) {
  border-top-color: #354151;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 0.75rem 0;
  border: 1px solid #ddd;
}

.dark .markdown-content :deep(table) {
  border-color: #354151;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid #ddd;
  padding: 0.5rem 0.75rem;
  text-align: left;
}

.dark .markdown-content :deep(th),
.dark .markdown-content :deep(td) {
  border-color: #354151;
}

.markdown-content :deep(th) {
  background-color: #f5f5f5;
  font-weight: 600;
}

.dark .markdown-content :deep(th) {
  background-color: #3f4a57;
}

@media (max-width: 768px) {
  .content {
    max-width: 95%;
  }
}
</style>
