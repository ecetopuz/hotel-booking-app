<!-- src/components/MiniMap.vue -->
<template>
  <div class="minimap-container">
    <l-map
      ref="map"
      :center="mapCenter"
      :zoom="zoom"
      :dragging="false"
      :scrollWheelZoom="false"
      :doubleClickZoom="false"
      :touchZoom="false"
      :zoomControl="false"
      :use-global-leaflet="false"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        name="OpenStreetMap"
      ></l-tile-layer>

      <!-- Sadece marker'ları göster, popup'a gerek yok -->
      <l-marker v-for="hotel in hotels" :key="hotel.id" :lat-lng="[hotel.lat, hotel.lng]">
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import { ref, watch, onMounted, nextTick, computed } from 'vue';

export default {
  name: "MiniMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  props: {
    // Dışarıdan otel listesini alıyoruz
    hotels: {
      type: Array,
      required: true,
      default: () => []
    },
    center: { // Haritanın merkezi [lat, lng]
      type: Array,
      default: null
    },
    zoom: { // Haritanın zoom seviyesi
      type: Number,
      default: 10
    }
  },
  setup(props) {
    const map = ref(null);
    const zoom = ref(10);

    // Otellerin ortalama konumunu harita merkezi olarak hesapla
    const mapCenter = computed(() => {
      if (props.hotels.length === 0) {
        return [36.85, 28.27]; // Varsayılan merkez (Marmaris)
      }
      const avgLat = props.hotels.reduce((sum, hotel) => sum + hotel.lat, 0) / props.hotels.length;
      const avgLng = props.hotels.reduce((sum, hotel) => sum + hotel.lng, 0) / props.hotels.length;
      return [avgLat, avgLng];
    });

    const invalidateMapSize = async () => {
        await nextTick();
        if (map.value && map.value.leafletObject) {
            map.value.leafletObject.invalidateSize();
        }
    };
    
    onMounted(invalidateMapSize);
    // Oteller değiştiğinde de haritayı yenile
    watch(() => props.hotels, invalidateMapSize);

    return { map, zoom, mapCenter };
  },
};
</script>

<style scoped>
.minimap-container {
  height: 200px; /* Mini haritanın yüksekliği */
  width: 100%;
  border-radius: 8px;
  overflow: hidden; /* Kenarları yuvarlak göstermek için */
}
</style>