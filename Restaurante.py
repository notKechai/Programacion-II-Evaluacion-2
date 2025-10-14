from ElementoMenu import CrearMenu
import customtkinter as ctk
from tkinter import ttk, Toplevel, Label, messagebox
from Ingrediente import Ingrediente
from Stock import Stock
import re
from PIL import Image
from CTkMessagebox import CTkMessagebox
from Pedido import Pedido
from BoletaFacade import BoletaFacade
import pandas as pd
from tkinter import filedialog
from Menu_catalog import get_default_menus
from menu_pdf import create_menu_pdf
from ctk_pdf_viewer import CTkPDFViewer
import os
from tkinter.font import nametofont
class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestión de ingredientes y pedidos")
        self.geometry("870x700")
        nametofont("TkHeadingFont").configure(size=14)
        nametofont("TkDefaultFont").configure(size=11)

        self.stock = Stock()
        self.menus_creados = []

        self.pedido = Pedido()

        self.menus = get_default_menus()  
  
        self.tabview = ctk.CTkTabview(self,command=self.on_tab_change)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.crear_pestanas()

    def actualizar_treeview(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for ingrediente in self.stock.lista_ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre,ingrediente.unidad, ingrediente.cantidad))    

    def on_tab_change(self):
        selected_tab = self.tabview.get()
        if selected_tab == "carga de ingredientes":
            print('Carga de ingredientes')
        if selected_tab == "Stock":
            self.actualizar_treeview()
            print("Stock")
        if selected_tab == "Pedido":
            self.actualizar_treeview()
            self.generar_menus()
            print('Pedido')
        if selected_tab == "Carta restaurante":
            self.actualizar_treeview()
            print('Carta restaurante')
        if selected_tab == "Boleta":
            self.actualizar_treeview()
            print('Boleta')       
    def crear_pestanas(self):
        self.tab3 = self.tabview.add("Carga de ingredientes")  
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restaurante")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()   
        self._configurar_pestana_ver_boleta()

    def configurar_pestana3(self):
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV o Excel")
        label.pack(pady=20)
        boton_cargar_csv = ctk.CTkButton(self.tab3, text="Cargar CSV o Excel", fg_color="#1976D2", text_color="white",command=self.cargar_csv)

        boton_cargar_csv.pack(pady=10)

        self.frame_tabla_csv = ctk.CTkFrame(self.tab3)
        self.frame_tabla_csv.pack(fill="both", expand=True, padx=10, pady=10)
        self.df_csv = None   
        self.tabla_csv = None

        self.boton_agregar_stock = ctk.CTkButton(self.frame_tabla_csv, text="Agregar al Stock",fg_color="#1976D2", text_color="white", command=self.agregar_csv_al_stock)
        self.boton_agregar_stock.pack(side="bottom", pady=10)
 
    def agregar_csv_al_stock(self):
        if self.df_csv is None:
            CTkMessagebox(title="Error", message="Primero debes cargar un archivo.", icon="warning")
            return
        
        try:
        # Asegurar normalización de columnas sin helpers
            df = self.df_csv.rename(columns={c: c.strip().lower() for c in self.df_csv.columns})

        # Validar columnas requeridas
            if not all(c in df.columns for c in ("nombre", "unidad", "cantidad")):
                CTkMessagebox(title="Error", message="El archivo debe tener columnas 'nombre', 'unidad' y 'cantidad'.", icon="warning")
                return

            for _, row in df.iterrows():
                nombre = str(row['nombre']).strip()
                unidad = str(row['unidad']).strip()
                cantidad = row['cantidad']

            # Validar unidad
                if unidad not in ("kg", "unid"):
                    CTkMessagebox(title="Unidad inválida",
                                message=f"Unidad no soportada para '{nombre}': {unidad}",
                                icon="warning")
                    continue

            # Convertir cantidad a número
                try:
                    cantidad = float(cantidad)
                except:
                    CTkMessagebox(title="Dato inválido",
                                message=f"Cantidad inválida para '{nombre}': {cantidad}",
                                icon="warning")
                    continue

                if unidad == "unid":
                    cantidad = int(cantidad)

                ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=cantidad)
                self.stock.agregar_ingrediente(ingrediente)

            CTkMessagebox(title="Stock Actualizado", message="Ingredientes agregados al stock correctamente.", icon="check")
            self.tabview.set("Stock")
            self.actualizar_treeview()
        
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo agregar al stock.\n{e}", icon="warning")


    def cargar_csv(self):
        ruta = filedialog.askopenfilename(
            parent=self,
            title='Selecciona archivo CSV o Excel',
            filetypes=[('CSV', '*.csv'), 
                       ("Excel", ('*.xlsx', '*.xls')), 
                       ('Todos los archivos', "*")
            ]
        )

        if not ruta:
            return #el usuario canceló la selección
        
        try:
            ext = os.path.splitext(ruta)[1].lower()
            if ext == ".csv":
                try:
                    df = pd.read_csv(ruta)
                except UnicodeDecodeError:
                    df = pd.read_csv(ruta, encoding='latin-1')
            elif ext in ('.xlsx', '.xls'):
                df = pd.read_excel(ruta)
            else:
                CTkMessagebox(title="Formato no soportado",
                              message="Usa CSV, XLSX o XLS.",
                              icon="warning")
                return
            
            df = df.rename(columns={c: c.strip().lower() for c in df.columns})

            requeridas = ('nombre', 'unidad', 'cantidad')
            faltan = [c for c in requeridas if c not in df.columns]
            if faltan:
                CTkMessagebox(title='Columnas Faltantes',
                              message=f"El archivo debe incluir las columnas: 'nombre', 'unidad', 'cantidad'. Faltan: {', '.join(faltan)}",
                              icon="warning")
                return
        except Exception as e:
            CTkMessagebox(title='Error al leer el archivo',
                          message=f'No se pudo leer el archivo.\n{e}',
                          icon='warning')
            return
        
        self.df_csv = df
        self.mostrar_dataframe_en_tabla(df)

    def mostrar_dataframe_en_tabla(self, df):
        if self.tabla_csv:
            self.tabla_csv.destroy()

        self.tabla_csv = ttk.Treeview(self.frame_tabla_csv, columns=list(df.columns), show="headings")
        for col in df.columns:
            self.tabla_csv.heading(col, text=col)
            self.tabla_csv.column(col, width=100, anchor="center")


        for _, row in df.iterrows():
            self.tabla_csv.insert("", "end", values=list(row))

        self.tabla_csv.pack(expand=True, fill="both", padx=10, pady=10)

    def actualizar_treeview_pedido(self):
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)

        for menu in self.pedido.menus:
            self.treeview_menu.insert("", "end", values=(menu.nombre, menu.cantidad, f"${menu.precio:.2f}"))
            
    def _configurar_pestana_crear_menu(self):
        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        boton_menu = ctk.CTkButton(
            contenedor,
            text="Generar Carta (PDF)",
            command=self.generar_y_mostrar_carta_pdf
        )
        boton_menu.pack(pady=10)

        self.pdf_frame_carta = ctk.CTkFrame(contenedor)
        self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_carta = None

    def generar_y_mostrar_carta_pdf(self):
        try:
            menus_para_pdf = [m for m in self.menus if m.esta_disponible(self.stock)]
            
            if not menus_para_pdf:
                CTkMessagebox(
                    title="Sin datos",
                    message="No hay menús dusponibles con el stock actual para generar la carta",
                    icon="warning"
                )
                return
            
            pdf_path = "carta.pdf"
            abs_pdf = create_menu_pdf(
                menus=menus_para_pdf,
                pdf_path=pdf_path,
                titulo_negocio="Restaurante",
                subtitulo="Carta (según el stock actual)",
                moneda="$",
            )
            
        
            #Limpiando el visor previo

            if self.pdf_viewer_carta is not None:
                try:
                    self.pdf_viewer_carta.pack_forget()
                    self.pdf_viewer_carta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_carta = None
            
            #Monatando el visor

            if not os.path.exists(abs_pdf):
                CTkMessagebox(title="Error", message="No se encontró el PDF generado.", icon="warning")
                return
            
            self.pdf_viewer_carta = CTkPDFViewer(self.pdf_frame_carta, file=abs_pdf)
            self.pdf_viewer_carta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar/mostrar la carta.\n{e}", icon="warning")

    def _configurar_pestana_ver_boleta(self):
        contenedor = ctk.CTkFrame(self.tab5)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)
    
        boton_boleta = ctk.CTkButton(
            contenedor,
            text="Mostrar Boleta (PDF)",
            command=self.mostrar_boleta
        )
        boton_boleta.pack(pady=10)
    
        self.pdf_frame_boleta = ctk.CTkFrame(contenedor)
        self.pdf_frame_boleta.pack(expand=True, fill="both", padx=10, pady=10)
    
        self.pdf_viewer_boleta = None
        
    # SE LE IMPLEMENTA BOLETAFACDE
    def mostrar_boleta(self):
        try:
            pdf_path = os.path.abspath("boleta.pdf")
            if not os.path.exists(pdf_path):
                CTkMessagebox(title="Sin boleta",
                            message="Aún no hay una boleta generada. Primero genera una desde la pestaña 'Pedido'.",
                            icon="warning")
                return

            if self.pdf_viewer_boleta is not None:
                try:
                    self.pdf_viewer_boleta.pack_forget()
                    self.pdf_viewer_boleta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_boleta = None

            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=pdf_path)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo mostrar la boleta.\n{e}", icon="warning")

            if self.pdf_viewer_boleta is not None:
                try:
                    self.pdf_viewer_boleta.pack_forget()
                    self.pdf_viewer_boleta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_boleta = None

            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar/mostrar la boleta.\n{e}", icon="warning")

            
    def configurar_pestana1(self):
        # Dividir la Pestaña 1 en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Unidad:")
        label_cantidad.pack(pady=5)
        self.combo_unidad = ctk.CTkComboBox(frame_formulario, values=["kg", "unid"])
        self.combo_unidad.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente")
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Unidad","Cantidad"), show="headings",height=25)
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_menu = ctk.CTkButton(frame_formulario, text="Generar Menú", command=self.generar_menus)
        self.boton_generar_menu.pack(pady=10)

    def tarjeta_click(self, event, menu):
        suficiente_stock = True
        if self.stock.lista_ingredientes==[]:
            suficiente_stock=False
        for ingrediente_necesario in menu.ingredientes:
            for ingrediente_stock in self.stock.lista_ingredientes:
                if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                    if float(ingrediente_stock.cantidad) < float(ingrediente_necesario.cantidad):
                        suficiente_stock = False
                        break
            if not suficiente_stock:
                break
        
        if suficiente_stock:
            for ingrediente_necesario in menu.ingredientes:
                for ingrediente_stock in self.stock.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        nueva_cantidad = float(ingrediente_stock.cantidad) - float(ingrediente_necesario.cantidad)
                        if ingrediente_stock.unidad == 'unid':
                            ingrediente_stock.cantidad = int(nueva_cantidad)
                        else:
                            ingrediente_stock.cantidad = nueva_cantidad
            
            self.pedido.agregar_menu(menu)
            self.actualizar_treeview_pedido()
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")
    
    def cargar_icono_menu(self, ruta_icono):
        imagen = Image.open(ruta_icono)
        icono_menu = ctk.CTkImage(imagen, size=(64, 64))
        return icono_menu

    
    def generar_menus(self):
        try:
            for widget in tarjetas_frame.winfo_children():
                widget.destroy()

            boton_menu = ctk.CTkButton(
            self.tab4, text="Generar Carta (PDF)", command=self.generar_y_mostrar_carta_pdf
            )
            boton_menu.pack(pady=10)

            self.pdf_viewer_carta = None
            self.pdf_frame_carta = ctk.CTkFrame(self.tab4)
            self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

            self.menus_creados.clear()

            for menu in self.menus:
                if menu.esta_disponible(self.stock):
                    if not any(m.nombre == menu.nombre for m in self.menus_creados):
                        self.menus_creados.append(menu)
                        self.crear_tarjeta(menu)
            else:
                print(f"No hay stock suficiente para '{menu.nombre}'")

            if not self.menus_creados:
                CTkMessagebox(
                title="Sin Stock suficiente",
                message="No se pudo generar ningún menu porque falta stock",
                icon="warning"
                )
            else:
                CTkMessagebox(
                title="Menús generados",
                message=f"Se generaron {len(self.menus_creados)} menús disponibles.",
                icon="info"
            )

        except Exception as e:
            CTkMessagebox(title="Error", message=f'Error al generar los menús.\n{e}', icon="warning")

    def eliminar_menu(self):
        sel = self.treeview_menu.selection()
        if not sel:
            CTkMessagebox(title="Nada Seleccionado", message="Debes seleccionar un menú para eliminar.", icon="warning")
            return
        
        # Eliminar el primer bloque de lógica de eliminación/devolución
        # que no está dentro del try/except, ya que el segundo bloque es más completo.

        try:
        # 1) Identificar el menú seleccionado
            item_id = sel[0]
            valores = self.treeview_menu.item(item_id, "values")
            if not valores:
                # Si se selecciona la cabecera u otra cosa sin valores
                CTkMessagebox(title="Nada Seleccionado", message="Debes seleccionar un menú para eliminar.", icon="warning")
                return

            nombre_menu_sel = valores[0]

        # 2) Buscar el menú y su cantidad en el pedido
            menu_en_pedido = None
            for m in self.pedido.menus:
                if m.nombre == nombre_menu_sel:
                    menu_en_pedido = m
                    break
                
            if menu_en_pedido is None:
                CTkMessagebox(title="No encontrado", message="No se encontró el menú seleccionado en el pedido.", icon="warning")
                return

            cantidad_menus = int(menu_en_pedido.cantidad) if menu_en_pedido.cantidad else 0
            if cantidad_menus <= 0:
            # Quitarlo de la lista si estuviera (aunque la cantidad sea 0 o menos)
                self.pedido.menus = [x for x in self.pedido.menus if x.nombre != nombre_menu_sel]
            else:
            # 3) Devolver al stock TODA la cantidad de este menú
                for req in menu_en_pedido.ingredientes:
                    total_devolver = float(req.cantidad) * cantidad_menus
                    # Asumiendo que 'Ingrediente' es una clase válida
                    self.stock.agregar_ingrediente(Ingrediente(req.nombre, req.unidad, total_devolver))

            # 4) Quitar completamente el menú del pedido
            # Esto se hace tanto en el if como en el else si es la intención
            self.pedido.menus = [x for x in self.pedido.menus if x.nombre != nombre_menu_sel]
            
            # Borrar la fila seleccionada de la treeview
            self.treeview_menu.delete(item_id)

        # 5) Refrescar UI
            self.actualizar_treeview()         # stock
            self.actualizar_treeview_pedido()  # tabla del pedido
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:,.0f}".replace(",", "."))

            CTkMessagebox(title="Eliminado", message=f"Se eliminó '{nombre_menu_sel}' del pedido y se devolvió el stock.", icon="info")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo eliminar el menú.\n{e}", icon="warning")
    
    def generar_boleta(self):
        if not self.pedido.menus:
            CTkMessagebox(title="Sin items", message="El pedido está vacío.", icon="warning")
            return
        
        try:
            facade = BoletaFacade(self.pedido)
            facade.generar_boleta()

            self.pedido = Pedido()
            self.actualizar_treeview_pedido()
            self.label_total.configure(text="Total: $0.00")
            
            CTkMessagebox(title="Boleta Generada", message="Boleta generada correctamente.\nVe a la pestaña 'Boleta' y pulsa 'Mostrar Boleta' para visualizarla.",
            icon="info")

            for item in self.tree.get_children():
                self.tree.delete(item)
        except Exception as e:
            CTkMessagebox(title="Error", message=f'No se pudo generar la boleta.\n{e}', icon="warning")

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_intermedio = ctk.CTkFrame(self.tab2)
        frame_intermedio.pack(side="top", fill="x", padx=10, pady=5)

        global tarjetas_frame
        tarjetas_frame = ctk.CTkFrame(frame_superior)
        tarjetas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(frame_intermedio, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(side="right", padx=10)

        self.label_total = ctk.CTkLabel(frame_intermedio, text="Total: $0.00", anchor="e", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio Unitario"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_boleta=ctk.CTkButton(frame_inferior,text="Generar Boleta",command=self.generar_boleta)
        self.boton_generar_boleta.pack(side="bottom",pady=10)

    def crear_tarjeta(self, menu):
        num_tarjetas = len(self.menus_creados)
        fila = 0
        columna = num_tarjetas

        tarjeta = ctk.CTkFrame(
            tarjetas_frame,
            corner_radius=10,
            border_width=1,
            border_color="#4CAF50",
            width=64,
            height=140,
            fg_color="gray",
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        if getattr(menu, "icono_path", None):
            try:
                icono = self.cargar_icono_menu(menu.icono_path)
                imagen_label = ctk.CTkLabel(
                    tarjeta, image=icono, width=64, height=64, text="", bg_color="transparent"
                )
                imagen_label.image = icono
                imagen_label.pack(anchor="center", pady=5, padx=10)
                imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
            except Exception as e:
                print(f"No se pudo cargar la imagen '{menu.icono_path}': {e}")

        texto_label = ctk.CTkLabel(
            tarjeta,
            text=f"{menu.nombre}",
            text_color="black",
            font=("Helvetica", 12, "bold"),
            bg_color="transparent",
        )
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad, unidad):
        try:
            if unidad == "unid":
                cantidad_num = int(cantidad)
                if cantidad_num <= 0:
                    CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número positivo.",icon="warning")
                    return False
            elif unidad == "kg":
                cantidad_num = float(cantidad)
                if cantidad_num <= 0:
                    CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número positivo.",icon="warning")
                    return False
            return True
        except ValueError:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número positivo.",icon="warning")

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get().strip()
        unidad = self.combo_unidad.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not nombre or not unidad or not cantidad:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="warning")
            return

        if not self.validar_nombre(nombre):
            return

        if not self.validar_cantidad(cantidad, unidad):
            return

        if unidad == "kg":
            cantidad = float(cantidad)
        elif unidad == "unid":
            cantidad = int(cantidad)

        nuevo_ingrediente = Ingrediente(nombre,unidad,cantidad)
        self.stock.agregar_ingrediente(nuevo_ingrediente)
        self.actualizar_treeview()
        CTkMessagebox(title="Éxito!", message="El ingrediente se a añadido correctamente.", icon="check")
        

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
                CTkMessagebox(title="Error", message="Selecciona un ingrediente para eliminar.", icon="warfning")
                return
        item_id = seleccion[0]
        nombre_ingrediente = self.tree.item(item_id, "values")[0]
        self.stock.eliminar_ingrediente(nombre_ingrediente)

        self.actualizar_treeview()

        CTkMessagebox(title="Ingrediente eliminado", message=f"'{nombre_ingrediente}' fue eliminado del stock.", icon="info")

        

    def actualizar_treeview(self):
        if not hasattr(self, "tree"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for ingrediente in self.stock.lista_ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.unidad, ingrediente.cantidad))


if __name__ == "__main__":
    import customtkinter as ctk
    from tkinter import ttk

    ctk.set_appearance_mode("Dark")  
    ctk.set_default_color_theme("blue") 
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = AplicacionConPestanas()

    try:
        style = ttk.Style(app)   
        style.theme_use("clam")
    except Exception:
        pass

    app.mainloop()