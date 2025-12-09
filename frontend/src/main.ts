import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar } from 'quasar'
import App from './App.vue'
import quasarUserOptions from './quasar-user-options'
import './styles/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(Quasar, quasarUserOptions)
app.mount('#app')
