# SEBlog-V5

Bu proje, Türkiye haritası üzerinde görsel ve etkileşimli bir deneyim sunan bir web uygulamasıdır. Kullanıcılar, harita üzerinde çeşitli illerle ilgili bilgilere erişebilir ve görsellerle desteklenen bir arayüzde gezinebilirler.

## Özellikler
- Türkiye haritası üzerinde etkileşimli iller
- İl bilgileri ve görseller
- Modern ve duyarlı (responsive) arayüz
- Bootstrap ve jQuery tabanlı görsel efektler

## Kurulum
1. **Depoyu klonlayın:**
   ```sh
   git clone https://github.com/sinanelms/SEBlog-V5.git
   cd SEBlog-V5
   ```
2. **Gerekli Python paketlerini yükleyin:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Veritabanı dosyasını oluşturun:**
   - `instance/yer.db` dosyasını kendiniz oluşturmalı veya uygulama ilk çalıştırıldığında otomatik oluşacaktır.

## Çalıştırma
```sh
python main.py
```

Uygulama çalıştıktan sonra tarayıcınızda `http://localhost:5000` adresine giderek kullanmaya başlayabilirsiniz.

## Notlar
- `yer.db` dosyası ve diğer hassas veriler `.gitignore` dosyasına eklenmiştir ve GitHub'a yüklenmez.
- Proje, Flask veya benzeri bir Python web framework'ü ile çalışmaktadır.

## Katkı
Katkıda bulunmak için lütfen bir fork oluşturun ve pull request gönderin.

---

**Geliştirici:** sinanelms 