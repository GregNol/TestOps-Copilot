<template>
  <q-layout view="hHh lpR fFf">
    <q-header v-if="$q.screen.lt.md" bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="toggleSidebar" aria-label="Открыть меню" />
        <q-toolbar-title>TestOps Copilot</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="sidebarOpen"
      show-if-above
      :width="260"
      :breakpoint="1024"
      bordered
      class="bg-background"
    >
      <Sidebar />
    </q-drawer>

    <q-page-container>
      <q-page class="page-shell column no-wrap">
        <ChatArea />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { QLayout, QHeader, QDrawer, QPageContainer, QPage, QToolbar, QToolbarTitle, QBtn } from 'quasar'
import Sidebar from '../components/Sidebar.vue'
import ChatArea from '../components/ChatArea.vue'

const sidebarOpen = ref(false)
const toggleSidebar = () => { sidebarOpen.value = !sidebarOpen.value }
</script>

<style scoped>
.page-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
}
</style>
