from typing import List
from ElementoMenu import CrearMenu

class Pedido:
    def __init__(self):
        self.menus: List[CrearMenu] = [] 

    def agregar_menu(self, menu: CrearMenu, cantidad: int = 1):
        for m in self.menus:
            if m.nombre == menu.nombre:
                m.cantidad += cantidad
                return
        nuevo = CrearMenu(
            nombre=menu.nombre,
            ingredientes=menu.ingredientes,
            precio=menu.precio,
            icono_path=menu.icono_path,
            cantidad=cantidad
        )
        self.menus.append(nuevo)

    def eliminar_menu(self, nombre_menu: str, cantidad: int = 1) -> bool:
        for m in list(self.menus):
            if m.nombre == nombre_menu:
                m.cantidad -= cantidad
                if m.cantidad <= 0:
                    self.menus.remove(m)
                return True
        return False

    def mostrar_pedido(self):
        return [(m.nombre, m.cantidad, m.precio, m.cantidad * m.precio) for m in self.menus]

    def calcular_total(self) -> float:
        return sum(m.precio * m.cantidad for m in self.menus)
