from flask import Flask, render_template, request, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__,static_folder='static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key= "seblog"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yer.db'
db = SQLAlchemy(app)

# Veritabanı tablosunu oluştur
def create_tables():
    try:
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS abcd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT,
                yerler TEXT,
                bolge TEXT,
                ili TEXT,
                teskilati TEXT,
                acm TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        db.session.commit()
        # print("Debug - abcd tablosu oluşturuldu veya zaten mevcut")
    except Exception as e:
        print(f"Debug - Tablo oluşturma hatası: {e}")

# Uygulama başladığında tabloları oluştur
with app.app_context():
    create_tables()

#anasayfa
@app.route("/")
def index():
    # Veritabanından abcd tablosundaki toplam satır sayısını al
    try:
        # Eğer veritabanı bağlantısı varsa abcd tablosundaki satır sayısını al
        result = db.session.execute(text("SELECT COUNT(*) as count FROM abcd"))
        count = result.fetchone()[0]
        son = {"no": count}
        # print(f"Debug - abcd tablosundaki satır sayısı: {count}")
        # print(f"Debug - son değişkeni: {son}")
        
    except Exception as e:
        # Veritabanı bağlantısı yoksa varsayılan değer
        # print(f"Debug - Hata oluştu: {e}")
        son = {"no": 0}
    
    # print(f"Debug - Template'e gönderilen son: {son}")
    return render_template("site.html", son=son)

# POST isteği için route - sonuçları veritabanına kaydetmek için
@app.route("/", methods=['POST'])
def save_result():
    try:
        data = request.get_json()
        if data and len(data) >= 6:
            # Veritabanına kaydet
            db.session.execute(text("""
                INSERT INTO abcd (isim, yerler, bolge, ili, teskilati, acm) 
                VALUES (:isim, :yerler, :bolge, :ili, :teskilati, :acm)
            """), {
                'isim': data[0],
                'yerler': data[1], 
                'bolge': data[2],
                'ili': data[3],
                'teskilati': data[4],
                'acm': data[5]
            })
            db.session.commit()
            # print(f"Debug - Veri kaydedildi: {data}")
            return jsonify({"success": True, "message": "Veri başarıyla kaydedildi"})
        else:
            return jsonify({"success": False, "error": "Geçersiz veri formatı"})
    except Exception as e:
        # print(f"Debug - Veri kaydetme hatası: {e}")
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})



if __name__ == "__main__":
    app.run(debug=True)