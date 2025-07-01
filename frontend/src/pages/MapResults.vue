
<template>
  <div class="map-container">
    
    <router-link to="/" class="back-button">← Ana Sayfaya Geri Dön</router-link>

    <!-- Harita -->
    <l-map
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      :use-global-leaflet="false"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>

      
      <l-marker 
        v-for="hotel in hotels" 
        :key="hotel.id" 
        :lat-lng="[hotel.lat, hotel.lng]"
      >
        <l-popup>
          <b>{{ hotel.name }}</b><br>
          {{ hotel.city }}
        </l-popup>
      </l-marker>
    </l-map>

    
    <div v-if="hotels.length === 0" class="no-results-overlay">
      Haritada gösterilecek otel bulunamadı. <br>
      Lütfen anasayfadan bir arama yapın.
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import { ref, onMounted, nextTick } from 'vue'; // nextTick 
import "leaflet/dist/leaflet.css";
import { hotelStore } from '../store/hotelStore.js'; 

export default {
  name: "MapResults",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  setup() {
    const map = ref(null);
    const zoom = ref(10);
    
    const center = ref([37.0, 35.0]); 
    const hotels = ref([]); 

    onMounted(async () => {
      
      const hotelsFromStore = hotelStore.filteredHotels.filter(h => h.lat && h.lng);
      
     
      hotels.value = hotelsFromStore;

      
      await nextTick();

      if (map.value && hotels.value.length > 0) {
       
        const bounds = hotels.value.map(h => [h.lat, h.lng]);
        map.value.leafletObject.fitBounds(bounds, { padding: [50, 50] });
      } else {
        
        console.log("Store'da gösterilecek otel bulunamadı. Harita varsayılan merkezde açılıyor.");
      }
    });

    return { 
      map, 
      zoom, 
      center,
      hotels, 
    };
  },
};
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100vh;
}
.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1000;
  padding: 10px 15px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
.no-results-overlay { 
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-size: 1.5em;
    z-index: 2000;
    pointer-events: none; 
}
</style>