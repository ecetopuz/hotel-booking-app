import { reactive } from 'vue';

// Uygulamanın her yerinden erişilebilecek reaktif bir nesne oluşturuyoruz.
export const hotelStore = reactive({
  // Başlangıçta boş bir otel listesi
  filteredHotels: [],
});