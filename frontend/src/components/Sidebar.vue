<template>
  <aside class="sidebar">
    <!-- Header -->
    <div class="header">
      <div class="logo">
        <span class="logo-icon">🤖</span>
        <h1 class="logo-text">TestOps Copilot</h1>
      </div>
      <button
        class="new-chat-button"
        @click="handleNewChat"
        title="Новый чат"
        aria-label="Новый чат"
      >
        <q-icon name="add" size="18px" />
      </button>
    </div>

    <!-- Chat History -->
    <div class="history-container">
      <div class="history-header">
        <h3 class="history-title">История чатов</h3>
        <button
          v-if="sortedChatHistories.length > 0"
          class="clear-button"
          @click="handleClearAll"
          title="Очистить всё"
          aria-label="Очистить всё"
        >
          <q-icon name="delete" size="16px" />
        </button>
      </div>

      <!-- Chat Items -->
      <div class="history-list">
        <p v-if="sortedChatHistories.length === 0" class="empty-state">
          Начните новый разговор
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
            <q-icon name="chat_bubble_outline" size="16px" />
            <span>{{ chat.title }}</span>
          </button>
          <button
            v-if="appStore.currentChatId === chat.id"
            class="delete-button"
            @click="handleDeleteChat(chat.id)"
            title="Удалить чат"
          >
            <q-icon name="close" size="14px" />
          </button>
        </div>
      </div>
    </div>

    <!-- Model, Settings, Tests Sections -->
    <div class="extra-sections">
      <button class="section-button" title="Выбор модели">
        <q-icon name="tune" size="18px" />
        <span>Модель</span>
      </button>
      <button class="section-button muted" title="Настройки">
        <q-icon name="settings" size="18px" />
        <span>Настройки</span>
      </button>
      <button class="section-button muted" title="Просмотр тестов">
        <q-icon name="inventory" size="18px" />
        <span>Тесты</span>
      </button>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="footer-top">
        <p class="footer-text">TestOps Copilot v0.1.0</p>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
          <button class="help-button" title="Справка">Справка</button>
          <ThemeToggle />
        </div>
      </div>
      <p class="footer-subtext">Powered by Cloud.ru</p>
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
/* Documentation-style Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  width: 260px;
  height: 100%;
  background-color: var(--color-background-alt);
  border-right: 1px solid var(--color-border);
  overflow: hidden;
  transition: background-color var(--transition-base), border-color var(--transition-base);
}

/* Header with Logo */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid var(--color-border);
  gap: 0.75rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.logo-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.logo-text {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* New Chat Button */
.new-chat-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
  border: 1px solid var(--color-primary);
  cursor: pointer;
  transition: transform var(--transition-base), box-shadow var(--transition-base);
  flex-shrink: 0;
}

.new-chat-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0, 185, 86, 0.12);
}

.new-chat-button:active {
  transform: translateY(0);
}

/* History Container */
.history-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

/* History Header with Title and Clear Button */
.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--color-border);
}

.history-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  margin: 0;
  letter-spacing: 0.5px;
}

/* Clear All Button */
.clear-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background-color: var(--color-surface-alt);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: background-color var(--transition-base), color var(--transition-base);
  flex-shrink: 0;
}

.clear-button:hover {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
}

/* Chat History List */
.history-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0;
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

/* Empty State Message */
.empty-state {
  padding: 2rem 1.25rem;
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: auto;
}

/* Chat Item Container */
.chat-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  gap: 0.5rem;
  position: relative;
}

.active-item {
  background-color: var(--color-primary);
}

.active-item .chat-button {
  color: var(--color-text-inverse);
}

.active-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: var(--color-primary-active);
  border-radius: 0 3px 3px 0;
}

/* Chat Button */
.chat-button {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  background-color: transparent;
  color: var(--color-text-secondary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color var(--transition-base), transform var(--transition-base);
  font-size: 0.875rem;
  font-weight: 500;
  text-align: left;
  overflow: hidden;
  min-width: 0;
}

.chat-button:hover {
  background-color: rgba(0, 185, 86, 0.06);
  color: var(--color-text-primary);
}

.chat-button svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  opacity: 0.9;
  color: inherit;
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
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background-color: transparent;
  color: var(--color-text-tertiary);
  border: none;
  cursor: pointer;
  transition: background-color var(--transition-base), color var(--transition-base);
  flex-shrink: 0;
  opacity: 0;
}

.chat-item:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  background-color: var(--color-error);
  color: var(--color-text-inverse);
}

/* Extra Sections (Model, Settings, Tests) */
.extra-sections {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1.5rem 0 0.5rem 0;
  padding: 0 1.25rem;
}

.section-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  background: var(--color-primary);
  color: var(--color-text-inverse);
  border: 1px solid var(--color-primary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color var(--transition-base), transform var(--transition-base);
}

.section-button.muted {
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.section-button:hover {
  transform: translateY(-1px);
}

.section-button.muted:hover {
  background: var(--color-surface-alt);
}

/* Footer */
.footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--color-border);
  background-color: var(--color-background-alt);
  transition: background-color var(--transition-base), border-color var(--transition-base);
}

.footer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.footer-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin: 0;
}

.footer-subtext {
  font-size: 0.65rem;
  color: var(--color-text-tertiary);
  margin: 0;
}

.help-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.6rem;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color var(--transition-base);
}

.help-button:hover {
  background: var(--color-surface-alt);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }

  .header {
    padding: 1rem 1rem;
  }

  .logo-text {
    font-size: 0.875rem;
  }

  .new-chat-button {
    width: 32px;
    height: 32px;
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

  .header {
    padding: 1rem;
  }

  .logo-icon {
    font-size: 1.25rem;
  }

  .logo-text {
    font-size: 0.875rem;
  }

  .new-chat-button {
    width: 32px;
    height: 32px;
  }
}
</style>
