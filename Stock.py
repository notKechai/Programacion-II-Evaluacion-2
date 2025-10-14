from Ingrediente import Ingrediente
from CTkMessagebox import CTkMessagebox

class Stock:
    def __init__(self):
        # Almacenamiento real encapsulado
        self._lista_ingredientes = []

    # Getter público (solo lectura) para mantener compatibilidad:
    # podrás seguir haciendo: for i in self.stock.lista_ingredientes
    @property
    def lista_ingredientes(self):
        return self._lista_ingredientes

    def agregar_ingrediente(self, ingrediente: Ingrediente):
        nombre_nuevo = ingrediente.nombre.strip().capitalize()
        unidad_nueva = ingrediente.unidad

        for ing in self._lista_ingredientes:
            if ing.nombre.capitalize() == nombre_nuevo and ing.unidad == unidad_nueva:
                ing.cantidad = float(ing.cantidad) + float(ingrediente.cantidad)
                return
            elif ing.nombre.capitalize() == nombre_nuevo and ing.unidad != unidad_nueva:
                CTkMessagebox(
                    title="Error de unidad",
                    message=f"La unidad de {ing.nombre.capitalize()} es {ing.unidad.capitalize()}, no {unidad_nueva.strip().capitalize()}",
                    icon="warning"
                )
                return

        ingrediente.nombre = nombre_nuevo
        self._lista_ingredientes.append(ingrediente)

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
        # Devolvemos una copia superficial para evitar mutaciones externas accidentales
        return self._lista_ingredientes[:]
