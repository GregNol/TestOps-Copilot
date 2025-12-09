<template>
  <form class="promptInput" @submit.prevent="handleSubmit">
    <div class="inputContainer">
      <!-- Attach Button -->
      <label class="attachButton" title="Прикрепить файл">
        <input
          type="file"
          style="display: none"
          @change="handleFileChange"
          :disabled="isLoading"
        />
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21.44 11.05l-8.49 8.49a5 5 0 01-7.07 0 5 5 0 010-7.07l9.19-9.19a3.5 3.5 0 015 5l-8.49 8.49a2 2 0 11-2.83-2.83l7.78-7.78" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </label>
      
      <textarea
        ref="textareaRef"
        class="textarea"
        placeholder="Введите UI-требования, OpenAPI спецификацию или другой запрос..."
        v-model="text"
        @keydown="handleKeyDown"
        @input="adjustTextareaHeight"
        :disabled="isLoading"
        rows="3"
      />
      
      <button
        class="submitButton"
        type="submit"
        :disabled="(!text.trim() && !file) || isLoading"
        aria-label="Отправить"
        title="Отправить"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2 10L18 2L10 18L8.5 11L2 10Z"
            fill="currentColor"
          />
        </svg>
      </button>
    </div>
    
    <div v-if="file" class="fileInfo">{{ file.name }}</div>
    <p class="hint">Нажмите Enter для отправки</p>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useAppStore } from '../stores/appStore'

const appStore = useAppStore()
const text = ref('')
const file = ref<File | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

const isLoading = computed(() => appStore.isLoading)

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    file.value = target.files[0]
  }
}

const adjustTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = `${Math.min(textareaRef.value.scrollHeight, 250)}px`
  }
}

const handleSubmit = () => {
  if ((text.value.trim() || file.value) && !isLoading.value) {
    // Emit the message to parent
    emit('sendMessage', text.value.trim())
    
    // Clear the input
    text.value = ''
    file.value = null
    
    // Reset textarea height
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  }
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit()
  }
}

// Auto-resize textarea when text changes
const handleTextChange = () => {
  nextTick(() => {
    adjustTextareaHeight()
  })
}

// Watch for text changes
watch(text, handleTextChange)

// Define emits
const emit = defineEmits<{
  (e: 'sendMessage', text: string): void
}>()
</script>

<style scoped>
/* Prompt Input Container */
.promptInput {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem;
  border-top: 1px solid var(--color-border);
  background-color: var(--color-surface);
  transition: border-color var(--transition-base);
}

/* Input Container */
.inputContainer {
  display: flex;
  gap: 0.875rem;
  align-items: flex-end;
}

/* Attach Button */
.attachButton {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 6px;
  background-color: var(--color-surface-alt);
  color: var(--color-primary);
  cursor: pointer;
  margin-right: 0.5rem;
  transition: background-color var(--transition-base), color var(--transition-base);
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}

.attachButton:hover:not(:disabled) {
  background-color: var(--color-primary-light);
  color: var(--color-primary-hover);
}

.attachButton:active:not(:disabled) {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
}

/* Textarea Styling */
.textarea {
  flex: 1;
  padding: 0.875rem 1.125rem;
  font-size: 0.95rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background-color: var(--color-surface-alt);
  color: var(--color-text-primary);
  resize: none;
  min-height: 44px;
  max-height: 200px;
  transition: border-color var(--transition-base), 
              background-color var(--transition-base),
              box-shadow var(--transition-base);
  line-height: 1.6;
  font-weight: 400;
  overflow-y: auto;
}

/* Textarea Focus State */
.textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-surface);
  box-shadow: 0 0 0 3px rgba(0, 185, 86, 0.1);
}

.dark .textarea:focus {
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.15);
}

/* Textarea Disabled State */
.textarea:disabled {
  background-color: var(--color-surface-alt);
  color: var(--color-text-tertiary);
  cursor: not-allowed;
  opacity: 0.7;
}

/* Textarea Placeholder */
.textarea::placeholder {
  color: var(--color-text-tertiary);
  opacity: 0.8;
}

/* Submit Button */
.submitButton {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 6px;
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
  cursor: pointer;
  transition: background-color var(--transition-base), box-shadow var(--transition-base), transform var(--transition-base), opacity var(--transition-base);
  flex-shrink: 0;
  border: none;
  font-weight: 500;
}

/* Submit Button Hover */
.submitButton:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  box-shadow: 0 2px 8px rgba(0, 185, 86, 0.2);
}

.dark .submitButton:hover:not(:disabled) {
  box-shadow: 0 2px 8px rgba(0, 200, 83, 0.25);
}

/* Submit Button Active */
.submitButton:active:not(:disabled) {
  transform: scale(0.98);
}

/* Submit Button Disabled */
.submitButton:disabled {
  background-color: var(--color-gray-300);
  color: var(--color-text-secondary);
  cursor: not-allowed;
  opacity: 0.6;
}

.dark .submitButton:disabled {
  background-color: var(--color-gray-600);
  color: var(--color-text-tertiary);
}

/* File Info */
.fileInfo {
  font-size: 0.85rem;
  color: var(--color-primary);
  margin-top: 0.25rem;
  margin-left: 0.5rem;
  word-break: break-all;
}

/* Hint Text */
.hint {
  font-size: 0.8125rem;
  color: var(--color-text-tertiary);
  margin: 0;
  padding-left: 0.5rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .promptInput {
    padding: 1rem 1.125rem;
    gap: 0.625rem;
  }

  .inputContainer {
    gap: 0.75rem;
  }

  .textarea {
    padding: 0.75rem 1rem;
  }
}

@media (max-width: 768px) {
  .promptInput {
    padding: 0.875rem 1rem;
  }

  .attachButton {
    width: 40px;
    height: 40px;
  }

  .submitButton {
    width: 40px;
    height: 40px;
  }

  .textarea {
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
  }

  .hint {
    font-size: 0.75rem;
  }
}
</style>
