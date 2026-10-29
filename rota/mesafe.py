"""Iki konum arasindaki mesafeyi hesaplayan fonksiyonlar."""

import math

from .model import Durak

DUNYA_YARICAPI_KM = 6371.0


def haversine_km(a: Durak, b: Durak) -> float:
    """Iki durak arasindaki kus ucusu mesafeyi kilometre olarak dondurur.

    Dunya'yi kure kabul eden haversine formulu kullanilir. Sehir ici
    mesafelerde hata payi cok kucuktur.
    """
    enlem1, boylam1 = math.radians(a.enlem), math.radians(a.boylam)
    enlem2, boylam2 = math.radians(b.enlem), math.radians(b.boylam)

    d_enlem = enlem2 - enlem1
    d_boylam = boylam2 - boylam1

    h = math.sin(d_enlem / 2) ** 2 + math.cos(enlem1) * math.cos(enlem2) * math.sin(d_boylam / 2) ** 2
    return 2 * DUNYA_YARICAPI_KM * math.asin(math.sqrt(h))


def mesafe_matrisi(duraklar: list[Durak]) -> list[list[float]]:
    """Her durak cifti arasindaki mesafeyi bir kez hesaplayip tabloya yazar.

    Algoritmalar ayni mesafeyi defalarca kullandigi icin onceden hesaplamak
    programi hizlandirir.
    """
    n = len(duraklar)
    matris = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine_km(duraklar[i], duraklar[j])
            matris[i][j] = d
            matris[j][i] = d
    return matris
