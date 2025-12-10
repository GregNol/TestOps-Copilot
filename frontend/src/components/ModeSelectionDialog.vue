<template>
  <q-dialog v-model="showDialog" persistent>
    <q-card class="mode-selection-card">
      <q-card-section class="dialog-header">
        <div class="header-content">
          <h2 class="dialog-title">Выберите режим тестирования</h2>
          <p class="dialog-subtitle">Выберите, что вы хотите протестировать</p>
        </div>
      </q-card-section>

      <q-card-section class="mode-options">
        <div class="mode-grid">
          <button
            class="mode-card"
            @click="selectMode('ui')"
          >
            <div class="mode-icon ui-icon">
              <q-icon name="web" size="48px" />
            </div>
            <h3 class="mode-title">Тестировать UI</h3>
            <p class="mode-description">
              Анализ веб-интерфейса, генерация UI тест-кейсов на основе HTML
            </p>
            <div class="mode-features">
              <span class="feature-badge">Web Crawler</span>
              <span class="feature-badge">Playwright</span>
            </div>
          </button>

          <button
            class="mode-card"
            @click="selectMode('api')"
          >
            <div class="mode-icon api-icon">
              <q-icon name="api" size="48px" />
            </div>
            <h3 class="mode-title">Тестировать API</h3>
            <p class="mode-description">
              Генерация API тест-кейсов из OpenAPI/Swagger спецификации
            </p>
            <div class="mode-features">
              <span class="feature-badge">OpenAPI</span>
              <span class="feature-badge">Requests</span>
            </div>
          </button>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { QDialog, QCard, QCardSection, QIcon } from 'quasar'

interface Props {
  modelValue: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'modeSelected', mode: 'ui' | 'api'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const showDialog = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  showDialog.value = newVal
})

watch(showDialog, (newVal) => {
  emit('update:modelValue', newVal)
})

const selectMode = (mode: 'ui' | 'api') => {
  emit('modeSelected', mode)
  showDialog.value = false
}
</script>

<style scoped>
.mode-selection-card {
  max-width: 800px;
  width: 90vw;
  border-radius: 24px;
  background: var(--color-surface);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.dialog-header {
  padding: 2.5rem 2rem 1.5rem;
  background: linear-gradient(135deg, var(--color-primary) 0%, #00c853 100%);
  color: white;
}

.header-content {
  text-align: center;
}

.dialog-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}

.dialog-subtitle {
  font-size: 1rem;
  margin: 0;
  opacity: 0.95;
  font-weight: 400;
}

.mode-options {
  padding: 2rem;
}

.mode-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.mode-card {
  position: relative;
  background: var(--color-surface-alt);
  border: 2px solid var(--color-border);
  border-radius: 20px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.mode-card:hover {
  border-color: var(--color-primary);
  background: var(--color-surface-hover);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 185, 86, 0.15);
}

.mode-card:active {
  transform: translateY(-2px);
}

.mode-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.ui-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.api-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.mode-card:hover .mode-icon {
  transform: scale(1.1);
}

.mode-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
}

.mode-description {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

.mode-features {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 0.5rem;
}

.feature-badge {
  background: var(--color-primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.02em;
}

@media (max-width: 768px) {
  .mode-grid {
    grid-template-columns: 1fr;
  }
  
  .dialog-title {
    font-size: 1.5rem;
  }
  
  .mode-selection-card {
    width: 95vw;
  }
}
</style>
