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
  width: 40px;
  height: 40px;
  color: #1f2937 !important;
  opacity: 0.8;
  transition: opacity 0.3s, color 0.3s;
  background-color: transparent !important;
  border: none !important;
}

.theme-toggle-btn:hover {
  opacity: 1;
  background-color: rgba(0, 185, 86, 0.1) !important;
}

/* Light theme */
:global(.body--light) .theme-toggle-btn,
:global(html:not(.dark)) .theme-toggle-btn {
  color: #1f2937 !important;
}

:global(.body--light) .theme-toggle-btn:hover,
:global(html:not(.dark)) .theme-toggle-btn:hover {
  background-color: rgba(0, 185, 86, 0.15) !important;
}

/* Dark theme - make button visible */
:global(.dark) .theme-toggle-btn,
:global(.body--dark) .theme-toggle-btn {
  color: #fbbf24 !important;
}

:global(.dark) .theme-toggle-btn:hover,
:global(.body--dark) .theme-toggle-btn:hover {
  background-color: rgba(251, 191, 36, 0.2) !important;
}

/* Ensure icon is visible */
:deep(.q-icon) {
  color: inherit !important;
}
</style>
