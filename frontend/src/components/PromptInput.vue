<template>
  <q-form class="prompt-input" @submit.prevent="handleSubmit">
    <!-- JSON/YAML Input Mode Toggle -->
    <div v-if="showJsonInput" class="json-input-section">
      <div class="json-header">
        <span class="json-label">
          <q-icon name="code" size="18px" />
          JSON/YAML спецификация
        </span>
        <q-btn
          flat
          dense
          round
          icon="close"
          size="sm"
          @click="closeJsonInput"
          class="close-json-btn"
        />
      </div>
      <q-input
        v-model="jsonContent"
        type="textarea"
        autogrow
        borderless
        dense
        placeholder='Вставьте JSON или YAML спецификацию здесь...'
        class="json-textarea"
        :input-style="{ 
          minHeight: '120px', 
          maxHeight: '300px',
          fontFamily: 'Monaco, Consolas, monospace',
          fontSize: '0.875rem'
        }"
      />
    </div>

    <div class="input-container">
      <div class="action-buttons">
        <q-btn
          flat
          round
          color="primary"
          icon="attach_file"
          class="action-button"
          :disable="isLoading"
          aria-label="Прикрепить файл"
          @click="triggerFile"
        />
        <q-btn
          flat
          round
          color="primary"
          icon="code"
          class="action-button"
          :disable="isLoading"
          aria-label="Вставить JSON/YAML"
          @click="toggleJsonInput"
        />
      </div>

      <input
        ref="fileInputRef"
        type="file"
        class="file-hidden"
        @change="handleFileChange"
        :disabled="isLoading"
        accept=".json,.yaml,.yml"
      />

      <q-input
        ref="inputRef"
        v-model="text"
        type="textarea"
        autogrow
        borderless
        dense
        color="primary"
        :disable="isLoading"
        placeholder="Введите UI-требования или описание тестов..."
        class="textarea full-width"
        @keydown="handleKeyDown"
        :input-style="{ maxHeight: '220px', color: 'var(--color-text-primary)' }"
      />

      <q-btn
        unelevated
        color="primary"
        text-color="white"
        icon="send"
        class="submit-button"
        type="submit"
        :disable="(!text.trim() && !file && !jsonContent.trim()) || isLoading"
        aria-label="Отправить"
      />
    </div>

    <!-- File Info with Remove Button -->
    <div v-if="file" class="file-info-container">
      <div class="file-info">
        <q-icon name="attach_file" size="16px" />
        <span class="file-name">{{ file.name }}</span>
        <q-btn
          flat
          dense
          round
          icon="close"
          size="xs"
          @click="removeFile"
          class="remove-file-btn"
          aria-label="Открепить файл"
        />
      </div>
    </div>
    
    <p class="hint">
      <kbd>Enter</kbd> для отправки, <kbd>Shift+Enter</kbd> для новой строки
    </p>
  </q-form>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { QForm, QInput, QBtn, QIcon } from 'quasar'

interface PromptInputProps {
  isLoading: boolean
}

const props = defineProps<PromptInputProps>()

const emit = defineEmits<{
  (e: 'send-message', payload: { text: string; file: File | null }): void
}>()

const text = ref('')
const file = ref<File | null>(null)
const jsonContent = ref('')
const showJsonInput = ref(false)
const fileInputRef = ref<HTMLInputElement | null>(null)
const inputRef = ref<QInput | null>(null)

const triggerFile = () => {
  fileInputRef.value?.click()
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    file.value = target.files[0]
    // If it's a JSON/YAML file, optionally read and display
    const fileName = target.files[0].name.toLowerCase()
    if (fileName.endsWith('.json') || fileName.endsWith('.yaml') || fileName.endsWith('.yml')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        jsonContent.value = e.target?.result as string || ''
        showJsonInput.value = true
      }
      reader.readAsText(target.files[0])
    }
  }
}

const removeFile = () => {
  file.value = null
  if (fileInputRef.value) fileInputRef.value.value = ''
}

const toggleJsonInput = () => {
  showJsonInput.value = !showJsonInput.value
}

const closeJsonInput = () => {
  showJsonInput.value = false
  jsonContent.value = ''
}

const handleSubmit = async () => {
  // Combine text with JSON if present
  let messageText = text.value.trim()
  if (jsonContent.value.trim()) {
    messageText = messageText 
      ? `${messageText}\n\nСпецификация:\n${jsonContent.value}` 
      : jsonContent.value
  }

  if ((messageText || file.value) && !props.isLoading) {
    emit('send-message', { text: messageText, file: file.value })
    text.value = ''
    jsonContent.value = ''
    showJsonInput.value = false
    file.value = null
    if (fileInputRef.value) fileInputRef.value.value = ''
    inputRef.value?.resetValidation()
    
    // Возвращаем фокус в поле ввода
    await nextTick()
    inputRef.value?.focus()
  }
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit()
  }
}
</script>

<style scoped>
/* Prompt Input Container */
.prompt-input {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem;
  background-color: var(--color-surface);
  border-radius: 0 0 16px 16px;
  transition: border-color var(--transition-base);
}

/* JSON Input Section */
.json-input-section {
  background: var(--color-surface-alt);
  border: 2px dashed var(--color-border);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 0.5rem;
}

.json-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.json-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.close-json-btn {
  color: var(--color-text-tertiary);
}

.json-textarea :deep(.q-field__control) {
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  transition: all 0.2s ease;
}

.json-textarea :deep(.q-field__control:focus-within) {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 185, 86, 0.1);
}

.json-textarea :deep(textarea) {
  padding: 0.875rem;
  line-height: 1.5;
  font-family: 'JetBrains Mono', 'SF Mono', 'Monaco', 'Consolas', monospace !important;
  font-size: 0.85rem !important;
  letter-spacing: 0 !important;
  color: var(--color-text-primary) !important;
}

.json-textarea :deep(.q-field__control::before),
.json-textarea :deep(.q-field__control::after) {
  display: none !important;
}

/* Input Container */
.input-container {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.full-width {
  flex: 1;
  width: 100%;
}

.action-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--color-surface-alt);
  color: var(--color-primary);
  border: 1px solid var(--color-border);
  transition: all 0.2s ease;
}

.action-button:hover {
  background: var(--accent-light);
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 185, 86, 0.15);
}

.action-button:deep(.q-icon) {
  color: var(--color-primary);
}

.textarea :deep(textarea) {
  padding: 0.875rem 1rem;
  min-height: 44px;
  font-size: 0.95rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  color: var(--color-text-primary);
}

.textarea :deep(.q-field__control) {
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-surface-alt);
  min-height: 44px;
  transition: all 0.2s ease;
}

.textarea :deep(.q-field__control:hover) {
  border-color: var(--color-primary);
  background: var(--color-surface);
}

.textarea :deep(.q-field__control:focus-within) {
  border-color: var(--color-primary);
  background: var(--color-surface);
  box-shadow: 0 0 0 3px rgba(0, 185, 86, 0.1);
}

.textarea :deep(.q-field__native) {
  outline: none !important;
}

.textarea :deep(.q-field__control::before),
.textarea :deep(.q-field__control::after) {
  display: none !important;
}

.textarea :deep(textarea::placeholder) {
  color: var(--color-text-tertiary);
}

.submit-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--color-primary) !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(0, 185, 86, 0.2);
  transition: all 0.2s ease;
}

.submit-button:hover {
  background: var(--color-primary-hover) !important;
  box-shadow: 0 4px 12px rgba(0, 185, 86, 0.3);
  transform: translateY(-2px);
}

.submit-button:deep(.q-icon) {
  color: white !important;
}

.file-hidden {
  display: none;
}

/* File Info with Remove Button */
.file-info-container {
  display: flex;
  align-items: center;
}

.file-info {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-surface-alt);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  transition: all 0.2s ease;
}

.file-name {
  font-weight: 500;
  color: var(--color-text-primary);
}

.remove-file-btn {
  color: var(--color-text-tertiary);
  transition: all 0.2s ease;
}

.remove-file-btn:hover {
  color: var(--color-error);
  background: rgba(239, 68, 68, 0.1);
}

/* Hint */
.hint {
  font-size: 0.8125rem;
  color: var(--color-text-tertiary);
  margin: 0;
  text-align: center;
}

.hint kbd {
  display: inline-block;
  padding: 0.125rem 0.375rem;
  background: var(--color-surface-alt);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

@media (max-width: 768px) {
  .prompt-input {
    padding: 1rem;
    border-radius: 0;
  }

  .input-container {
    gap: 0.5rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }

  .action-button {
    width: 40px;
    height: 40px;
  }

  .textarea :deep(textarea) {
    font-size: 0.9rem;
    min-height: 40px;
  }

  .submit-button {
    width: 40px;
    height: 40px;
  }
}
</style>
