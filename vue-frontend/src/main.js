import { createApp } from 'vue'
import App from './App.vue'
import router from './router'   // ← ✅ now it's from './router' not './router.js'

const app = createApp(App)
app.use(router)
app.mount('#app')
