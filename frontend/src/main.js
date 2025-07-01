// src/main.js

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "leaflet/dist/leaflet.css";

// ❌ KALDIRILDI: GoogleSignInPlugin import'u
// import GoogleSignInPlugin from "vue3-google-signin"

const app = createApp(App)

// ❌ KALDIRILDI: GoogleSignInPlugin'in app.use() ile kurulumu
/*
app.use(GoogleSignInPlugin, {
  // Client ID'niz aynı kalıyor.
  clientId: '659956907252-7km6e82iuv0gongd3ilnrsmb0chm7gho.apps.googleusercontent.com'
})
*/

app.use(router)
app.mount('#app')