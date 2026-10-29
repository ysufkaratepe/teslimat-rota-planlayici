"""Komut satiri arayuzu.

Kullanim:
    python -m rota ornek_veri/worms_duraklar.csv
    python -m rota ornek_veri/worms_duraklar.csv --grafik rota.png
"""

import argparse
import sys
import time

from .algoritmalar import en_yakin_komsu, iki_opt, rota_uzunlugu
from .mesafe import mesafe_matrisi
from .veri import VeriHatasi, csv_oku


def main(argv: list[str] | None = None) -> int:
    ayristirici = argparse.ArgumentParser(
        prog="python -m rota",
        description="Teslimat duraklari icin kisa bir rota hesaplar.",
    )
    ayristirici.add_argument("csv", help="ad,enlem,boylam sutunlu CSV dosyasi (ilk satir depo)")
    ayristirici.add_argument("--grafik", help="rotayi bu dosyaya cizer (.png veya .svg)")
    args = ayristirici.parse_args(argv)

    try:
        duraklar = csv_oku(args.csv)
    except (OSError, VeriHatasi) as hata:
        print(f"Hata: {hata}", file=sys.stderr)
        return 1

    matris = mesafe_matrisi(duraklar)

    baslangic = time.perf_counter()
    ilk = en_yakin_komsu(matris)
    iyi = iki_opt(ilk, matris)
    sure_ms = (time.perf_counter() - baslangic) * 1000

    ilk_km = rota_uzunlugu(ilk, matris)
    iyi_km = rota_uzunlugu(iyi, matris)
    kazanc = (ilk_km - iyi_km) / ilk_km * 100 if ilk_km else 0.0

    print(f"{len(duraklar) - 1} teslimat noktasi, depo: {duraklar[0].ad}\n")
    print(f"En yakin komsu rotasi : {ilk_km:6.2f} km")
    print(f"2-opt sonrasi         : {iyi_km:6.2f} km  ({kazanc:.1f}% daha kisa)")
    print(f"Hesaplama suresi      : {sure_ms:.1f} ms\n")

    print("Onerilen sira:")
    for sira, i in enumerate(iyi[1:-1], start=1):
        print(f"  {sira:2d}. {duraklar[i].ad}")
    print(f"  -> {duraklar[0].ad} (donus)")

    if args.grafik:
        from .gorsel import karsilastirma_ciz

        karsilastirma_ciz(duraklar, ilk, ilk_km, iyi, iyi_km, args.grafik)
        print(f"\nGrafik kaydedildi: {args.grafik}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
