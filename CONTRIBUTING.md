# Katkıda bulunma

Hata bildirmek veya özellik önermek için [Issues](https://github.com/SenseiTuna/TCDD-Koltuk-Bulucu/issues) bölümünü kullanabilirsin. Hata bildiriminde tarayıcı sürümünü, eklenti sürümünü, hatayı yeniden oluşturma adımlarını ve beklediğin davranışı belirt.

Ekran görüntülerinden ad, kimlik, iletişim, PNR ve ödeme bilgilerini gizle.

Kod katkısı için repoyu fork'la, değişikliği ayrı bir dalda hazırla ve pull request aç. Test ederken mümkün olduğunda yerel örnek sayfa kullan.

Göndermeden önce `node --check script.js` ve `python tools/package_extension.py` komutlarını çalıştır. Çalışma dosyaları değişirse paketleme betiğinin dosya listesini de güncelle. Oluşturulan `dist/` klasörünü kaynak koduna ekleme; ZIP ve SHA-256 dosyasını release'e ekle.
