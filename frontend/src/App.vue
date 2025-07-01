<!-- src/App.vue -->
<!-- src/App.vue -->
<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      userName: ''
    };
  },
  watch: {
    '$route'(to, from) {
      console.log(`B. URL değişti: ${from.path} -> ${to.path}. Durum kontrol ediliyor.`);
      this.checkLoginStatus();
    }
  },
  created() {
    console.log("A. App.vue bileşeni OLUŞTURULDU. Durum kontrol ediliyor.");
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      console.log("C. checkLoginStatus metodu çalıştı.");
      const token = localStorage.getItem('user_token');
      
      if (token) {
        console.log("D. localStorage'da token bulundu:", token);
        try {
          const decodedToken = jwtDecode(token);
          console.log("E. Token çözümlendi:", decodedToken);

          const currentTime = Date.now() / 1000;
          if (decodedToken.exp > currentTime) {
            console.log("F. Token geçerli. Kullanıcı durumu güncelleniyor.");
            this.isLoggedIn = true;
            this.userName = decodedToken.name;
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          } else {
            console.log("F. HATA: Token'ın süresi dolmuş.");
            this.logout();
          }
        } catch (error) {
          console.error("F. HATA: Token çözümlenirken sorun oluştu.", error);
          this.logout();
        }
      } else {
        console.log("D. localStorage'da token BULUNAMADI.");
        this.logout();
      }
    },
    logout() {
      console.log("G. Logout metodu çalıştı, durum sıfırlanıyor.");
      localStorage.removeItem('user_token');
      this.isLoggedIn = false;
      this.userName = '';
      delete axios.defaults.headers.common['Authorization'];
    }
  }
}
</script>
<template>
  <!-- Bu kısım önemli: updateUserStatus'a artık gerek yok -->
  <router-view :isLoggedIn="isLoggedIn" :userName="userName" />
</template>