# Otel Rezervasyon Projesi

Bu proje, kullanıcıların otel araması yapabildiği, detaylarını görebildiği, kayıt olup giriş yapabildiği ve otelleri harita üzerinde görüntüleyebildiği tam kapsamlı bir web uygulamasıdır. Proje, Vue.js ile geliştirilmiş bir frontend ve Python/Flask ile geliştirilmiş bir backend'den oluşmaktadır.

---

## 🚀 Canlı Demo Linkleri

*   **Frontend (Kullanıcı Arayüzü):** [(https://hotel-booking-app-frontend-5wfj.onrender.com)](https://hotel-booking-app-frontend-5wfj.onrender.com)  
*   

---

## 🎥 Proje Tanıtım Videosu ve Ekran Görüntüleri

Projenin nasıl çalıştığını gösteren kısa tanıtım videosuna ve diğer materyallere aşağıdaki Google Drive linkinden ulaşabilirsiniz.

*   **Video ve Ekran Görüntüleri:** [https://drive.google.com/drive/folders/1w0u4wKIRA5yDLuEYEKmBGHwi9bbvUiGK?usp=sharing](https://drive.google.com/drive/folders/1w0u4wKIRA5yDLuEYEKmBGHwi9bbvUiGK?usp=sharing)

---

## 🛠️ Kullanılan Teknolojiler

*   **Frontend:**
    *   Vue.js 3 (Composition & Options API)
    *   Vue Router ile istemci tarafı yönlendirme
    *   Axios ile asenkron API istekleri
    *   Leaflet & @vue-leaflet/vue-leaflet (Etkileşimli haritalar için)
    *   @vuepic/vue-datepicker (Tarih seçimi için)
*   **Backend:**
    *   Python 3
    *   Flask Web Framework
    *   psycopg2 (PostgreSQL veritabanı bağlantısı için)
    *   Flask-JWT-Extended (JWT tabanlı kullanıcı yetkilendirme)
    *   Flask-Bcrypt & Werkzeug (Şifre hashleme)
*   **Veritabanı:**
    *   PostgreSQL
*   **Deploy (Canlıya Alma):**
    *   Backend & Veritabanı: **Render**
    *   Frontend: **Render**

---

## 📝 Tasarım ve Veri Modeli

### Tasarım Kararları
Projenin frontend'i, modern ve reaktif bir kullanıcı deneyimi sunmak amacıyla Vue.js 3 ile geliştirilmiştir. Bileşen tabanlı mimari, kodun daha yönetilebilir ve tekrar kullanılabilir olmasını sağlamıştır. Backend tarafında ise, Python'un sadeliği ve Flask framework'ünün minimal yapısı sayesinde hızlı ve esnek bir API sunucusu oluşturulmuştur.

### Veri Modeli
Veritabanı, PostgreSQL üzerinde ilişkisel bir yapıda tasarlanmıştır. Ana tablolar `users`, `hotels`, `rooms`, `bookings`, `comments` ve `amenities` gibi varlıklardan oluşmaktadır. Bu yapı, otellerin müsaitlik durumunu kontrol etmeye ve kullanıcı yorumlarını otellerle ilişkilendirmeye olanak tanır.

---

## 🔧 Karşılaşılan Zorluklar ve Çözümler

Bu proje geliştirilirken karşılaşılan en önemli zorluklar ve bu zorluklara bulunan çözümler aşağıda özetlenmiştir.

*   **Zorluk 1: Veritabanı Deploy ve Şema Taşıma**
    *   **Problem:** Render üzerinde boş bir veritabanı oluşturulduktan sonra, lokal geliştirme ortamındaki tablo yapısını ve test verilerini canlı ortama taşımak gerekiyordu.
    *   **Çözüm:** Bu sorun, PostgreSQL'in yerel araçları kullanılarak aşıldı. `pg_dump` komutu ile lokal veritabanının tam bir yedeği `.sql` dosyası olarak alındı. Ardından `psql` komutu ve Render'ın sağladığı "External Database URL" kullanılarak bu yedek dosya, canlı veritabanına başarıyla yüklendi. Bu yöntem, veri kaybı olmadan ve şema bütünlüğü korunarak taşıma yapılmasını sağladı.

*   **Zorluk 2: Frontend Build Hataları**
    *   **Problem:** Frontend uygulamasını Render'da deploy etmeye çalışırken, `leaflet`, `axios`, `@vuepic/vue-datepicker` gibi kütüphaneler için sürekli "Rollup failed to resolve import" hatası alındı.
    *   **Çözüm:** Sorunun temel nedeni, bu paketlerin `npm install` ile kurulmuş olmasına rağmen `package.json` dosyasına kaydedilmemiş veya yanlışlıkla `devDependencies` altına kaydedilmiş olmasıydı. Çözüm olarak, projedeki tüm `import` ifadeleri incelendi, gerekli tüm NPM paketlerinin bir listesi çıkarıldı ve `npm install <paket1> <paket2> ...` komutuyla hepsi tek seferde `dependencies` altına kaydedildi. Bu, "içindekiler listesini" eksiksiz hale getirerek build işleminin başarıyla tamamlanmasını sağladı.

*   **Zorluk 3: Canlı Ortamda API Adreslerinin Yönetimi**
    *   **Problem:** Frontend kodu, geliştirme aşamasında API isteklerini `http://localhost:5000` adresine yapıyordu. Canlıya alındığında bu adreslerin dinamik olarak değişmesi gerekiyordu.
    *   **Çözüm:** En pratik çözüm olarak, canlıya alınma aşamasında Vue bileşenleri içindeki tüm `localhost` adresleri, Render üzerinde çalışan canlı backend sunucusunun URL'i (`https://hotel-booking-app-095q.onrender.com`) ile manuel olarak güncellendi.

