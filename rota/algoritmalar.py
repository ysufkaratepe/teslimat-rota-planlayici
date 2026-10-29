"""Rota bulma algoritmalari.

Bir depodan cikip butun duraklara ugrayan ve depoya geri donen en kisa rotayi
bulmak "Gezgin Satici Problemi"dir (Traveling Salesman Problem, TSP). Durak
sayisi arttikca butun ihtimalleri denemek imkansizlasir: 15 durak icin bile
yaklasik 43 milyar farkli sira vardir. Bu yuzden pratikte iyi ama hizli
sezgisel yontemler kullanilir:

1. En yakin komsu: her adimda en yakin, henuz gidilmemis duraga git.
   Cok hizlidir ama sonuc genelde en iyiden %15-25 uzundur.
2. 2-opt: mevcut rotada kesisen iki yolu "cozerek" rotayi kisaltir.
   Artik iyilesme bulamayana kadar tekrarlanir.

Rotalar, mesafe matrisindeki indekslerin listesi olarak tutulur. Indeks 0
her zaman depodur; rota depoda baslar ve depoda biter: [0, 3, 1, 2, 0]
"""

from itertools import permutations

Matris = list[list[float]]


def rota_uzunlugu(rota: list[int], matris: Matris) -> float:
    """Rotadaki ardisik duraklar arasi mesafelerin toplami."""
    return sum(matris[rota[i]][rota[i + 1]] for i in range(len(rota) - 1))


def en_yakin_komsu(matris: Matris, baslangic: int = 0) -> list[int]:
    """En yakin komsu sezgiseli ile bir baslangic rotasi olusturur."""
    n = len(matris)
    gidilmemis = set(range(n)) - {baslangic}
    rota = [baslangic]

    while gidilmemis:
        su_an = rota[-1]
        en_yakin = min(gidilmemis, key=lambda j: matris[su_an][j])
        rota.append(en_yakin)
        gidilmemis.remove(en_yakin)

    rota.append(baslangic)  # depoya geri don
    return rota


def iki_opt(rota: list[int], matris: Matris) -> list[int]:
    """2-opt ile rotayi iyilestirir.

    Rotadan iki kenar secilir: (a -> b) ve (c -> d). Bunlar (a -> c) ve
    (b -> d) ile degistirilip aradaki kisim ters cevrildiginde rota kisaliyorsa
    degisiklik yapilir. Hicbir degisiklik kazanc saglamayana kadar devam edilir.
    """
    rota = list(rota)
    iyilesti = True

    while iyilesti:
        iyilesti = False
        for i in range(1, len(rota) - 2):
            for j in range(i + 1, len(rota) - 1):
                a, b = rota[i - 1], rota[i]
                c, d = rota[j], rota[j + 1]
                eski = matris[a][b] + matris[c][d]
                yeni = matris[a][c] + matris[b][d]
                if yeni < eski - 1e-9:
                    rota[i : j + 1] = reversed(rota[i : j + 1])
                    iyilesti = True

    return rota


def kaba_kuvvet(matris: Matris, baslangic: int = 0) -> list[int]:
    """Butun siralamalari deneyerek kesin en kisa rotayi bulur.

    Sadece kucuk durak sayilari (yaklasik 9'a kadar) icin uygundur. Testlerde
    diger algoritmalarin sonucunu karsilastirmak icin kullanilir.
    """
    diger = [i for i in range(len(matris)) if i != baslangic]
    en_iyi, en_iyi_uzunluk = None, float("inf")
    for sira in permutations(diger):
        rota = [baslangic, *sira, baslangic]
        uzunluk = rota_uzunlugu(rota, matris)
        if uzunluk < en_iyi_uzunluk:
            en_iyi, en_iyi_uzunluk = rota, uzunluk
    return en_iyi if en_iyi is not None else [baslangic, baslangic]
