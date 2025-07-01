<!-- src/pages/HotelDetail.vue -->
<!-- src/pages/HotelDetail.vue -->
<template>
  <div class="page-container">
    <!-- 1. Yükleniyor durumu için bir div -->
    <div v-if="loading" class="loading-state">Otel bilgileri yükleniyor...</div>
    
    <!-- 2. Hata durumu için bir div -->
    <div v-else-if="error" class="error-state">{{ error }}</div>
    
    <!-- 3. Veri yüklendiğinde gösterilecek ana div -->
    <div v-else-if="hotel" class="hotel-detail-container">
      
      <!-- 1. SOL SÜTUN: Ana içerik -->
      <div class="left-column">
        <header class="hotel-header">
          <h1>{{ hotel.name }}</h1>
          <div class="rating-box">
            <span class="rating-score">{{ hotel.rating }}</span>
            <span>{{ getRatingText(hotel.rating) }}</span>
            <a href="#comments" class="comments-link">({{ hotel.commentsCount }} yorum)</a>
          </div>
        </header>

        <img :src="hotel.photo" class="main-photo" alt="Otel ana fotoğrafı">
        
        <div v-if="hotel.amenities && hotel.amenities.length > 0">
          <h2>Popüler konaklama yeri imkân ve özellikleri</h2>
          <ul class="amenities-list">
            <li v-for="amenity in hotel.amenities.slice(0, 5)" :key="amenity.name">
              {{ amenity.name }}
            </li>
            <li v-if="hotel.amenities.length > 5">
              <a href="#">... ve daha fazlası</a>
            </li>
          </ul>
        </div>
        
        <div id="comments" class="comments-section">
          <h2>Yorumlar</h2>
          <div v-if="hotel.ratingDistribution && hotel.ratingDistribution.length > 0" class="rating-summary">
            <h3>{{ hotel.rating }}/10 {{ getRatingText(hotel.rating) }}</h3>
            <p>{{ hotel.commentsCount }} doğrulanmış yorum</p>
            <div class="rating-bars">
              <div v-for="item in hotel.ratingDistribution" :key="item.category" class="rating-bar-item">
                <span class="category-name">{{ item.category }}</span>
                <div class="bar-container">
                  <div class="bar" :style="{ width: (item.score / 10 * 100) + '%' }"></div>
                </div>
                <span class="category-score">{{ item.score }}</span>
              </div>
            </div>
          </div>
          <div v-if="hotel.comments && hotel.comments.length > 0" class="comment-list">
            <div v-for="comment in hotel.comments" :key="comment.date" class="comment-card">
              <h3>{{ comment.rating }}/10 - {{ comment.title }}</h3>
              <p>"{{ comment.text }}"</p>
              <small>{{ comment.author }} - {{ new Date(comment.date).toLocaleDateString('tr-TR') }}</small>
            </div>
          </div>
          <div v-else>
            <p>Bu otel için henüz yorum yapılmamış.</p>
          </div>
        </div>
      </div>

      <!-- 2. SAĞ SÜTUN: Harita, Adres ve Fiyat -->
      <div class="right-column">
        <div class="map-widget">
          <mini-map 
            v-if="hotel.lat && hotel.lng" 
            :hotels="[hotel]" 
            :center="[hotel.lat, hotel.lng]"
            :zoom="14" 
          />
        </div>
        <div class="address-box">
          <p>{{ hotel.city }}, {{ hotel.country }}</p>
        </div>
        
        <!-- ================================================================ -->
        <!-- === FİYAT KARTININ GÜNCELLENMİŞ HALİ === -->
        <!-- ================================================================ -->
        <div class="price-box">
          <h3>Gecelik Fiyat</h3>
          
          <!-- Yeni, tutarlı fiyat gösterim bölümü -->
          <div class="price-section-detail">
            <div v-if="hotel.specialDiscountRate" class="discount-badge">
              %{{ hotel.specialDiscountRate }} indirim
            </div>
            <div class="price-display">
              <div>
                <p v-if="hotel.specialDiscountRate" class="original-price">
                  <s>{{ formatPrice(hotel.price) }}</s>
                </p>
                <p class="standard-price">{{ formatPrice(hotel.publicPrice) }}</p>
              </div>
            </div>
          </div>

          <!-- Üye Fiyatı Bölümü -->
          <div v-if="isLoggedIn && hotel.memberPrice" class="member-price-highlight-section">
            <div class="member-benefit-tag">
              <span>💎 Üye Fiyatı</span>
            </div>
            <p class="member-price-value">{{ formatPrice(hotel.memberPrice) }}</p>
          </div>
          
          <!-- Giriş Yapmamış Kullanıcı İçin Uyarı -->
          <div v-if="!isLoggedIn && hotel.memberPrice" class="login-prompt-section">
              <p class="login-for-member-price">
                Üye fiyatını görmek için <router-link to="/login" @click.stop>giriş yapın</router-link>
              </p>
          </div>

          <button class="reserve-button">Oda Seç</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import MiniMap from '../components/MiniMap.vue';

export default {
  name: 'HotelDetail',
  components: {
    MiniMap
  },
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  
  // --- SETUP FONKSİYONU BAŞLANGICI ---
  setup(props) {
    // 1. Reaktif değişkenleri tanımla
    const hotel = ref(null);
    const loading = ref(true);
    const error = ref(null);

    // 2. YARDIMCI FONKSİYONLARI TANIMLA (Hepsi aynı seviyede)
    
    const formatPrice = (price) => {
        return price ? price.toLocaleString('tr-TR', { style: 'currency', currency: 'TRY' }) : 'Fiyat bilgisi yok';
    };
    
    // getRatingText burada, fetchHotelDetails'ın DIŞINDA tanımlanmalı
    const getRatingText = (score) => {
      if (!score) return ''; 
      if (score >= 9) return 'Olağanüstü';
      if (score >= 8) return 'Çok İyi';
      if (score >= 7) return 'İyi';
      return 'Değerlendirildi';
    };

    // 3. ANA FONKSİYONU TANIMLA
    
    const fetchHotelDetails = async () => {
      loading.value = true;
      error.value = null;
      try {
        const response = await axios.get(`http://localhost:5000/api/hotel/${props.id}`);
        hotel.value = response.data;
      } catch (err) {
        error.value = 'Otel bilgileri yüklenemedi. Lütfen daha sonra tekrar deneyin.';
        console.error("API Hatası:", err);
      } finally {
        loading.value = false;
      }
    };

    // 4. LIFECYCLE HOOK'UNU KULLAN
    
    onMounted(fetchHotelDetails);

    // 5. TEMPLATE'DE KULLANILACAK HER ŞEYİ RETURN ET
    // Artık hem formatPrice hem de getRatingText doğru şekilde erişilebilir.
    return { 
      hotel, 
      loading, 
      error, 
      formatPrice, 
      getRatingText 
    }; 
  }
  // --- SETUP FONKSİYONU BİTİŞİ ---
}
</script>

<style scoped>
.page-container {
  padding: 20px;
  background-color: #f7f7f7; /* Sayfa arkasına hafif bir renk verebiliriz */
}
.hotel-detail-container {
  display: flex;
  flex-wrap: wrap; /* Küçük ekranlarda alt alta geçsin */
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}
.left-column {
  flex: 2; /* Sol sütun, sağ sütunun 2 katı genişliğinde olsun */
  min-width: 300px; /* Esnerken çok küçülmesin */
}
.right-column {
  flex: 1;
  position: sticky; /* Sayfa kaydırılınca sağ sütun sabit kalsın */
  top: 20px; /* Yukarıdan ne kadar boşluk bırakacağı */
  align-self: flex-start; /* Kendini yukarıya hizala */
}
.hotel-header h1 {
  margin-top: 0;
  margin-bottom: 5px;
}
.rating-box {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9em;
  color: #555;
}
.rating-score {
  background-color: #003580;
  color: white;
  padding: 5px 8px;
  font-weight: bold;
  border-radius: 5px;
}
.main-photo {
  width: 100%;
  border-radius: 10px;
  margin-top: 20px;
  object-fit: cover; /* Resmin oranını bozmadan alanı kaplamasını sağlar */
}
h2 {
  margin-top: 40px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
}
.amenities-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}
.amenities-list li {
  background-color: #f2f2f2;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 0.9em;
}
.comments-section {
  margin-top: 40px;
}
.comment-card {
  border: 1px solid #e0e0e0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}
.comment-card h3 {
  margin-top: 0;
}
.map-widget, .price-box, .address-box {
  border: 1px solid #e0e0e0;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}
.address-box {
    padding: 15px 20px;
}
.reserve-button {
  width: 100%;
  padding: 15px;
  background-color: #0071c2;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}
.reserve-button:hover {
  background-color: #005a9c;
}
.price-amount {
  font-size: 1.8em;
  font-weight: bold;
  color: #333;
}
.rating-summary {
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.rating-bars {
  margin-top: 15px;
}

.rating-bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.9em;
}

.category-name {
  width: 150px; /* Kategori isimleri için sabit genişlik */
  flex-shrink: 0;
}

.bar-container {
  flex-grow: 1;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  margin: 0 10px;
}

.bar {
  height: 100%;
  background-color: #003580; /* Koyu mavi */
  border-radius: 4px;
}

.category-score {
  font-weight: bold;
}

.comment-list {
  margin-top: 30px;
}
</style>