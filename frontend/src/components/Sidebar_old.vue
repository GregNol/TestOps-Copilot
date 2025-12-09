<template>
  <aside class="sidebar">
    <!-- Header with Logo -->
    <div class="header">
      <div class="logo">
        <span class="logoIcon">🤖</span>
        <h1 class="logoText">TestOps Copilot</h1>
      </div>
      <button
        class="newChatButton"
        @click="$emit('newChat')"
        title="Новый чат"
        aria-label="Новый чат"
      >
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 2V18M2 10H18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </button>
    </div>

    <!-- Chat History -->
    <div class="historyContainer">
      <div class="historyHeader">
        <h3 class="historyTitle">История чатов</h3>
        <button
          v-if="chatHistories.length > 0"
          class="clearButton"
          @click="$emit('clearAllChats')"
          title="Очистить"
          aria-label="Очистить"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M2 4h12M6.5 7v4M9.5 7v4M3 4l1 10c0 0.5 0.5 1 1 1h6c0.5 0 1-0.5 1-1l1-10M6 4V3c0-0.5 0.5-1 1-1h2c0.5 0 1 0.5 1 1v1"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
            />
          </svg>
        </button>
      </div>

      <!-- Chat Items -->
      <div class="historyList">
        <div v-if="chatHistories.length === 0" class="emptyState">
          Новый разговор
        </div>
        <div
          v-else
          v-for="chat in sortedChatHistories"
          :key="chat.id"
          class="chatItem"
          :class="{ activeItem: currentChatId === chat.id }"
        >
          <button
            class="chatButton"
            @click="$emit('selectChat', chat.id)"
            :title="chat.title"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                d="M2 2H14C15.1 2 16 2.9 16 4V12C16 13.1 15.1 14 14 14H3L1 16V4C1 2.9 1.9 2 3 2Z"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
            </svg>
            <span>{{ chat.title }}</span>
          </button>
          <button
            v-if="currentChatId === chat.id"
            class="deleteButton"
            @click="$emit('removeChat', chat.id)"
            title="Удалить чат"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path
                d="M1 1L13 13M13 1L1 13"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Extra Sections -->
    <div class="extraSections">
      <button class="sectionButton" title="Выбор модели">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M6 9l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>Модель</span>
      </button>
      <button class="sectionButton" title="Настройки">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M9 5v4l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>Настройки</span>
      </button>
      <button class="sectionButton" title="Просмотр тестов">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <rect x="3" y="5" width="12" height="8" rx="2" stroke="currentColor" stroke-width="2"/>
          <path d="M6 9h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>Тесты</span>
      </button>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="footerTop">
        <p class="footerText">TestOps Copilot v0.1.0</p>
        <div style="display: flex; gap: 0.5rem; align-items: center">
          <button class="helpButton" title="Справка">Справка</button>
          <ThemeToggle />
        </div>
      </div>
      <p class="footerSubtext">Powered by Cloud.ru</p>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '../stores/appStore'
import ThemeToggle from './ThemeToggle.vue'

const appStore = useAppStore()

const chatHistories = computed(() => appStore.chatHistories || [])
const currentChatId = computed(() => appStore.currentChatId)
const sortedChatHistories = computed(() => [...chatHistories.value].sort((a, b) => b.updatedAt - a.updatedAt))

// Define emits
const emit = defineEmits<{
  (e: 'newChat'): void
  (e: 'selectChat', id: string): void
  (e: 'removeChat', id: string): void
  (e: 'clearAllChats'): void
}>()
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

.logoIcon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.logoText {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* New Chat Button */
.newChatButton {
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

.newChatButton:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0, 185, 86, 0.12);
}

.newChatButton:active {
  transform: translateY(0);
}

/* History Container */
.historyContainer {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

/* History Header with Title and Clear Button */
.historyHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--color-border);
}

.historyTitle {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  margin: 0;
  letter-spacing: 0.5px;
}

/* Clear All Button */
.clearButton {
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

.clearButton:hover {
  background-color: var(--color-primary-light);
  color: var(--color-text-inverse);
}

/* Chat History List */
.historyList {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.historyList::-webkit-scrollbar {
  width: 6px;
}

.historyList::-webkit-scrollbar-track {
  background: transparent;
}

.historyList::-webkit-scrollbar-thumb {
  background: var(--color-gray-300);
  border-radius: 3px;
}

.historyList::-webkit-scrollbar-thumb:hover {
  background: var(--color-gray-400);
}

/* Empty State Message */
.emptyState {
  padding: 2rem 1.25rem;
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: auto;
}

/* Chat Item Container */
.chatItem {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  gap: 0.5rem;
  position: relative;
}

.activeItem {
  background-color: var(--color-primary);
}

.activeItem .chatButton {
  color: var(--color-text-inverse);
}

.activeItem::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: var(--color-primary-dark);
  border-radius: 0 3px 3px 0;
}

/* Chat Button */
.chatButton {
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
  transition: background-color var(--transition-base), transform var(--transition-base), opacity var(--transition-base), box-shadow var(--transition-base);
  font-size: 0.875rem;
  font-weight: 500;
  text-align: left;
  overflow: hidden;
  min-width: 0;
}

.chatButton:hover {
  background-color: rgba(0, 185, 86, 0.06);
  color: var(--color-text-primary);
}

.chatButton svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  opacity: 0.9;
  color: inherit;
}

.chatButton span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

/* Delete Button */
.deleteButton {
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
  transition: background-color var(--transition-base), transform var(--transition-base), opacity var(--transition-base), box-shadow var(--transition-base);
  flex-shrink: 0;
  opacity: 0;
}

.chatItem:hover .deleteButton {
  opacity: 1;
}

.deleteButton:hover {
  background-color: var(--color-error);
  color: var(--color-text-inverse);
}

/* Footer */
.footerText {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin: 0;
}

.footerSubtext {
  font-size: 0.65rem;
  color: var(--color-text-tertiary);
  margin: 0;
}

.footerTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--color-border);
  background-color: var(--color-background-alt);
  transition: background-color var(--transition-base), border-color var(--transition-base);
}

.helpButton {
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
  transition: background-color var(--transition-base), transform var(--transition-base);
}

.helpButton:hover {
  background: var(--color-surface-alt);
}

/* Extra Sections (Model, Settings, Tests) */
.extraSections {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1.5rem 0 0.5rem 0;
}

.sectionButton {
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
  transition: background-color var(--transition-base), color var(--transition-base), transform var(--transition-base);
}

.sectionButton:hover {
  background: var(--color-primary-light);
  transform: translateY(-1px);
}

.sectionButton:active {
  background: var(--color-primary-dark);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }

  .header {
    padding: 1rem 1rem;
  }

  .logoText {
    font-size: 0.875rem;
  }

  .newChatButton {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: var(--z-modal);
    width: 100%;
    max-width: 280px;
    height: 100%;
    transform: translateX(-100%);
    transition: transform var(--transition-base);
    box-shadow: 2px 0 16px rgba(0, 0, 0, 0.1);
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .header {
    padding: 1rem;
  }

  .logoIcon {
    font-size: 1.25rem;
  }

  .logoText {
    font-size: 0.875rem;
  }

  .newChatButton {
    width: 32px;
    height: 32px;
  }

  .historyList {
    padding: 0.5rem 0;
  }

  .emptyState {
    padding: 1.5rem 1rem;
  }
}
</style>
