<template>
  <q-form class="prompt-input" @submit.prevent="handleSubmit">
    <div class="input-container">
      <q-btn
        flat
        round
        color="primary"
        icon="attach_file"
        class="attach-button"
        :disable="isLoading"
        aria-label="Прикрепить файл"
        @click="triggerFile"
      />

      <input
        ref="fileInputRef"
        type="file"
        class="file-hidden"
        @change="handleFileChange"
        :disabled="isLoading"
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
        placeholder="Введите UI-требования, OpenAPI спецификацию или другой запрос..."
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
        :disable="(!text.trim() && !file) || isLoading"
        aria-label="Отправить"
      />
    </div>

    <div v-if="file" class="file-info">
      <q-icon name="attach_file" size="16px" />
      <span>{{ file.name }}</span>
    </div>
    <p class="hint">Нажмите Enter для отправки</p>
  </q-form>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
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
const fileInputRef = ref<HTMLInputElement | null>(null)
const inputRef = ref<QInput | null>(null)

const triggerFile = () => {
  fileInputRef.value?.click()
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    file.value = target.files[0]
  }
}

const handleSubmit = async () => {
  if ((text.value.trim() || file.value) && !props.isLoading) {
    emit('send-message', { text: text.value.trim(), file: file.value })
    text.value = ''
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
  transition: border-color var(--transition-base);
}

.input-container {
  display: flex;
  gap: 0.875rem;
  align-items: flex-end;
}

.full-width {
  flex: 1;
  width: 100%;
}

.attach-button {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  background: var(--color-surface-alt);
  color: var(--color-primary);
  border: 1px solid var(--color-border);
  transition: all 0.2s ease;
}

.attach-button:hover {
  background: var(--accent-light);
  border-color: var(--color-primary);
}

.attach-button:deep(.q-icon) {
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
  border-radius: 8px;
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
  border-radius: 8px;
  background: var(--color-primary) !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(0, 185, 86, 0.2);
  transition: all 0.2s ease;
}

.submit-button:hover {
  background: var(--color-primary-hover) !important;
  box-shadow: 0 4px 12px rgba(0, 185, 86, 0.3);
  transform: translateY(-1px);
}

.submit-button:deep(.q-icon) {
  color: white !important;
}

.file-hidden {
  display: none;
}

.file-info {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: var(--color-primary);
  word-break: break-all;
}

.hint {
  font-size: 0.8125rem;
  color: var(--color-text-tertiary);
  margin: 0;
}

@media (max-width: 768px) {
  .prompt-input {
    padding: 1rem;
  }

  .input-container {
    gap: 0.5rem;
  }

  .textarea :deep(textarea) {
    font-size: 0.9rem;
    min-height: 40px;
  }

  .attach-button,
  .submit-button {
    width: 40px;
    height: 40px;
  }
}
</style>
