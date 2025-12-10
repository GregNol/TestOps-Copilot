<template>
  <div :class="['error-display', severityClass]">
    <div class="error-icon">
      <q-icon :name="iconName" size="28px" />
    </div>
    <div class="error-content">
      <h4 class="error-title">{{ title || defaultTitle }}</h4>
      <p class="error-message">{{ message }}</p>
      <p v-if="details" class="error-details">{{ details }}</p>
      <div v-if="actions" class="error-actions">
        <q-btn
          v-for="action in actions"
          :key="action.label"
          :label="action.label"
          :color="action.color || 'primary'"
          :outline="action.outline !== false"
          size="sm"
          @click="action.handler"
          class="action-button"
        />
      </div>
    </div>
    <button v-if="closable" class="close-button" @click="$emit('close')">
      <q-icon name="close" size="20px" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { QIcon, QBtn } from 'quasar'

type ErrorSeverity = 'error' | 'warning' | 'info'

interface ErrorAction {
  label: string
  handler: () => void
  color?: string
  outline?: boolean
}

interface Props {
  title?: string
  message: string
  details?: string
  severity?: ErrorSeverity
  closable?: boolean
  actions?: ErrorAction[]
}

const props = withDefaults(defineProps<Props>(), {
  severity: 'error',
  closable: true
})

defineEmits<{
  (e: 'close'): void
}>()

const severityClass = computed(() => `severity-${props.severity}`)

const iconName = computed(() => {
  switch (props.severity) {
    case 'error': return 'error_outline'
    case 'warning': return 'warning_amber'
    case 'info': return 'info_outline'
    default: return 'error_outline'
  }
})

const defaultTitle = computed(() => {
  switch (props.severity) {
    case 'error': return 'Произошла ошибка'
    case 'warning': return 'Предупреждение'
    case 'info': return 'Информация'
    default: return 'Ошибка'
  }
})
</script>

<style scoped>
.error-display {
  display: flex;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
  border: 2px solid;
  position: relative;
  animation: slideIn 0.3s ease-out;
  backdrop-filter: blur(10px);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.severity-error {
  background: linear-gradient(135deg, rgba(248, 113, 113, 0.08) 0%, rgba(248, 113, 113, 0.03) 100%);
  border-color: #f87171;
}

.severity-warning {
  background: linear-gradient(135deg, rgba(251, 146, 60, 0.08) 0%, rgba(251, 146, 60, 0.03) 100%);
  border-color: #fb923c;
}

.severity-info {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, rgba(34, 197, 94, 0.03) 100%);
  border-color: #22c55e;
}

.error-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.severity-error .error-icon {
  background: rgba(248, 113, 113, 0.12);
  color: #f87171;
}

.severity-warning .error-icon {
  background: rgba(251, 146, 60, 0.12);
  color: #fb923c;
}

.severity-info .error-icon {
  background: rgba(34, 197, 94, 0.12);
  color: #22c55e;
}

.error-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.error-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: -0.01em;
}

.error-message {
  margin: 0;
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.error-details {
  margin: 0;
  font-size: 0.875rem;
  color: var(--color-text-tertiary);
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  background: var(--color-surface-alt);
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border-left: 3px solid var(--color-border);
  overflow-x: auto;
}

.error-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.action-button {
  border-radius: 10px;
  text-transform: none;
  font-weight: 500;
  letter-spacing: 0;
}

.close-button {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  transition: all 0.2s ease;
}

.close-button:hover {
  background: var(--color-surface-alt);
  color: var(--color-text-primary);
}

.close-button:active {
  transform: scale(0.95);
}

@media (max-width: 640px) {
  .error-display {
    padding: 1rem;
  }
  
  .error-icon {
    width: 40px;
    height: 40px;
  }
  
  .error-title {
    font-size: 1rem;
  }
  
  .error-message {
    font-size: 0.875rem;
  }
}
</style>
