"""Programin kullandigi veri yapilari."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Durak:
    """Bir teslimat noktasi (veya baslangic deposu)."""

    ad: str
    enlem: float
    boylam: float
