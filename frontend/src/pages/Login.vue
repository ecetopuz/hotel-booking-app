<template>
  <div class="login-page">
    <div class="form-container">
      
      <div v-if="!isRegisterMode" class="form-box">
        <h2>Giriş Yap</h2>
       
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="login-email">Kullanıcı email:</label>
            <input type="email" id="login-email" v-model="loginData.email" required />
          </div>
          <div class="input-group">
            <label for="login-password">Şifre:</label>
            <input type="password" id="login-password" v-model="loginData.password" required />
          </div>
          <div class="button-group">
            <button type="submit" class="btn-primary">GİRİŞ</button>
            <button type="button" @click="isRegisterMode = true" class="btn-secondary">Üye Ol</button>
          </div>
        </form>
      </div>

      <!-- KAYIT FORMU -->
      <div v-else class="form-box">
        <h2>Kayıt Ol</h2>
        <form @submit.prevent="handleRegister">
          <div class="input-group">
            <label for="reg-name">Ad:</label>
            <input type="text" id="reg-name" v-model="registerData.name" required />
          </div>
          <div class="input-group">
            <label for="reg-surname">Soyad:</label>
            <input type="text" id="reg-surname" v-model="registerData.surname" required />
          </div>
          <div class="input-group">
            <label for="reg-email">Kullanıcı email:</label>
            <input type="email" id="reg-email" v-model="registerData.email" required />
          </div>
          <div class="input-group">
  <label for="reg-password">Şifre:</label>
  <input type="password" id="reg-password" v-model="registerData.password" required />
  <small class="password-hint">
    En az 8 karakter, 1 rakam ve 1 özel karakter (!@#$%) içermelidir.
  </small>
          </div>
          <div class="input-group">
            <label for="reg-password-repeat">Tekrar:</label>
            <input type="password"id="reg-password-repeat"v-model="registerData.passwordRepeat" required/>
          </div>
          <div class="input-group">
            <label for="reg-country">Ülke:</label>
            <select id="reg-country" v-model="registerData.country" required>
              <option value="Türkiye">Türkiye</option>
              <option value="Yunanistan">Yunanistan</option>
              <option value="Macaristan">Macaristan</option>
            </select>
          </div>
           <div class="input-group">
            <label for="reg-city">Şehir:</label>
            <select id="reg-city" v-model="registerData.city" required>
              <option value="İzmir">İzmir</option>
              <option value="Ankara">Ankara</option>
              <option value="İstanbul">İstanbul</option>
              <option value="Manisa">Manisa</option>
              <option value="Bursa">Bursa</option>
            </select>
          </div>
          <div class="input-group">
              <label for="reg-photo">Profil Fotoğrafı (İsteğe Bağlı):</label>
              <input type="file" id="reg-photo" @change="handleFileUpload" accept="image/*" />
          </div>
          <div class="button-group">
            <button type="submit" class="btn-primary">Kayıt Ol</button>
            <button type="button" @click="isRegisterMode = false" class="btn-secondary">Giriş Yap</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import '../assets/Login.css';
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const API_URL = 'http://localhost:5000';

export default {
  name: 'Login',
  components: {},
  setup() {
    const router = useRouter();
    const isRegisterMode = ref(false);
    
    const loginData = ref({ email: '', password: '' });
    const registerData = ref({ 
        name: '', 
        surname: '', 
        email: '', 
        password: '', 
        passwordRepeat: '', 
        country: 'Türkiye', 
        city: 'İzmir', 
        photo: null 
    });

    const validatePassword = (password) => {
      if (password.length < 8) return false;
      if (!/\d/.test(password)) return false;
      if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) return false;
      return true;
    };
    
    const handleLogin = async () => {
      try {
        const response = await axios.post(`${API_URL}/api/login`, loginData.value);
        localStorage.setItem('user_token', response.data.access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
        window.location.href = '/'; 
      } catch (error) {
        const errorMessage = error.response?.data?.error || 'Giriş başarısız oldu. Lütfen bilgilerinizi kontrol edin.';
        alert(errorMessage);
        console.error("Giriş hatası:", error.response || error);
      }
    };

    const handleRegister = async () => {
      if (registerData.value.password !== registerData.value.passwordRepeat) {
        alert('Şifreler uyuşmuyor!');
        return;
      }
      if (!validatePassword(registerData.value.password)) {
        alert('Şifreniz kurallara uymuyor.\n\n- En az 8 karakter\n- En az 1 rakam\n- En az 1 özel karakter (!@#$%) içermelidir.');
        return;
      }
      
      const formData = new FormData();
      Object.keys(registerData.value).forEach(key => {
        if (key !== 'passwordRepeat') {
          formData.append(key, registerData.value[key]);
        }
      });

      try {
        const response = await axios.post(`${API_URL}/api/register`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        const accessToken = response.data.access_token;
        if (!accessToken) {
          throw new Error("Kayıt sonrası token alınamadı.");
        }

        localStorage.setItem('user_token', accessToken);
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        
        window.location.href = '/'; 

      } catch (error) {
        const errorMessage = error.response?.data?.error || 'Kayıt sırasında bir hata oluştu.';
        alert(errorMessage);
        console.error("Kayıt hatası:", error.response || error);
      }
    };

    const handleFileUpload = (event) => {
        registerData.value.photo = event.target.files[0];
    };

    return {
      isRegisterMode,
      loginData,
      registerData,
      handleLogin,
      handleRegister,
      handleFileUpload,
    };
  },
};
</script>