import random

import pytest

from rota.__main__ import main
from rota.algoritmalar import en_yakin_komsu, iki_opt, kaba_kuvvet, rota_uzunlugu
from rota.mesafe import haversine_km, mesafe_matrisi
from rota.model import Durak
from rota.veri import VeriHatasi, csv_oku


def rastgele_duraklar(n, tohum):
    r = random.Random(tohum)
    return [Durak(f"D{i}", 49.6 + r.random() * 0.1, 8.3 + r.random() * 0.1) for i in range(n)]


def test_ayni_noktanin_mesafesi_sifir():
    d = Durak("A", 49.63, 8.36)
    assert haversine_km(d, d) == 0


def test_bilinen_mesafe():
    # Istanbul - Ankara kus ucusu yaklasik 350 km
    istanbul = Durak("Istanbul", 41.0082, 28.9784)
    ankara = Durak("Ankara", 39.9334, 32.8597)
    assert haversine_km(istanbul, ankara) == pytest.approx(350, abs=5)


def test_matris_simetrik():
    m = mesafe_matrisi(rastgele_duraklar(6, 1))
    for i in range(6):
        assert m[i][i] == 0
        for j in range(6):
            assert m[i][j] == m[j][i]


def test_rota_her_duraga_bir_kez_ugrar_ve_depoya_doner():
    m = mesafe_matrisi(rastgele_duraklar(10, 2))
    for rota in (en_yakin_komsu(m), iki_opt(en_yakin_komsu(m), m)):
        assert rota[0] == 0 and rota[-1] == 0
        assert sorted(rota[1:-1]) == list(range(1, 10))


def test_iki_opt_rotayi_uzatmaz():
    for tohum in range(20):
        m = mesafe_matrisi(rastgele_duraklar(12, tohum))
        ilk = en_yakin_komsu(m)
        assert rota_uzunlugu(iki_opt(ilk, m), m) <= rota_uzunlugu(ilk, m) + 1e-9


def test_iki_opt_kucuk_orneklerde_en_iyiye_yakin():
    for tohum in range(10):
        m = mesafe_matrisi(rastgele_duraklar(8, tohum))
        en_iyi = rota_uzunlugu(kaba_kuvvet(m), m)
        bulunan = rota_uzunlugu(iki_opt(en_yakin_komsu(m), m), m)
        assert bulunan <= en_iyi * 1.10  # en fazla %10 uzun


def test_tek_teslimat_noktasi():
    m = mesafe_matrisi(rastgele_duraklar(2, 3))
    assert iki_opt(en_yakin_komsu(m), m) == [0, 1, 0]


def test_ornek_csv_okunur():
    duraklar = csv_oku("ornek_veri/worms_duraklar.csv")
    assert len(duraklar) == 14
    assert duraklar[0].ad.startswith("Depo")


def test_eksik_sutun_hata_verir(tmp_path):
    dosya = tmp_path / "bozuk.csv"
    dosya.write_text("ad,enlem\nDepo,49.6\n", encoding="utf-8")
    with pytest.raises(VeriHatasi):
        csv_oku(dosya)


def test_gecersiz_koordinat_hata_verir(tmp_path):
    dosya = tmp_path / "bozuk.csv"
    dosya.write_text("ad,enlem,boylam\nDepo,49.6,8.3\nA,abc,8.3\n", encoding="utf-8")
    with pytest.raises(VeriHatasi):
        csv_oku(dosya)


def test_komut_satiri_calisir(capsys, tmp_path):
    grafik = tmp_path / "rota.png"
    assert main(["ornek_veri/worms_duraklar.csv", "--grafik", str(grafik)]) == 0
    cikti = capsys.readouterr().out
    assert "2-opt sonrasi" in cikti
    assert grafik.exists() and grafik.stat().st_size > 0


def test_olmayan_dosya_hata_kodu_dondurur():
    assert main(["olmayan.csv"]) == 1
