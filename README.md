# 🇹🇷 Türkiye Sektörel İstihdam Analizi (2009-2025)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=matplotlib&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

Bu proje, TÜİK tarafından sağlanan ham ve karmaşık yapıdaki **ücretli çalışan istatistiklerini** temizleyerek analiz edilebilir bir zaman serisine dönüştürür. Özellikle pandemi etkisi, sektörlerin büyüme hızları ve turizmdeki mevsimsellik üzerine odaklanır.

---

## ⚡ Temel Özellikler

Bu repo üç ana problemi çözer:

* 🧹 **Gelişmiş Veri Temizleme:** 3 satıra yayılmış (multi-row) bozuk başlıkları ve dipnotları temizleyip tekil bir `DateTime` indeksine dönüştürür.
* 📈 **Sektörel Kıyaslama:** Sanayi, İnşaat ve Ticaret sektörlerinin yıllık performansını karşılaştırır.
* 🔍 **Mevsimsellik Analizi:** Turizm sektöründeki *Ham Veri* vs *Arındırılmış Veri* farkını görselleştirir.

---

## 🛠️ Teknik Detaylar

Projenin en kritik kısmı, analizden ziyade veriyi analize hazır hale getirmektir:

| Sorun | Çözüm Yöntemi |
| :--- | :--- |
| **Karmaşık Başlıklar** | İlk 3 satır `ffill()` ile doldurulup birleştirildi. |
| **Bozuk Tarihler** | Yıl ve Ay sütunları birleştirilip `pd.to_datetime` ile indekslendi. |
| **Eksik Veriler** | Dipnot kaynaklı `NaN` satırları temizlendi, tipler `int/float`'a zorlandı. |

---

## 📊 Çıktılar

Kod çalıştırıldığında 3 temel görsel üretir:

1.  🏭 **Sektör Büyüme Oranları:** Ekonomik dalgalanmaların sektörlere etkisi.
2.  🏖️ **Turizm & Mevsimsellik:** Yaz sezonunun istihdama net etkisi.
3.  📉 **Genel Trend & Krizler:** Nisan 2020 (Pandemi) kırılımı ve toparlanma süreci.

---

## 🚀 Hızlı Başlangıç

```bash
# 1. Repoyu klonla
git clone [https://github.com/mertbayram1/sektorel-istihdam-analizi.git](https://github.com/mertbayram1/sektorel-istihdam-analizi.git)

# 2. Klasöre gir
cd sektorel-istihdam-analizi

# 3. Gereksinimleri kur
pip install pandas numpy matplotlib

# 4. Çalıştır
python main.py
