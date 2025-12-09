<template>
  <div class="loader">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  </div>
</template>

<script setup lang="ts">
// This component doesn't need any logic
</script>

<style scoped>
/* Loading Indicator Container */
.loader {
  display: flex;
  gap: 0.625rem;
  align-items: center;
  justify-content: center;
  padding: 1.75rem;
}

/* Loader Dot */
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--color-primary);
  animation: pulse 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  transition: background-color var(--transition-base);
}

.dot:nth-child(2) {
  animation-delay: 0.3s;
}

.dot:nth-child(3) {
  animation-delay: 0.6s;
}

/* Pulse Animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.4;
    transform: scale(0.85);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .loader {
    padding: 1.5rem;
    gap: 0.5rem;
  }

  .dot {
    width: 8px;
    height: 8px;
  }
}
</style>