"""Durak listesini CSV dosyasindan okur."""

import csv
from pathlib import Path

from .model import Durak


class VeriHatasi(Exception):
    """CSV dosyasi beklenen bicimde degilse firlatilir."""


def csv_oku(yol: str | Path) -> list[Durak]:
    """`ad,enlem,boylam` sutunlu bir CSV dosyasini okur.

    Ilk satir depo (baslangic noktasi) kabul edilir.
    """
    duraklar = []
    with open(yol, encoding="utf-8", newline="") as dosya:
        okuyucu = csv.DictReader(dosya)
        eksik = {"ad", "enlem", "boylam"} - set(okuyucu.fieldnames or [])
        if eksik:
            raise VeriHatasi(f"CSV dosyasinda eksik sutunlar: {', '.join(sorted(eksik))}")

        for satir_no, satir in enumerate(okuyucu, start=2):
            try:
                enlem = float(satir["enlem"])
                boylam = float(satir["boylam"])
            except (TypeError, ValueError):
                raise VeriHatasi(f"{satir_no}. satirda gecersiz koordinat") from None
            if not (-90 <= enlem <= 90 and -180 <= boylam <= 180):
                raise VeriHatasi(f"{satir_no}. satirdaki koordinat dunya disinda")
            duraklar.append(Durak(satir["ad"].strip(), enlem, boylam))

    if len(duraklar) < 2:
        raise VeriHatasi("En az bir depo ve bir teslimat noktasi gerekli")
    return duraklar
