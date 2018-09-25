import random
from datetime import datetime
from functools import wraps
from flask import Flask, flash, logging, redirect, render_template, request,session, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, PasswordField, StringField, TextAreaField, validators
from passlib.hash import sha256_crypt

# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))

    return decorated_function

# Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    password = PasswordField("Parola:",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

app = Flask(__name__,static_folder='static')
app.secret_key= "seblog"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/WeLoo/Desktop/flasktodoapp/yer.db'
db = SQLAlchemy(app)
#☺yargı bölgeleri
class yer(db.Model):
    no =        db.Column(db.Integer, primary_key=True)
    yerler =     db.Column(db.String(80))
    bolge =     db.Column(db.String(80))
    teskilati =     db.Column(db.String(80))
    acm =     db.Column(db.String(80))
    ili =     db.Column(db.String(80))
#sonuclar    
class abc(db.Model):
    no =        db.Column(db.Integer, primary_key=True)
    isim =  db.Column(db.String(80))
    yerler =     db.Column(db.String(80))
    bolge =     db.Column(db.String(80))
    teskilati =     db.Column(db.String(80))
    acm =     db.Column(db.String(80))
    ili =     db.Column(db.String(80))

#kayıt
class User(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
    
      
#son giriş
class abcd(db.Model):
    no =        db.Column(db.Integer, primary_key=True)
    isim =  db.Column(db.String(80))
    yerler =     db.Column(db.String(80))
    bolge =     db.Column(db.String(80))
    teskilati =     db.Column(db.String(80))
    acm =     db.Column(db.String(80))
    ili =     db.Column(db.String(80))
    zaman = db.Column(db.DateTime(),default=datetime.now(),nullable=True)
   
#anasayfa    
@app.route("/")
def index():
    articles = yer.query.all()
    todo = db.session.query(db.func.max(abcd.no)).scalar()
    son = abcd.query.filter_by(no = todo).first()
    

    return render_template("site.html",articles=articles,son=son)


#haritalar
@app.route("/maps")
def about():
    return render_template("maps.html")
#iletişim
@app.route("/iletisim")
def iletisim():
    return render_template("call.html")
#resimler
@app.route("/resimler")
def resim():
    return render_template("resim.html")
#sonuçları göster
@app.route("/sonuc",methods=["GET","POST"])
def sonuc():
    keyword = request.form.get("keyword")
    if request.method == "POST" and (len(keyword) >= 3):        
        isimler = keyword.split("\r")
        for isim in isimler:
            if (len(isim) >= 3) :
                a =random.randint(1,591)
                bilgileer =yer.query.filter_by(no =str(a))
                for bilgi in bilgileer:
                    yenibilgi = abc(yerler = bilgi.yerler, isim = isim, bolge = bilgi.bolge,teskilati = bilgi.teskilati,
                    acm = bilgi.acm,ili = bilgi.ili)
                    db.session.add(yenibilgi)

                    yenibilgi2 = abcd(yerler = bilgi.yerler, isim = isim, bolge = bilgi.bolge,teskilati = bilgi.teskilati,
                    acm = bilgi.acm,ili = bilgi.ili)
                    db.session.add(yenibilgi2)

                    db.session.commit()
            elif len(isim) == 1:
                continue            
            else:
                flash("Lütfen isimleri düzgün giriniz...","danger")
                return render_template("site.html")              
        bilgiler = abc.query.all()   
        db.session.query(abc).delete()
        db.session.commit()
    
        return render_template("sonuc.html",bilgiler = bilgiler)
    else:
        flash("İsim(ler) girmeyi unuttunuz...","danger")
        db.session.query(abc).delete()
        db.session.commit()
        return redirect(url_for("index"))
#bilgi
@app.route("/ekip")
@login_required
def ekip():
    articles = abcd.query.all()
    #db.session.query(abcd).delete() 
    #db.session.commit()
    return render_template("ekip2.html",articles = articles)    

#Kayıt Olma
"""
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        yenibilgi3 = User(username = username,password=password)
        db.session.add(yenibilgi3)
        db.session.commit()
        flash("Başarıyla Kayıt Oldunuz...","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)
"""
# Login İşlemi
@app.route("/login",methods =["GET","POST"])
def login():

    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data        
        hesap = User.query.filter_by(username=username).first()
        real_password = hesap.password
        if sha256_crypt.verify(password_entered,real_password):
               flash("Başarıyla Giriş Yaptınız...","success")

               session["logged_in"] = True
               session["username"] = username

               return redirect(url_for("index"))
        else:
            flash("Parolanızı Yanlış Girdiniz...","danger")
            return redirect(url_for("login")) 
    return render_template("login.html",form = form)


# Logout İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# bölgeler
@app.route("/adli")
def adli():
    articles = yer.query.all()
    return render_template("adli.html",articles = articles)

#denemealanı
@app.route("/deneme")
def deneme():
    return render_template("turkey.html")
  
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
