
<template>
  <div class="home-container">
    <header class="header">
      <img src="/logo.png" alt="Hotels.com Logo" class="logo" />
      <span v-if="isLoggedIn">Merhaba, {{ userName }}</span>
      <router-link to="/login" v-else>Giriş yap</router-link>
    </header>

    <div class="search-bar">
      <!-- Arama çubuğu  -->
      <input v-model="destination" placeholder="Nereye?" />
      <Datepicker v-model="dates" range :enable-time-picker="false" auto-apply locale="tr" :format="formatDateForPicker">
        <template #trigger>
          <div class="custom-date-input">
            <span class="icon">🗓️</span>
            <div class="text"><span class="label">Tarihler</span><span class="date-text">{{ formattedDateDisplay }}</span></div>
          </div>
        </template>
      </Datepicker>
      <select v-model="guestCount">
        <option value="4"> 4 misafir, 2 oda</option>
        <option value="3"> 3 misafir, 1 oda</option>
        <option value="2">2 misafir, 1 oda</option>
        <option value="1">1 misafir, 1 oda</option>
      </select>
      <button @click="searchHotels">Ara</button>
    </div>
      
    <div class="page-layout">
      <aside class="sidebar">
        <div class="map-widget">
          <mini-map :hotels="hotels" />
          <button class="map-link-button" @click="showOnMap">Haritada göster</button>
        </div>
      </aside>

      <main class="main-content">
        
        <div v-if="hotels.length > 0" class="hotel-list">
          <router-link v-for="hotel in hotels" :key="hotel.id" :to="`/hotel/${hotel.id}`" class="hotel-card-link">
            <div class="hotel-card">
              <img :src="hotel.photo" alt="Otel Fotoğrafı" class="hotel-image-placeholder" />
              <div class="hotel-info">
                <h2>{{ hotel.name }}</h2>
                <p class="hotel-location">📍 {{ hotel.city }}, {{ hotel.country }}</p>
                <p>{{ hotel.rating }} ⭐ ({{ hotel.commentsCount || hotel.comments }} yorum)</p>
                
                
<div class="price-section">
  
  <div v-if="hotel.specialDiscountRate" class="discount-badge">
    %{{ hotel.specialDiscountRate }} indirim
  </div>

  <div class="price-display">
    
    <div>
      
      <p v-if="hotel.specialDiscountRate" class="original-price">
        <s>{{ formatPrice(hotel.price) }}</s>
      </p>
     
      <p class="standard-price">{{ formatPrice(calculateDiscountedPrice(hotel)) }}</p>
    </div>
    
  </div>

 
  <div v-if="isLoggedIn && hotel.memberPrice" class="member-price-highlight-section">
    <div class="member-benefit-tag">
      <span>💎 Üye Fiyatından yararlanılabilir</span>
    </div>
    <p class="member-price-value">
      Üye Fiyatı : {{ formatPrice(hotel.memberPrice) }}
    </p>
  </div>

 
  <div v-if="!isLoggedIn && hotel.memberPrice" class="login-prompt-section">
    <p class="login-for-member-price">
      Üye fiyatını görmek için <router-link to="/login" @click.stop>giriş yapın</router-link>
    </p>
  </div>
</div>
              </div>   
            </div>     
          </router-link> 
        </div> 

        
        <div v-else>
          <p>Arama sonucu otel bulunamadı.</p>
        </div>
      </main>
    </div>
  </div>
</template>


<script>
import '../assets/Home.css';
import axios from 'axios';
import MiniMap from '../components/MiniMap.vue';
import { hotelStore } from '../store/hotelStore.js';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

export default {
  name: 'Home',
  components: {
    MiniMap,
    Datepicker, 
    
  },
   props: {
    isLoggedIn: {
      type: Boolean,
      default: false
    },
    userName: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      destination: '',
      guestCount: 2,
      hotels: [],
      dates: null, 
    };
  },
  computed: {
    
    formattedDateDisplay() {
      if (!this.dates || this.dates.length < 2) {
        return 'Tarih aralığı seçin';
      }
      const options = { day: 'numeric', month: 'short' };
      const startDate = this.dates[0].toLocaleDateString('tr-TR', options);
      const endDate = this.dates[1].toLocaleDateString('tr-TR', options);
      return `${startDate} - ${endDate}`;
    }
    
  },
  
  mounted() {
    this.searchHotels();
    
    const startDate = new Date();
    const endDate = new Date(new Date().setDate(startDate.getDate() + 1));
    this.dates = [startDate, endDate];
  },
  methods: {
    async searchHotels() {
  try {
    const apiUrl = 'http://localhost:5000/api/hotels';

    const params = {
      guests: this.guestCount,
      
    };

     if (this.destination && this.destination.trim() !== '') {
      params.destination = this.destination; 
    }

    if (this.dates && this.dates[0] && this.dates[1]) {
      params.start_date = this.dates[0].toISOString().split('T')[0];
      params.end_date = this.dates[1].toISOString().split('T')[0];
    }

   
    console.log("---------------------------");
    console.log("API İsteği Gönderiliyor...");
    console.log("URL:", apiUrl);
    console.log("Gönderilen Parametreler:", params);
   

    const response = await axios.get(apiUrl, { params: params });
    
    console.log("API'den Gelen Cevap:", response.data);
    this.hotels = response.data;
    hotelStore.filteredHotels = response.data;
  } catch (error) {
    console.error('Oteller alınırken bir hata oluştu:', error);
    this.hotels = [];
    hotelStore.filteredHotels = [];
  }
},
    formatPrice(price) {
      return price.toLocaleString('tr-TR') + ' TL';
    },
    calculateDiscountedPrice(hotel) {
    
    if (!hotel.specialDiscountRate || hotel.specialDiscountRate <= 0) {
      return hotel.price;
    }
    
    
    const discountMultiplier = hotel.specialDiscountRate / 100;
    
    
    const discountedPrice = hotel.price * (1 - discountMultiplier);
    
    return discountedPrice;
  },
    showOnMap() {
      this.$router.push('/map');
    },
    getImageUrl(hotelId) {
      return `https://via.placeholder.com/200x150.png?text=Otel+Resmi`;
    },
    
    formatDateForPicker(dates) {
       if (!dates || dates.length < 2) {
        return '';
      }
      const options = { day: 'numeric', month: 'short' };
      const startDate = dates[0].toLocaleDateString('tr-TR', options);
      const endDate = dates[1].toLocaleDateString('tr-TR', options);
      return `${startDate} - ${endDate}`;
    }
    
  },
};
</script>