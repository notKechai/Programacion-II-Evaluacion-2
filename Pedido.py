from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  

    def agregar_menu(self, menu: CrearMenu):
        if menu not in self.menus:
            self.menus.append(menu)

    def eliminar_menu(self, nombre_menu: str):
        pass

    def mostrar_pedido(self):
        pass

    def calcular_total(self) -> float:
        pass
