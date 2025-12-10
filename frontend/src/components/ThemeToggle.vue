<template>
  <q-btn 
    flat 
    round 
    class="theme-toggle-btn" 
    @click="toggle" 
    :title="title"
    unelevated
  >
    <q-icon :name="icon" size="24px" />
  </q-btn>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '../stores/appStore'
import { QBtn, QIcon } from 'quasar'

const appStore = useAppStore()
const toggle = () => appStore.toggleTheme()
const icon = computed(() => appStore.theme === 'light' ? 'light_mode' : 'dark_mode')
const title = computed(() => appStore.theme === 'light' ? 'Переключиться в темную' : 'Переключиться в светлую')
</script>

<style scoped>
.theme-toggle-btn {
  width: 40px !important;
  height: 40px !important;
  min-width: 40px !important;
  min-height: 40px !important;
  padding: 0 !important;
  color: #1f2937 !important;
  opacity: 0.7;
  transition: all 0.3s ease;
  background-color: transparent !important;
  border: none !important;
  flex-shrink: 0;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.theme-toggle-btn:hover {
  opacity: 1;
  background-color: rgba(0, 185, 86, 0.12) !important;
  transform: scale(1.1);
}

.theme-toggle-btn:active {
  transform: scale(0.95);
}

/* Light theme */
html:not(.dark) .theme-toggle-btn {
  color: #1f2937 !important;
}

html:not(.dark) .theme-toggle-btn:hover {
  background-color: rgba(0, 185, 86, 0.12) !important;
}

/* Dark theme - make button visible */
html.dark .theme-toggle-btn {
  color: #fbbf24 !important;
}

html.dark .theme-toggle-btn:hover {
  background-color: rgba(251, 191, 36, 0.15) !important;
}

/* Ensure icon is visible */
:deep(.q-icon) {
  color: inherit !important;
}
</style>
