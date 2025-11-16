# Ball Physics Simulator 🎱

Harika ve modern bir top fiziği simülatörüne hoş geldiniz! (Başlık: "Benim fiziğim Newton'u bile şok eder!")

## Özellikler
- Farklı boy, renk ve hızda dinamik toplar
- Çarpışma açık/kapalı modu
- Tüm topları sıfırlama, topları manuel veya rastgele ekleme/çıkarma
- Göz alıcı modern arayüz, koyu tema
- Animasyon hızı kontrolü (yavaş/boost)
- Akıllı buton test otomasyonu (tester.py)
- Hız/obje durumu her an görünür

## Kurulum

Python 3.8+ yüklü olmalı (standart tkinter ile uyumlu)

```bash
pip install tk
```
veya genellikle Python ile birlikte gelir.

## Kullanım

### 1. Normal Kullanıcı Arayüzü

```bash
python game.py
```
Arayüz açılır, topları ekle, boyut/rengini seç ve tüm özellikleri keyfine göre dene!
- **Top Boyutu** seç, ardından **Top Rengi** seç, otomatik top eklenir
- 🎲 **10x RANDOM**: Rastgele 10 top ekler
- ⏪/⚡ **SLOW/BOOST**: Hız çarpanını değiştirir
- ⟳ **RESET**: Ekranı ve hızı sıfırlar
- 🗑 **DELETE**: Son eklenen topu siler
- 💥 **ÇARPIŞMA**: Çarpışma açık/kapalı
- 🖵 **TAM EKRAN**: Tam ekran moduna geçer/çıkılır

### 2. Otomatik Testçi Modu (Gizli BT Sihirbazları ve Geliştiricilere)
Ekrandaki butonları koddan, canlı bir şekilde sırayla, animasyonlu olarak test eder.

```
python tester.py
```
- GUI açılır, otomatik top ekleme-hızlandırma-vs. testleri canlı yapılır.
- İşlemler ekrana animasyonlu yansır, test bitince pencereyi serbestçe kullanabilirsin.

## Bağımlılıklar
- Sadece standart Python kütüphaneleri (`tkinter`, `math`, `random`, `time`) yeterli!

## Ekran
- Üstte obje-adet ve hız gösterir
- Boyut/seçim görselliği modernleştirilmiş
- Tüm butonlar büyük, renkli, modern ve mouse-ile eğlencelik

---
Bugsız yazdık, ama yine de bir şey patlarsa: TAHTAYA VUR! 🤞

Keyifli top fiziği oyunları dileriz!

---
Yazan: AI + SEN
