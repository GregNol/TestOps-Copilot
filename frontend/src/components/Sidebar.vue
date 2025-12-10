<template>
  <aside class="sidebar">
    <!-- Header -->
    <div class="header">
      <div class="logo">
        <div class="logo-icon">
          <q-icon name="science" size="24px" />
        </div>
        <h1 class="logo-text">TestOps Copilot</h1>
      </div>
      <button
        class="new-chat-button"
        @click="handleNewChat"
        title="Новый чат"
        aria-label="Новый чат"
      >
        <q-icon name="add" size="20px" />
      </button>
    </div>

    <!-- Chat History -->
    <div class="history-container">
      <div class="history-header">
        <h3 class="history-title">История</h3>
        <button
          v-if="sortedChatHistories.length > 0"
          class="clear-button"
          @click="handleClearAll"
          title="Очистить всё"
          aria-label="Очистить всё"
        >
          <q-icon name="delete_sweep" size="18px" />
        </button>
      </div>

      <!-- Chat Items -->
      <div class="history-list">
        <p v-if="sortedChatHistories.length === 0" class="empty-state">
          Начните новый чат
        </p>
        <div
          v-for="chat in sortedChatHistories"
          :key="chat.id"
          :class="['chat-item', { 'active-item': appStore.currentChatId === chat.id }]"
        >
          <button
            class="chat-button"
            @click="handleSelectChat(chat.id)"
            :title="chat.title"
          >
            <q-icon 
              :name="chat.type === 'ui' ? 'web' : chat.type === 'api' ? 'api' : 'chat'" 
              size="18px" 
            />
            <span>{{ chat.title }}</span>
          </button>
          <button
            class="delete-button"
            @click.stop="handleDeleteChat(chat.id)"
            title="Удалить чат"
          >
            <q-icon name="close" size="16px" />
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation Menu -->
    <div class="nav-menu">
      <button class="nav-button" title="Экспорт результатов">
        <q-icon name="download" size="20px" />
        <span>Экспорт</span>
      </button>
      <button class="nav-button" title="Настройки">
        <q-icon name="settings" size="20px" />
        <span>Настройки</span>
      </button>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="footer-top">
        <div class="version-info">
          <q-icon name="science" size="16px" />
          <span>v0.2.0</span>
        </div>
        <ThemeToggle />
      </div>
      <div class="footer-bottom">
        <span class="powered-by">Powered by Cloud.ru</span>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '../stores/appStore'
import ThemeToggle from './ThemeToggle.vue'

const appStore = useAppStore()

const sortedChatHistories = computed(() =>
  [...appStore.chatHistories].sort((a, b) => b.updatedAt - a.updatedAt)
)

const handleNewChat = () => {
  appStore.createNewChat()
}

const handleSelectChat = (id: string) => {
  appStore.setCurrentChatId(id)
}

const handleDeleteChat = (id: string) => {
  if (confirm('Удалить этот чат?')) {
    appStore.removeChatHistory(id)
  }
}

const handleClearAll = () => {
  if (confirm('Очистить всю историю чатов?')) {
    appStore.chatHistories.forEach(chat => appStore.removeChatHistory(chat.id))
  }
}
</script>

<style scoped>
/* Modern Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  width: 280px;
  height: 100%;
  background: linear-gradient(180deg, var(--color-background-alt) 0%, var(--color-background) 100%);
  border-right: 1px solid var(--color-border);
  overflow: hidden;
  transition: background var(--transition-base), border-color var(--transition-base);
  justify-content: space-between;
}

/* Header with Modern Logo */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid var(--color-border);
  gap: 1rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  flex: 1;
  min-width: 0;
}

.logo-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #00c853 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 185, 86, 0.2);
}

.logo-text {
  font-size: 1.125rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-primary) 0%, #00c853 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.02em;
}

/* New Chat Button */
.new-chat-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--color-primary);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 185, 86, 0.2);
}

.new-chat-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 185, 86, 0.3);
  background: var(--color-primary-hover);
}

.new-chat-button:active {
  transform: translateY(0);
}

/* Workflow Section */
.workflow-section {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--color-border);
}

.section-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  margin-bottom: 0.75rem;
  letter-spacing: 0.5px;
}

/* History Container */
.history-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem 0.5rem;
  gap: 0.5rem;
}

.history-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  margin: 0;
  letter-spacing: 0.5px;
}

/* Clear Button */
.clear-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  color: var(--color-text-tertiary);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-button:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* History List */
.history-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.history-list::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-track {
  background: transparent;
}

.history-list::-webkit-scrollbar-thumb {
  background: var(--color-gray-300);
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover {
  background: var(--color-gray-400);
}

/* Empty State */
.empty-state {
  padding: 2rem 1rem;
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: auto;
}

/* Chat Item */
.chat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  position: relative;
  border-radius: 10px;
  transition: background-color 0.2s ease;
}

.chat-item:hover {
  background: var(--color-surface-hover);
}

.active-item {
  background: linear-gradient(135deg, rgba(0, 185, 86, 0.15) 0%, rgba(0, 200, 83, 0.1) 100%);
}

.active-item .chat-button {
  color: var(--color-primary);
  font-weight: 600;
}

/* Chat Button */
.chat-button {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0.875rem;
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: left;
  overflow: hidden;
  min-width: 0;
}

.chat-button:hover {
  color: var(--color-text-primary);
}

.chat-button span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

/* Delete Button */
.delete-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-tertiary);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  opacity: 0;
  margin-right: 0.5rem;
}

.chat-item:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

/* Navigation Menu */
.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid var(--color-border);
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.nav-button:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

/* Footer */
.footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--color-border);
  background: var(--color-background-alt);
}

.footer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.version-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.footer-bottom {
  display: flex;
  justify-content: center;
}

.powered-by {
  font-size: 0.7rem;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

/* Responsive */
@media (max-width: 1024px) {
  .sidebar {
    width: 260px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 150;
    width: 100%;
    max-width: 280px;
    height: 100%;
  }
}
</style>
