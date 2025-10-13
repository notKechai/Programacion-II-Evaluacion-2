# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

def get_default_menus() -> List[IMenu]:
    return [
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa", "unid", 1),
                Ingrediente("Pan de completo", "unid", 1),
                Ingrediente("Palta", "unid", 1),
                Ingrediente("Tomate", "unid", 1),
            ],
            precio=1800,
            icono_path="IMG/icono_hotdog_sin_texto_64x64.png",
        ),
        CrearMenu(
            "Pepsi",
            [
                Ingrediente("Pepsi", "unid", 1),
            ],
            precio=1100, 
            icono_path="IMG/icono_cola_64x64.png",
        ),
        CrearMenu(
            "Papas fritas",
            [
                Ingrediente("Papas", "unid", 5)
            ],
            precio=1100,
            icono_path="IMG/icono_papas_fritas_64x64.png",
        ),
        CrearMenu(
            "Hamburguesa",
            [
                Ingrediente("Pan de hamburguesa", "unid", 1),
                Ingrediente("Lamina de queso", "unid", 1),
                Ingrediente("Hamburgesa de carne", "unid", 1)
            ],
            precio=3500,
            icono_path="IMG/icono_hamburguesa_negra_64x64.png",
        ),
        CrearMenu(
            "Panqueques",
            [
                Ingrediente("Panqueque", "unid", 2),
                Ingrediente("Manjar", "unid", 1),
                Ingrediente("Azucar", "unid", 1)
            ],
            precio=2000,
            icono_path="IMG/icono_panqueques_64x64.png"
        ),
        CrearMenu(
            "Pollo frito",
            [
                Ingrediente("Presa de pollo", "unid", 1),
                Ingrediente("Porcion de harina","unid", 1),
                Ingrediente("Porcion de aceite", "unid", 1),
            ],
            precio=2800,
            icono_path="IMG/icono_pollo_frito_64x64.png",
        ),
        CrearMenu(
            "Ensalada Mixta",
            [
                Ingrediente("Lechuga", "unid", 1),
                Ingrediente("Tomate", "unid", 1),
                Ingrediente("Zanahoria rallada", "unid", 1),
            ],
            precio=1500,
            icono_path="IMG/icono_ensalada_mixta_64x64.png"
        )
    ]
