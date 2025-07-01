
# --- 1. GEREKLİ KÜTÜPHANELER ---
import os
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import psycopg2
from flask_jwt_extended import create_access_token, JWTManager
from datetime import date, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import requests 
# --- 2. UYGULAMA KURULUMU VE YAPILANDIRMASI ---

app = Flask(__name__)


CORS(app) 


app.config["JWT_SECRET_KEY"] = "bu-jwt-icin-kullanilan-gizli-anahtar" 
app.config['UPLOAD_FOLDER'] = 'uploads'


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- 3. EKLENTİLERİ  ---

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# --- 4. VERİTABANI  ---
#
#conn = psycopg2.connect(
#    dbname="hotel_booking",        
#    user="postgres",               
#    password="12345",              
#    host="localhost",              
#    port="5432"                    
#)
DATABASE_URL = os.environ.get("DATABASE_URL","postgresql://postgres:12345@localhost:5432/hotel_booking")   
conn = psycopg2.connect(DATABASE_URL)
# --- 5. YARDIMCI FONKSİYONLAR ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# --- API ENDPOINTS ---

@app.route("/api/hotels")
def get_hotels():
    try:
        
        destination_query = request.args.get('destination')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        guests_str = request.args.get('guests')

        
        
        is_search_request = bool(start_date_str and end_date_str and guests_str)

        cur = conn.cursor()

        if is_search_request:
            # --- FİLTRELİ ARAMA  ---
            try:
                guests = int(guests_str)
            except (ValueError, TypeError):
                guests = 1

            base_query = """
                SELECT DISTINCT 
                    h.id, h.name, h.city, h.country, h.price, h.rating, h.comments, 
                    h.member_price, h.latitude, h.longitude, h.hotel_image_url, 
                    h.special_discount_rate
                FROM hotels h
                JOIN rooms r ON h.id = r.hotel_id
                WHERE
                    r.capacity >= %s
                    AND r.id NOT IN (
                        SELECT b.room_id FROM bookings b
                        WHERE DATERANGE(b.check_in, b.check_out, '[]') && DATERANGE(%s::date, %s::date, '[]')
                    )
            """
            params = [guests, start_date_str, end_date_str]

            if destination_query:
                base_query += " AND (h.city ILIKE %s OR h.country ILIKE %s)"
                search_term = f"%{destination_query}%"
                params.extend([search_term, search_term])
            
            base_query += " ORDER BY h.rating DESC"
            cur.execute(base_query, tuple(params))

        else:
            # --- ANASAYFA  ---
            # filtresiz, en yüksek puanlı otelleri listele
            cur.execute("""
                SELECT id, name, city, country, price, rating, comments, 
                       member_price, latitude, longitude, hotel_image_url, 
                       special_discount_rate
                FROM hotels
                ORDER BY rating DESC
                LIMIT 20
            """)

        
        rows = cur.fetchall()
        cur.close()

        hotels_list = []
        for row in rows:
            
            hotels_list.append({
                "id": row[0], "name": row[1], "city": row[2], "country": row[3],
                "price": float(row[4]) if row[4] is not None else 0.0,
                "rating": float(row[5]) if row[5] is not None else 0.0,
                "commentsCount": row[6], "memberPrice": float(row[7]) if row[7] is not None else None,
                "lat": float(row[8]) if row[8] is not None else 0.0, "lng": float(row[9]) if row[9] is not None else 0.0,
                "photo": row[10], "specialDiscountRate": row[11] if row[11] is not None else None
            })
            
        return jsonify(hotels_list)

    except psycopg2.Error as db_error:
        # Veritabanı ile ilgili bir hata olursa...
        error_trace = traceback.format_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! /api/hotels VERİTABANI HATASI !!!")
        print(f"!!! HATA MESAJI: {db_error}")
        print("!!! TRACEBACK:")
        print(error_trace)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if conn: conn.rollback()
        return jsonify({"error": "Veritabanı ile ilgili bir sorun oluştu. Detaylar loglandı."}), 500
        
    except Exception as e:
        # Veritabanı dışındaki genel bir Python hatası olursa...
        error_trace = traceback.format_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! /api/hotels GENEL HATA !!!")
        print(f"!!! HATA MESAJI: {e}")
        print("!!! TRACEBACK:")
        print(error_trace)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if conn: conn.rollback()
        return jsonify({"error": "Sunucuda beklenmedik bir hata oluştu. Detaylar loglandı."}), 500

@app.route("/api/init-hotels")
def insert_hotels():
    hotels = [
        {"name": "Elite World Marmaris", "price": 13357, "rating": 8.8, "comments": 261, "member_price": 12000, "lat": 36.8532, "lng": 28.2396, "city": "Marmaris", "country": "Türkiye"},
        {"name": "D Maris Bay", "price": 16000, "rating": 8.7, "comments": 140, "member_price": None, "lat": 36.7584, "lng": 28.0645, "city": "Marmaris", "country": "Türkiye"},
        {"name": "Blue Waters Resort", "price": 11200, "rating": 8.5, "comments": 98, "member_price": 10500, "lat": 36.8451, "lng": 28.2720, "city": "Marmaris", "country": "Türkiye"},
        {"name": "Grand Yazıcı Club Turban", "price": 6965, "rating": 8.2, "comments": 450, "member_price": None, "lat": 36.8377, "lng": 28.2312, "city": "Marmaris", "country": "Türkiye"},
        {"name": "Cook's Club Adakoy", "price": 5804, "rating": 9.1, "comments": 155, "member_price": None, "lat": 36.8285, "lng": 28.3241, "city": "Marmaris", "country": "Türkiye"}
    ]
    try:
        cur = conn.cursor()
        for hotel in hotels:
            
            cur.execute("""
                INSERT INTO hotels (name, city, country, price, rating, comments, member_price, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING
            """, (
                hotel["name"], hotel["city"], hotel["country"], hotel["price"], hotel["rating"],
                hotel["comments"], hotel["member_price"], hotel["lat"], hotel["lng"]
            ))
        conn.commit()
        cur.close()
        return jsonify({"message": "Oteller başarıyla veritabanına eklendi."})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    



@app.route('/api/register', methods=['POST'])
def register():
    try:
        
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')
        photo_file = request.files.get('photo')

        
        if not all([name, surname, email, password, country, city]):
            return jsonify({"error": "Tüm zorunlu alanlar doldurulmalıdır."}), 400

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(not char.isalnum() for char in password):
            return jsonify({"error": "Şifre kurallara uymuyor."}), 400

        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            return jsonify({"error": "Bu e-posta adresi zaten kayıtlı."}), 409

        hashed_password = generate_password_hash(password)
        
        
        photo_url_to_db = None
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo_file.save(file_path)
            
            photo_url_to_db = f"/uploads/{filename}" 

        
        full_name = f"{name} {surname}"
        
        
        cur.execute(
            """
            INSERT INTO users (name, email, password_hash, country, city, photo_url)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """,
            
            (full_name, email, hashed_password, country, city, photo_url_to_db)
        )
        new_user_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()

        display_name = name 
        access_token = create_access_token(
        identity=new_user_id,  
        additional_claims={'name': display_name} 
)
        
        return jsonify({
            "message": "Kayıt başarılı ve giriş yapıldı!",
            "access_token": access_token
        }), 201

    except Exception as e:
        if conn: conn.rollback()
        print(f"Kayıt sırasında hata: {e}")
        return jsonify({"error": "Sunucuda bir hata oluştu."}), 500
# 2. KULLANICI GİRİŞİ 
@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "E-posta ve şifre gereklidir."}), 400

    try:
        cur = conn.cursor()
        
        cur.execute("SELECT id, password_hash, name FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            
            user_id = user[0]
            full_name = user[2]
            display_name = full_name.split(' ')[0]
            
            
             
            
            access_token = create_access_token(
                identity=user_id, 
                additional_claims={'name': display_name}
            )
            return jsonify(access_token=access_token)
        else:
            return jsonify({"error": "Geçersiz e-posta veya şifre."}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/api/hotel/<int:hotel_id>")
def get_hotel_details(hotel_id):
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, name, rating, price, country, city, latitude, longitude,
                   comments, member_price, hotel_image_url, special_discount_rate 
            FROM hotels WHERE id = %s
        """, (hotel_id,))
        hotel_row = cur.fetchone()

        if not hotel_row:
            cur.close()
            return jsonify({"error": "Otel bulunamadı."}), 404

        original_price = float(hotel_row[3]) if hotel_row[3] is not None else 0.0
        special_rate = hotel_row[11]
        public_price = original_price
        if special_rate is not None and special_rate > 0:
            public_price = original_price * (1 - float(special_rate) / 100)

        hotel_details = {
            "id": hotel_row[0], "name": hotel_row[1], "rating": float(hotel_row[2]), 
            "price": original_price,
            "publicPrice": round(public_price, 2),
            "country": hotel_row[4], "city": hotel_row[5],
            "lat": float(hotel_row[6]), "lng": float(hotel_row[7]),
            "commentsCount": hotel_row[8],
            "memberPrice": float(hotel_row[9]) if hotel_row[9] is not None else None,
            "photo": hotel_row[10], "specialDiscountRate": special_rate
        }
        
       
        
        # 2. Yorumları ve Puan Dağılımını Çek ve `hotel_details` objesine ekle
        cur.execute("""
            SELECT u.name, c.rating, c.comment_title, c.comment, c.created_at, c.service_type
            FROM comments c JOIN users u ON c.user_id = u.id
            WHERE c.hotel_id = %s ORDER BY c.created_at DESC
        """, (hotel_id,))
        
        comments_data = cur.fetchall()
        
        hotel_details["comments"] = []
        hotel_details["ratingDistribution"] = []
        category_ratings = {}

        for row in comments_data:
            
            hotel_details["comments"].append({
                "author": row[0], "rating": float(row[1]), "title": row[2], 
                "text": row[3], "date": row[4].isoformat()
            })
            
            category = row[5]
            rating = float(row[1])
            if category:
                if category not in category_ratings:
                    category_ratings[category] = []
                category_ratings[category].append(rating)

        
        for category, ratings in category_ratings.items():
            average_rating = sum(ratings) / len(ratings)
            hotel_details["ratingDistribution"].append({
                "category": category, "score": round(average_rating, 1)
            })

        
        cur.execute("""
            SELECT a.name, a.icon_name FROM hotel_amenities ha
            JOIN amenities a ON ha.amenity_id = a.id
            WHERE ha.hotel_id = %s
        """, (hotel_id,))
        
        hotel_details["amenities"] = [{"name": row[0], "icon": row[1]} for row in cur.fetchall()]
        cur.close()
        return jsonify(hotel_details)

    except Exception as e:
        if conn: conn.rollback()
        print(f"Otel detayı alınırken hata: {e}")
        return jsonify({"error": "Sunucu hatası: " + str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


    