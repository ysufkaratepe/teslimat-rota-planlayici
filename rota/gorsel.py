"""Rotalari grafik olarak cizer."""

import matplotlib

matplotlib.use("Agg")  # ekran olmadan dosyaya cizmek icin
import matplotlib.pyplot as plt

from .model import Durak


def _ciz(eksen, duraklar: list[Durak], rota: list[int], baslik: str, renk: str) -> None:
    xs = [duraklar[i].boylam for i in rota]
    ys = [duraklar[i].enlem for i in rota]
    eksen.plot(xs, ys, "-", color=renk, linewidth=1.8, zorder=1)
    eksen.scatter([d.boylam for d in duraklar[1:]], [d.enlem for d in duraklar[1:]],
                  s=36, color="#333333", zorder=2)
    eksen.scatter([duraklar[0].boylam], [duraklar[0].enlem], s=140, marker="s",
                  color="#e8590c", zorder=3, label="Depo")

    # Ziyaret sirasini numara olarak yaz
    for sira, i in enumerate(rota[1:-1], start=1):
        eksen.annotate(str(sira), (duraklar[i].boylam, duraklar[i].enlem), textcoords="offset points",
                       xytext=(5, 5), fontsize=8)

    eksen.set_title(baslik, fontsize=11)
    eksen.set_xticks([])
    eksen.set_yticks([])
    eksen.set_aspect("equal", adjustable="datalim")
    eksen.legend(loc="lower right", fontsize=8)


def karsilastirma_ciz(duraklar: list[Durak], ilk_rota: list[int], ilk_km: float,
                      iyi_rota: list[int], iyi_km: float, dosya_yolu: str) -> None:
    """Iyilestirme oncesi ve sonrasi rotayi yan yana cizip dosyaya kaydeder."""
    plt.rcParams["svg.fonttype"] = "none"  # SVG'de yazilar metin olarak kalsin
    fig, (sol, sag) = plt.subplots(1, 2, figsize=(10, 5))
    _ciz(sol, duraklar, ilk_rota, f"En yakin komsu: {ilk_km:.1f} km", "#868e96")
    _ciz(sag, duraklar, iyi_rota, f"2-opt sonrasi: {iyi_km:.1f} km", "#1c7ed6")
    fig.tight_layout()
    fig.savefig(dosya_yolu)
    plt.close(fig)
