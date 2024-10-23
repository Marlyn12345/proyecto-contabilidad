import tkinter as tk
from tkinter import ttk, messagebox
from typing import Self
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BreakEvenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo del Punto de Equilibrio")
        self.root.geometry("800x600")  
        self.style = ttk.Style()
        self.style.configure("TNotebook", tabposition='wn')
        self.style.configure("TButton", padding=6, background="#F2C2D4")
        self.style.configure("TLabel", padding=6)

        # Estilo para las tablas
        self.style.configure("Treeview", rowheight=18, font=('Arial', 10))
        self.style.map("Treeview", background=[("selected", "#d1e7f4")])  # Color de selección
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        self.title_label = ttk.Label(self.root, text="Danna Lucrecia Del Cid López      y       Marlyn Yaneth Ixcoy García", font=('Arial', 12, 'bold'), background="#F3EAF4")
        self.title_label.pack(pady=10, anchor='nw')  
        
        
        # Crear pestañas
        self.tab_control = ttk.Notebook(self.root)

        self.tab_calculo = tk.Frame(self.tab_control, bg="#F3EAF4")
        self.tab_grafica = tk.Frame(self.tab_control, bg="#F3EAF4")

        self.tab_control.add(self.tab_calculo, text='Cálculo')
        self.tab_control.add(self.tab_grafica, text='Gráfica')

        self.tab_control.pack(expand=1, fill='both')

        self.create_calculo_tab()
        self.create_grafica_tab()

        self.canvas = None  
        
        self.footer_label = ttk.Label(self.root, text="26 de octubre de 2024", font=('Arial', 10), background="#F3EAF4")
        self.footer_label.pack(side='bottom', pady=10) 
  

    def create_calculo_tab(self):
        # Entradas de usuario
        ttk.Label(self.tab_calculo, text="Costos Fijos (Quetzales):", background="#F3EAF4", foreground="#040348").grid(column=0, row=0, sticky='w', padx=10, pady=5)
        self.fixed_costs = tk.DoubleVar()
        ttk.Entry(self.tab_calculo, textvariable=self.fixed_costs).grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(self.tab_calculo, text="Precio de Venta (Quetzales):", background="#F3EAF4", foreground="#040348").grid(column=0, row=1, sticky='w', padx=10, pady=5)
        self.sale_price = tk.DoubleVar()
        ttk.Entry(self.tab_calculo, textvariable=self.sale_price).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self.tab_calculo, text="Costo Variable por Unidad (Quetzales):", background="#F3EAF4", foreground="#040348").grid(column=0, row=2, sticky='w', padx=10, pady=5)
        self.variable_cost = tk.DoubleVar()
        ttk.Entry(self.tab_calculo, textvariable=self.variable_cost).grid(column=1, row=2, padx=10, pady=5)

        # Botón para calcular
        ttk.Button(self.tab_calculo, text="Calcular Punto de Equilibrio", command=self.calculate_breakeven).grid(column=0, row=3, columnspan=2, pady=10)

        # Crear tabla de resultados
        self.create_results_table()

    def create_results_table(self):
        # Configurar la tabla
        columns = ["Producción", "Unidades", "Ingreso por Ventas", "Costos Variables", "Costos Fijos", "Resultado"]
        self.results_table = ttk.Treeview(self.tab_calculo, columns=columns, show='headings')
        
        # Definir encabezados
        for col in columns:
            self.results_table.heading(col, text=col)
            self.results_table.column(col, anchor='center')

        self.results_table.grid(column=0, row=4, columnspan=2, pady=10, sticky='nsew')

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.tab_calculo, orient="vertical", command=self.results_table.yview)
        scrollbar.grid(column=2, row=4, sticky='ns')
        self.results_table.configure(yscroll=scrollbar.set)

        # Configurar las líneas de separación
        self.results_table.tag_configure("oddrow", background="#FFFFFF")
        self.results_table.tag_configure("evenrow", background="#FAEBD7")

    def show_error(self, message):
        messagebox.showerror("Error de Entrada", message)

    def calculate_breakeven(self):
        fixed_costs = self.fixed_costs.get()
        sale_price = self.sale_price.get()
        variable_cost = self.variable_cost.get()

        if sale_price <= variable_cost:
            self.show_error("El precio de venta debe ser mayor que el costo variable por unidad.")
            return

        if fixed_costs < 0 or sale_price < 0 or variable_cost < 0:
            self.show_error("Los costos fijos, el precio de venta y el costo variable deben ser valores positivos.")
            return

        contribution_margin = sale_price - variable_cost
        breakeven_units = fixed_costs / contribution_margin

        result_message = f"Margen de Contribución por Unidad: {round(contribution_margin, 2)} Quetzales\n"
        result_message += f"Punto de Equilibrio: {round(breakeven_units, 2)} unidades"
        messagebox.showinfo("Resultados", result_message)

        production_levels = {
            "20% menos de producción": breakeven_units * 0.8,
            "10% menos de producción": breakeven_units * 0.9,
            "Punto de equilibrio": breakeven_units,
            "10% más de producción": breakeven_units * 1.1,
            "20% más de producción": breakeven_units * 1.2,
        }

        self.results_table.delete(*self.results_table.get_children())

        # Insertar los datos en la tabla
        for idx, (label, units) in enumerate(production_levels.items()):
            revenue = sale_price * units
            variable_costs = variable_cost * units
            result = revenue - (variable_costs + fixed_costs)

            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.results_table.insert("", "end", values=(label, round(units), round(revenue, 2), round(variable_costs, 2), round(fixed_costs, 2), round(result, 2)), tags=(row_tag,))

    def create_grafica_tab(self):
        self.create_graph_results_table()

        ttk.Button(self.tab_grafica, text="Mostrar Gráfica", command=self.plot_breakeven).pack(pady=20)
        ttk.Button(self.tab_grafica, text="Borrar Datos", command=self.clear_data).pack(pady=10)

    def create_graph_results_table(self):
        columns = ["Total de Unidades", "Ingresos Totales", "Costos Totales", "Costos Fijos", "Costos Variables"]
        self.graph_results_table = ttk.Treeview(self.tab_grafica, columns=columns, show='headings')

        for col in columns:
            self.graph_results_table.heading(col, text=col)
            self.graph_results_table.column(col, anchor='center')

        self.graph_results_table.pack(pady=10, fill='x')
        
        scrollbar = ttk.Scrollbar(self.tab_grafica, orient="vertical", command=self.graph_results_table.yview)
        scrollbar.pack(side='right', fill='y')
        self.graph_results_table.configure(yscroll=scrollbar.set)

        # Configurar las líneas de separación
        self.graph_results_table.tag_configure("oddrow", background="#FFFFFF")
        self.graph_results_table.tag_configure("evenrow", background="#FAEBD7")

    def plot_breakeven(self):
        fixed_costs = self.fixed_costs.get()
        sale_price = self.sale_price.get()
        variable_cost = self.variable_cost.get()

        contribution_margin = sale_price - variable_cost
        breakeven_units = fixed_costs / contribution_margin

        units = np.arange(0, breakeven_units * 2, 1)
        revenue = sale_price * units
        total_costs = fixed_costs + variable_cost * units
        variable_costs = variable_cost * units  
        fixed_costs_line = np.full_like(units, fixed_costs)  

        self.graph_results_table.delete(*self.graph_results_table.get_children())

        for idx, u in enumerate(units):
            self.graph_results_table.insert("", "end", values=(u, round(revenue[int(u)], 2), round(total_costs[int(u)], 2), round(fixed_costs, 2), round(variable_costs[int(u)], 2)), tags=("evenrow" if idx % 2 == 0 else "oddrow",))

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(units, revenue, label='Ingresos Totales', color='green')
        ax.plot(units, total_costs, label='Costos Totales', color='red')
        ax.plot(units, variable_costs, label='Costos Variables', linestyle='--', color='blue')
        ax.axhline(y=fixed_costs, color='orange', linestyle='--', label='Costos Fijos')

        # Líneas del punto de equilibrio
        ax.axvline(x=breakeven_units, color='purple', linestyle='--', label='Punto de Equilibrio')

        ax.set_title('Gráfica del Punto de Equilibrio')
        ax.set_xlabel('Unidades')
        ax.set_ylabel('Quetzales')
        ax.legend()
        ax.grid(True)

        # Si ya existe una gráfica, la borramos
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Crear un nuevo lienzo para la gráfica
        self.canvas = FigureCanvasTkAgg(fig, master=self.tab_grafica)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def clear_data(self):
        # Limpiar entradas
        self.fixed_costs.set(0)
        self.sale_price.set(0)
        self.variable_cost.set(0)

        # Limpiar tablas
        self.results_table.delete(*self.results_table.get_children())
        self.graph_results_table.delete(*self.graph_results_table.get_children())

        # Si existe una gráfica, eliminarla
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None  # Reiniciar el lienzo

if __name__ == "__main__":
    root = tk.Tk()
    app = BreakEvenApp(root)
    root.mainloop()
