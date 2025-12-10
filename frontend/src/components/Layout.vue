<template>
  <q-layout view="hHh lpR fFf">
    <!-- Mobile Menu Button -->
    <q-header v-if="$q.screen.lt.md" elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Toggle sidebar"
          @click="toggleSidebar"
        />
        <q-toolbar-title>
          TestOps Copilot
        </q-toolbar-title>
        <ThemeToggle />
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
    <q-drawer
      v-model="sidebarOpen"
      show-if-above
      :width="280"
      :breakpoint="1024"
      bordered
      class="bg-background sidebar-drawer"
    >
      <Sidebar
        :chat-histories="chatHistories"
        :current-chat-id="currentChatId"
        @new-chat="$emit('newChat')"
        @select-chat="$emit('selectChat', $event)"
        @remove-chat="$emit('removeChat', $event)"
        @clear-all-chats="$emit('clearAllChats')"
      />
    </q-drawer>

    <!-- Main Content -->
    <q-page-container>
      <q-page class="page-shell column no-wrap q-pa-none">
        <div class="page-status">
          <ApiStatusBadge />
        </div>
        <ChatArea
          :messages="messages"
          :is-loading="isLoading"
          @send-message="$emit('sendMessage', $event)"
        />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import ChatArea from './ChatArea.vue'
import ApiStatusBadge from './ApiStatusBadge.vue'
import ThemeToggle from './ThemeToggle.vue'
import { QLayout, QHeader, QDrawer, QPageContainer, QPage, QToolbar, QToolbarTitle, QBtn } from 'quasar'

interface ChatHistory {
  id: string
  title: string
  messages: any[]
  createdAt: number
  updatedAt: number
}

interface LayoutProps {
  messages: any[]
  isLoading: boolean
  chatHistories: ChatHistory[]
  currentChatId: string | null
}

interface LayoutEmits {
  (e: 'newChat'): void
  (e: 'selectChat', id: string): void
  (e: 'removeChat', id: string): void
  (e: 'clearAllChats'): void
  (e: 'sendMessage', payload: { text: string; file: File | null }): void
}

const props = defineProps<LayoutProps>()
const emit = defineEmits<LayoutEmits>()

const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<style scoped>
.sidebar-drawer {
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
  overflow: hidden;
}

.page-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  border-radius: var(--radius-md);
}

.page-status {
  display: flex;
  justify-content: center;
  padding: 0.75rem 0;
  background: var(--color-background-alt);
  border-bottom: 1px solid var(--color-border);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
}

@media (max-width: 1024px) {
  .sidebar-drawer {
    border-radius: 0;
  }
}
</style>
