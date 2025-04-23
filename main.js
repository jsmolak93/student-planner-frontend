// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router.js'; // Make sure this is the correct path

createApp(App).use(router).mount('#app');
