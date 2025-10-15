from Ingrediente import Ingrediente
from CTkMessagebox import CTkMessagebox

class Stock:
    def __init__(self):
        self._lista_ingredientes = []

    @property
    def lista_ingredientes(self):
        return self._lista_ingredientes

    def agregar_ingrediente(self, ingrediente: Ingrediente):
        nombre_nuevo = ingrediente.nombre.strip().capitalize()
        unidad_nueva = ingrediente.unidad

        for ing in self._lista_ingredientes:
            if ing.nombre.capitalize() == nombre_nuevo and ing.unidad == unidad_nueva:
                ing.cantidad = float(ing.cantidad) + float(ingrediente.cantidad)
                return "actualizado"
            elif ing.nombre.capitalize() == nombre_nuevo and ing.unidad != unidad_nueva:
                return "error"

        ingrediente.nombre = nombre_nuevo
        self._lista_ingredientes.append(ingrediente)
        return "nuevo"

    def eliminar_ingrediente(self, nombre_ingrediente: str):
        self._lista_ingredientes = [
            i for i in self._lista_ingredientes
            if i.nombre.lower() != nombre_ingrediente.lower()
        ]

    def verificar_stock(self):
        return {f'{i.nombre} ({i.unidad})': float(i.cantidad) for i in self._lista_ingredientes}

    def actualizar_stock(self, nombre_ingrediente: str, nueva_cantidad):
        for i in self._lista_ingredientes:
            if i.nombre == nombre_ingrediente:
                i.cantidad = float(nueva_cantidad)
                return True
        return False

    def obtener_elementos_menu(self):
        return self._lista_ingredientes[:]
