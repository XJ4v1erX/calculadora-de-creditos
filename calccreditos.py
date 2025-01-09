import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk, messagebox
import re

# Datos del historial
tabla_historial = []

def calcular_tasa():
    try:
        nombre = entry_nombre.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        monto_credito = entry_monto.get()
        tipo_cliente = combo_tipo.get()
        plazo = combo_plazo.get()

        # Validaciones
        if not nombre.strip():
            raise ValueError("El campo 'Nombre' es obligatorio.")
        if not correo.strip() or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            raise ValueError("Ingrese un correo electrónico válido.")
        if not telefono.strip() or not telefono.isdigit():
            raise ValueError("El campo 'Teléfono' debe contener solo números.")
        if not monto_credito.strip() or not monto_credito.isdigit():
            raise ValueError("El campo 'Monto del Crédito' debe ser un número válido.")
        if not tipo_cliente.strip():
            raise ValueError("Seleccione un 'Tipo de Cliente'.")
        if not plazo.strip():
            raise ValueError("Seleccione un 'Plazo (años)'.")

        monto_credito = float(monto_credito)
        plazo = int(plazo)

        # Cálculo de costos
        costo_dinero = 0.04 * monto_credito
        costo_nomina = 200
        costo_agencia = 35

        if tipo_cliente == "Persona":
            costo_oportunidad = 0.04 * monto_credito
        elif tipo_cliente == "Pyme":
            costo_oportunidad = 0.05 * monto_credito
        elif tipo_cliente == "Empresa":
            costo_oportunidad = 0.06 * monto_credito
        else:
            raise ValueError("Seleccione un tipo de cliente válido.")

        if plazo == 3:
            costo_tiempo = 0.02 * monto_credito
        elif plazo == 4:
            costo_tiempo = 0.03 * monto_credito
        elif plazo == 5:
            costo_tiempo = 0.04 * monto_credito
        else:
            raise ValueError("Seleccione un plazo válido.")

        # Suma de costos
        costos_totales = costo_dinero + costo_nomina + costo_agencia + costo_oportunidad + costo_tiempo

        # Cálculo de la tasa de interés
        tasa_interes = (costos_totales / monto_credito) * 100

        # Actualizar resultados
        label_resultado_tasa.config(text=f"Tasa de interés: {tasa_interes:.2f}%")
        label_costo_dinero.config(text=f"Costo del Dinero: Q{costo_dinero:.2f}")
        label_costo_nomina.config(text=f"Costo de Nómina: Q{costo_nomina:.2f}")
        label_costo_agencia.config(text=f"Costo por Agencia: Q{costo_agencia:.2f}")
        label_costo_oportunidad.config(text=f"Costo de Oportunidad: Q{costo_oportunidad:.2f}")
        label_costo_tiempo.config(text=f"Costo del Tiempo: Q{costo_tiempo:.2f}")

        # Agregar al historial
        tabla_historial.append((nombre, correo, telefono, monto_credito, f"{tasa_interes:.2f}%"))
        actualizar_tabla()

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "Ocurrió un error inesperado. Verifique los datos ingresados.")


def actualizar_tabla():
    for row in tabla_historial_tree.get_children():
        tabla_historial_tree.delete(row)

    for i, (nombre, correo, telefono, monto, tasa) in enumerate(tabla_historial):
        tabla_historial_tree.insert("", "end", values=(i + 1, nombre, correo, telefono, monto, tasa))


def eliminar_seleccion():
    try:
        seleccionado = tabla_historial_tree.selection()[0]
        indice = int(tabla_historial_tree.item(seleccionado)['values'][0]) - 1
        del tabla_historial[indice]
        actualizar_tabla()
    except IndexError:
        messagebox.showerror("Error", "Seleccione un registro para eliminar.")

# Configuración de la ventana principal
style = Style(theme="yeti")  # Tema moderno con colores claros
ventana = style.master
ventana.title("Calculadora de Créditos")
ventana.geometry("1200x850")
ventana.configure(bg="white")

# Título principal
titulo_label = ttk.Label(ventana, text="Calculadora de Créditos", font=("Helvetica", 24), anchor="center", foreground="goldenrod", background="white")
titulo_label.pack(pady=20)

# Marco principal para entrada y resultados
frame_principal = ttk.Frame(ventana)
frame_principal.pack(fill="both", padx=20, pady=10)

# Configurar grid del frame principal
frame_principal.columnconfigure(0, weight=1)
frame_principal.columnconfigure(1, weight=1)
frame_principal.rowconfigure(0, weight=1)

# Marco de entrada de datos
frame_entrada = ttk.LabelFrame(frame_principal, text="Datos del Cliente", padding=20)
frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label_nombre = ttk.Label(frame_entrada, text="Nombre", background="white")
label_nombre.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nombre = ttk.Entry(frame_entrada)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

label_correo = ttk.Label(frame_entrada, text="Correo Electrónico", background="white")
label_correo.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_correo = ttk.Entry(frame_entrada)
entry_correo.grid(row=1, column=1, padx=10, pady=5)

label_telefono = ttk.Label(frame_entrada, text="Teléfono", background="white")
label_telefono.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_telefono = ttk.Entry(frame_entrada)
entry_telefono.grid(row=2, column=1, padx=10, pady=5)

label_monto = ttk.Label(frame_entrada, text="Monto del Crédito", background="white")
label_monto.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_monto = ttk.Entry(frame_entrada)
entry_monto.grid(row=3, column=1, padx=10, pady=5)

label_tipo = ttk.Label(frame_entrada, text="Tipo de Cliente", background="white")
label_tipo.grid(row=4, column=0, padx=10, pady=5, sticky="w")
combo_tipo = ttk.Combobox(frame_entrada, values=["Persona", "Pyme", "Empresa"])
combo_tipo.grid(row=4, column=1, padx=10, pady=5)

label_plazo = ttk.Label(frame_entrada, text="Plazo (años)", background="white")
label_plazo.grid(row=5, column=0, padx=10, pady=5, sticky="w")
combo_plazo = ttk.Combobox(frame_entrada, values=["3", "4", "5"])
combo_plazo.grid(row=5, column=1, padx=10, pady=5)

btn_calcular = ttk.Button(frame_entrada, text="Calcular", command=calcular_tasa, bootstyle="warning")
btn_calcular.grid(row=6, column=0, columnspan=2, pady=20)

# Marco de resultados
frame_resultado = ttk.LabelFrame(frame_principal, text="Resultados", padding=20)
frame_resultado.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

label_resultado_tasa = ttk.Label(frame_resultado, text="Tasa de interés: ", font=("Helvetica", 14), anchor="w", background="white")
label_resultado_tasa.pack(anchor="w", pady=5)
label_costo_dinero = ttk.Label(frame_resultado, text="", anchor="w", background="white")
label_costo_dinero.pack(anchor="w", pady=5)
label_costo_nomina = ttk.Label(frame_resultado, text="", anchor="w", background="white")
label_costo_nomina.pack(anchor="w", pady=5)
label_costo_agencia = ttk.Label(frame_resultado, text="", anchor="w", background="white")
label_costo_agencia.pack(anchor="w", pady=5)
label_costo_oportunidad = ttk.Label(frame_resultado, text="", anchor="w", background="white")
label_costo_oportunidad.pack(anchor="w", pady=5)
label_costo_tiempo = ttk.Label(frame_resultado, text="", anchor="w", background="white")
label_costo_tiempo.pack(anchor="w", pady=5)

# Marco de historial
frame_historial = ttk.LabelFrame(ventana, text="Historial", padding=20)
frame_historial.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("#", "Nombre", "Correo", "Teléfono", "Monto", "Tasa")
tabla_historial_tree = ttk.Treeview(frame_historial, columns=columns, show="headings")
for col in columns:
    tabla_historial_tree.heading(col, text=col)
    tabla_historial_tree.column(col, width=150, anchor="center")

tabla_historial_tree.pack(fill="both", expand=True, padx=10, pady=10)

btn_eliminar = ttk.Button(frame_historial, text="Eliminar Selección", command=eliminar_seleccion, bootstyle="danger")
btn_eliminar.pack(pady=10)

ventana.mainloop()
