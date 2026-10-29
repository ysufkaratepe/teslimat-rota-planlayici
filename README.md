# Teslimat Rota Planlayıcı

![test](https://github.com/ysufkaratepe/teslimat-rota-planlayici/actions/workflows/test.yml/badge.svg)

Bir depodan çıkıp tüm teslimat noktalarına uğrayan ve depoya geri dönen **kısa bir rota** hesaplayan Python projesi.

2026 yazında Almanya'nın Worms şehrinde Amazon paketleri dağıtan bir kurye olarak çalıştım. Her gün dolu bir araç ve sıkı bir zaman planıyla çalışırken teslimatları hangi sırayla yapmam gerektiğini düşünürdüm. Bu proje, o günlük problemi bilgisayar mühendisliğinde öğrendiğim yöntemlerle çözme denemem.

<p align="center">
  <img src="docs/ornek_rota.svg" alt="En yakın komşu ve 2-opt rotalarının karşılaştırması" width="760">
</p>

*Solda en yakın komşu yöntemiyle bulunan rota, sağda 2-opt ile iyileştirilmiş hali. Birbirini kesen yollar ortadan kalkıyor ve rota yaklaşık %10 kısalıyor.*

## Problem

Bu problem bilgisayar biliminde **Gezgin Satıcı Problemi** (Traveling Salesman Problem) olarak bilinir. Durak sayısı arttıkça tüm sıralamaları denemek imkânsızlaşır: sadece 15 durak için yaklaşık 43 milyar farklı sıralama vardır. Bu yüzden proje, hızlı ve iyi sonuç veren iki sezgisel yöntem kullanır:

1. **En yakın komşu:** Her adımda henüz gidilmemiş en yakın durağa gider. Çok hızlıdır ama rota genelde en iyisinden uzundur.
2. **2-opt iyileştirmesi:** Rotadaki iki yolu seçer; bunları çapraz bağlayıp aradaki kısmı ters çevirmek rotayı kısaltıyorsa değişikliği yapar. Kazanç kalmayana kadar tekrarlanır. Bu işlem özellikle birbirini kesen yolları çözer.

Mesafeler, iki koordinat arasındaki kuş uçuşu mesafeyi veren **haversine formülü** ile hesaplanır.

## Kullanım

```bash
pip install -r requirements.txt
python -m rota ornek_veri/worms_duraklar.csv --grafik rota.png
```

Örnek çıktı:

```
13 teslimat noktasi, depo: Depo (Worms merkez)

En yakin komsu rotasi :  42.52 km
2-opt sonrasi         :  38.36 km  (9.8% daha kisa)
Hesaplama suresi      : 0.1 ms

Onerilen sira:
   1. Pfiffligheim
   2. Horchheim
   3. Wiesoppenheim
   ...
```

Kendi duraklarınızı kullanmak için `ad,enlem,boylam` sütunlu bir CSV dosyası hazırlayın. İlk satır depo, yani başlangıç noktası olarak kabul edilir.

```csv
ad,enlem,boylam
Depo,49.6320,8.3590
Herrnsheim,49.6560,8.3410
```

> Örnek veri, Worms'taki semtlerin yaklaşık merkez koordinatlarından oluşur. Gerçek teslimat adresi içermez.

## Testler

```bash
pip install -r requirements-dev.txt
pytest -v
```

Testler; mesafe hesabını (İstanbul–Ankara gibi bilinen bir mesafeyle), her durağa tam bir kez uğranıp depoya dönüldüğünü, 2-opt'un rotayı hiçbir zaman uzatmadığını ve küçük örneklerde tüm sıralamaları deneyen kaba kuvvet çözümüne en fazla %10 uzaklıkta kaldığını kontrol eder. Her yüklemede GitHub Actions ile Windows ve Linux'ta, Python 3.10 ve 3.12 üzerinde çalışır.

## Proje yapısı

```
rota/
  model.py         Durak veri yapısı
  mesafe.py        Haversine mesafesi ve mesafe matrisi
  algoritmalar.py  En yakın komşu, 2-opt ve kaba kuvvet
  veri.py          CSV okuma ve doğrulama
  gorsel.py        Matplotlib ile rota grafiği
  __main__.py      Komut satırı arayüzü
tests/
  test_rota.py
```

## Geliştirme fikirleri

- Kuş uçuşu yerine gerçek yol mesafeleri (OpenStreetMap / OSRM)
- Teslimat zaman pencereleri ("bu adrese 14:00'ten önce")
- Araç kapasitesi ve birden fazla araç (Araç Rotalama Problemi, VRP)

## Geliştirici

**Yusuf Karatepe**, Bilgisayar Mühendisliği öğrencisi
[LinkedIn](https://www.linkedin.com/in/yusuf-karatepe-0720923a1/) · [GitHub](https://github.com/ysufkaratepe)
