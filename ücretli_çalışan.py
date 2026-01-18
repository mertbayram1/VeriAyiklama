import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # Tarih formatı için özel kütüphane

# 1. VERİYİ OKU VE TEMİZLE
df_raw = pd.read_csv('ucretli_calisan_duzgun.csv', header=None)

# Başlıkları düzelt
header_rows = df_raw.iloc[:3].replace(r'^Unnamed:.*', np.nan, regex=True)
data_rows = df_raw.iloc[3:].copy()

sector_names = header_rows.iloc[0].ffill()
series_types = header_rows.iloc[1].ffill()
measure_types = header_rows.iloc[2]

new_columns = []
for i in range(len(sector_names)):
    sec = str(sector_names[i]).split('\n')[0].replace('nan', '').strip()
    ser = str(series_types[i]).split('\n')[0].replace('nan', '').strip()
    mea = str(measure_types[i]).split('\n')[0].replace('nan', '').strip()
    if i == 0: new_columns.append("Yıl"); continue
    if i == 1: new_columns.append("Ay"); continue
    new_columns.append(f"{sec} | {ser} | {mea}".strip(' |'))

data_rows.columns = new_columns
data_rows['Yıl'] = data_rows['Yıl'].ffill()

# --- KRİTİK DÜZELTME BAŞLIYOR ---

# 1. Önce Yıl ve Ay sütunlarını Sayıya Zorla (Metinleri NaN yap)
data_rows['Yıl'] = pd.to_numeric(data_rows['Yıl'], errors='coerce')
data_rows['Ay'] = pd.to_numeric(data_rows['Ay'], errors='coerce')

# 2. Yıl veya Ay bilgisi olmayan (NaN) satırları sil (Dipnotlar burada gider)
df_clean = data_rows.dropna(subset=['Yıl', 'Ay']).copy()

# 3. Yıl ve Ay'ı Tam Sayıya (Integer) Çevir (2009.0 -> 2009)
df_clean['Yıl'] = df_clean['Yıl'].astype(int)
df_clean['Ay'] = df_clean['Ay'].astype(int)

# 4. Diğer veri sütunlarını sayıya çevir
for col in df_clean.columns:
    if col not in ['Yıl', 'Ay']:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

df_final = df_clean.fillna(0)

# 5. TARİH SÜTUNUNU OLUŞTUR VE INDEX YAP
# Format: YIL-AY-01 (Örn: 2009-1-1)
df_final['Tarih'] = pd.to_datetime(df_final['Yıl'].astype(str) + '-' + df_final['Ay'].astype(str) + '-01')
df_final = df_final.set_index('Tarih')

# Kontrol: Tarihlerin düzgün oluştuğunu teyit et
print("İlk 3 Tarih:", df_final.index[:3])
print("Son 3 Tarih:", df_final.index[-3:])

# --- GRAFİK ÇİZİMİ ---
cols = [
    'B-E - Sanayi | Takvim etkilerinden | Yıllık değişim',
    'F - İnşaat | Takvim etkilerinden | Yıllık değişim',
    'G-N - Ticaret ve hizmetler | Takvim etkilerinden | Yıllık değişim'
]

plt.figure(figsize=(14, 6))

# X Ekseni olarak 'df_final.index' (yani Tarihler) kullanılıyor
plt.plot(df_final.index, df_final[cols[0]], label='Sanayi', linewidth=2)
plt.plot(df_final.index, df_final[cols[1]], label='İnşaat', linewidth=2)
plt.plot(df_final.index, df_final[cols[2]], label='Ticaret', linewidth=2)

plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.title('Sektörlerin Yıllık Büyüme Oranları (2009-2025)', fontsize=14)
plt.ylabel('Yıllık Değişim (%)')
plt.legend()
plt.grid(True, alpha=0.3)

# Eksen Formatını Ayarla (Sadece Yılları Göster)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(1)) # Her 1 yılı göster
plt.gcf().autofmt_xdate() # Tarihleri birbirine girmesin diye eğik yaz

# Konaklama Sektörü Verileri
raw_col = 'I - Konaklama ve yiyecek hizmeti | Arındırılmamış | Ücretli çalışan sayısı'
adj_col = 'I - Konaklama ve yiyecek hizmeti | Mevsim | Ücretli çalışan sayısı'

plt.figure(figsize=(14, 6))
plt.plot(df_final.index, df_final[raw_col], label='Ham Veri (Arındırılmamış)', color='blue', alpha=0.6)
plt.plot(df_final.index, df_final[adj_col], label='Mevsim Etkisinden Arındırılmış', color='red', linewidth=2)

plt.title('Turizm Sektöründe Mevsimsellik Etkisi', fontsize=14)
plt.ylabel('Çalışan Sayısı')
plt.legend()
plt.grid(True, alpha=0.3)

# Toplam İstihdam (Mevsim Etkisinden Arındırılmış)
total_col = 'B-N - Sanayi, inşaat, ticaret ve hizmetler | Mevsim | Ücretli çalışan sayısı'

plt.figure(figsize=(14, 6))
plt.plot(df_final.index, df_final[total_col], color='darkgreen', linewidth=2)

# Kriz veya Önemli Dönemleri İşaretleyelim (Örnek: Pandemi)
plt.axvline(pd.to_datetime('2020-04-01'), color='red', linestyle='--', label='Pandemi Başlangıcı')

plt.title('Türkiye Toplam Ücretli Çalışan Sayısı Trendi', fontsize=14)
plt.ylabel('Çalışan Sayısı')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()