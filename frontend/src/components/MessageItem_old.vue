<template>
  <div :class="['message', isUser ? 'userMessage' : 'assistantMessage']">
    <div class="content">
      <div v-if="isUser" class="textContent">{{ message.content }}</div>
      <div v-else class="markdownContent" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import type { Message } from '../stores/appStore'
import { renderMarkdown } from '../utils/markdown'

interface Props {
  message: Message
}

const props = defineProps<Props>()

const isUser = computed(() => props.message.role === 'user')
const renderedContent = ref<string>('')

const renderContent = async () => {
  if (!isUser.value && props.message.content) {
    try {
      renderedContent.value = await renderMarkdown(props.message.content)
    } catch (error) {
      console.error('Error rendering markdown:', error)
      renderedContent.value = props.message.content
    }
  } else {
    renderedContent.value = props.message.content
  }
}

// Watch for content changes
watch(() => props.message.content, renderContent, { immediate: true })

// Initial render
onMounted(() => {
  renderContent()
})
</script>

<style scoped>
.message {
  display: flex;
  width: 100%;
  margin-bottom: 1.5rem;
  animation: fadeIn 0.3s ease;
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

.userMessage {
  justify-content: flex-end;
}

.assistantMessage {
  justify-content: flex-start;
}

.content {
  max-width: 85%;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  word-wrap: break-word;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: background-color var(--transition-base);
  line-height: 1.6;
}

.userMessage .content {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
  margin-left: auto;
  margin-right: 0;
}

.assistantMessage .content {
  background-color: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  margin-right: auto;
  margin-left: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.textContent {
  white-space: pre-wrap;
  word-break: break-word;
}

.markdownContent {
  line-height: 1.6;
}

.markdownContent :deep(p) {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.6;
  color: inherit;
}

.markdownContent :deep(p + p) {
  margin-top: 0.75rem;
}

.markdownContent :deep(ul),
.markdownContent :deep(ol) {
  margin: 0.75rem 0 0 1.5rem;
  padding: 0;
}

.markdownContent :deep(li) {
  margin-bottom: 0.5rem;
  color: inherit;
}

.markdownContent :deep(blockquote) {
  border-left: 3px solid var(--color-primary);
  padding-left: 1rem;
  margin: 0.75rem 0;
  color: var(--color-text-secondary);
  font-style: italic;
  opacity: 0.9;
}

.markdownContent :deep(h1),
.markdownContent :deep(h2),
.markdownContent :deep(h3),
.markdownContent :deep(h4),
.markdownContent :deep(h5),
.markdownContent :deep(h6) {
  margin: 1rem 0 0.5rem 0;
  font-weight: 700;
  color: inherit;
}

.markdownContent :deep(h1) {
  font-size: 1.5rem;
  line-height: 1.8;
  margin-top: 1.5rem;
}

.markdownContent :deep(h2) {
  font-size: 1.25rem;
  line-height: 1.7;
  margin-top: 1.25rem;
}

.markdownContent :deep(h3) {
  font-size: 1.125rem;
  line-height: 1.6;
  margin-top: 1rem;
}

.markdownContent :deep(h4),
.markdownContent :deep(h5),
.markdownContent :deep(h6) {
  font-size: 1rem;
  margin-top: 0.75rem;
}

.markdownContent :deep(pre) {
  background-color: var(--color-code-background);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  margin: 0.75rem 0;
}

.markdownContent :deep(pre code) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Courier New', monospace;
  font-size: 0.875rem;
  color: var(--color-code-text);
  line-height: 1.5;
  display: block;
  white-space: pre;
}

.userMessage .markdownContent :deep(pre) {
  background-color: rgba(0, 0, 0, 0.2);
  border-color: rgba(0, 0, 0, 0.3);
}

.userMessage .markdownContent :deep(pre code) {
  color: rgba(255, 255, 255, 0.9);
}

.markdownContent :deep(code) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Courier New', monospace;
  font-size: 0.9em;
  background-color: var(--color-code-background);
  color: var(--color-code-text);
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

.userMessage .markdownContent :deep(code) {
  background-color: rgba(0, 0, 0, 0.2);
  color: rgba(255, 255, 255, 0.95);
}

.markdownContent :deep(a) {
  color: inherit;
  text-decoration: underline;
  opacity: 0.8;
}

.markdownContent :deep(a:hover) {
  opacity: 1;
}

.userMessage .markdownContent :deep(a) {
  color: inherit;
  text-decoration-color: rgba(255, 255, 255, 0.6);
}

.markdownContent :deep(hr) {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 1rem 0;
}

.userMessage .markdownContent :deep(hr) {
  border-top-color: rgba(0, 0, 0, 0.2);
}

.markdownContent :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.markdownContent :deep(th) {
  background-color: var(--color-surface-alt);
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  text-align: left;
  font-weight: 600;
}

.markdownContent :deep(td) {
  padding: 0.75rem;
  border: 1px solid var(--color-border);
}

.userMessage .markdownContent :deep(th) {
  background-color: rgba(0, 0, 0, 0.2);
  border-color: rgba(0, 0, 0, 0.3);
}

.userMessage .markdownContent :deep(td) {
  border-color: rgba(0, 0, 0, 0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
  .message {
    margin-bottom: 1rem;
  }

  .content {
    max-width: 95%;
    padding: 0.875rem 1rem;
    border-radius: 6px;
    font-size: 0.9375rem;
  }

  .markdownContent :deep(h1) {
    font-size: 1.25rem;
  }

  .markdownContent :deep(h2) {
    font-size: 1.125rem;
  }

  .markdownContent :deep(h3) {
    font-size: 1rem;
  }

  .markdownContent :deep(pre) {
    padding: 0.75rem;
    font-size: 0.8125rem;
  }

  .markdownContent :deep(table) {
    font-size: 0.8rem;
  }

  .markdownContent :deep(th),
  .markdownContent :deep(td) {
    padding: 0.5rem;
  }
}
</style>
