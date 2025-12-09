<template>
  <div :class="['api-status', status]">
    <q-icon :name="iconName" size="16px" />
    <span class="label">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { checkHealth } from '../utils/api'

const status = ref<'checking' | 'online' | 'offline'>('checking')
let timer: number | null = null

const pollHealth = async () => {
  status.value = 'checking'
  const isOnline = await checkHealth()
  status.value = isOnline ? 'online' : 'offline'
}

onMounted(() => {
  pollHealth()
  timer = window.setInterval(pollHealth, 15000)
})

onBeforeUnmount(() => {
  if (timer) window.clearInterval(timer)
})

const iconName = computed(() => {
  if (status.value === 'online') return 'cloud_done'
  if (status.value === 'offline') return 'cloud_off'
  return 'sync'
})

const label = computed(() => {
  if (status.value === 'online') return 'API: online'
  if (status.value === 'offline') return 'API: offline'
  return 'API: проверка'
})
</script>

<style scoped>
.api-status {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}

.api-status.online {
  color: var(--color-primary);
  border-color: var(--accent-border);
  background: var(--accent-light);
}

.api-status.offline {
  color: var(--color-error);
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.08);
}

.api-status .label {
  white-space: nowrap;
}
</style>
