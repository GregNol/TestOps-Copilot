// Minimal Quasar user options placeholder
import 'quasar/dist/quasar.css'
import '@quasar/extras/material-icons/material-icons.css'
import './styles/main.css'
import { Notify } from 'quasar'

export default {
  config: {
    brand: {
      primary: '#00b956',
      secondary: '#00a04d',
      accent: '#00c853',
      dark: '#1a1f26',
      positive: '#00c853',
      negative: '#ef4444',
      info: '#00b956',
      warning: '#f59e0b'
    }
  },
  plugins: {
    Notify,
  },
}
