from Ingrediente import Ingrediente
from CTkMessagebox import CTkMessagebox

class Stock:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        for ing in self.lista_ingredientes:
            if ing.nombre.lower() == ingrediente.nombre.lower() and ing.unidad == ingrediente.unidad:
                ing.cantidad = float(ing.cantidad) + float(ingrediente.cantidad) 
                return
            elif ing.nombre.lower() == ingrediente.nombre.lower() and ing.unidad != ingrediente.unidad:
                CTkMessagebox(title="Error de unidad", message=f"La unidad de {ing.nombre.lower()} es {ing.unidad.lower()}, no {ingrediente.unidad.lower()}", icon="warning")
                return
    
        self.lista_ingredientes.append(ingrediente)

    def eliminar_ingrediente(self, nombre_ingrediente: str):
        self.lista_ingredientes = [i for i in self.lista_ingredientes if i.nombre.lower() != nombre_ingrediente.lower()]

    def verificar_stock(self):
        return {f'{i.nombre} ({i.unidad})': float(i.cantidad) for i in self.lista_ingredientes}

    def actualizar_stock(self, nombre_ingrediente, nueva_cantidad):
        for i in self.lista_ingredientes:
            if i.nombre == nombre_ingrediente:
                i.cantidad = float(nueva_cantidad)
                return True
        return False

    def obtener_elementos_menu(self):
        return self.lista_ingredientes[:]



