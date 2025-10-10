# IMenu.py
from typing import Protocol, List, Optional
from Ingrediente import Ingrediente
from Stock import Stock

class IMenu(Protocol):

    nombre: str
    ingredientes: List[Ingrediente]
    precio: float
    icono_path: Optional[str]
    cantidad: int

    def esta_disponible(self, stock: Stock) -> bool:
        ...
