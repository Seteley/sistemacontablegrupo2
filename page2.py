import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget
)
from PyQt5.QtCore import QDate
from app.funciones.DiarioTransaccion import mostrar_diario, mostrar_transacciones, registrar_diario
from page4 import Page4

class CustomTableItem(QTableWidgetItem):
    def __init__(self, text):
        super().__init__(text)
        self.original_text = "(Nuevo)"
        
    def setText(self, text):
        # Ensure "(Nuevo)" prefix is always present
        if not text.startswith("(Nuevo)"):
            text = "(Nuevo)" + text
        super().setText(text)

class Page2(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None):
        """
        Página de Diarios con tabla de registros.
        :param main_window: Instancia de la ventana principal (para cambiar de página).
        """
        super().__init__(parent)
        self.main_window = main_window  # Referencia al main_window para cambiar de página
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz gráfica de la página."""
        self.page2_layout = QVBoxLayout(self)

        # ✅ Título
        self.label = QtWidgets.QLabel("📜 Diarios Registrados")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        # ✅ Barra de búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Buscar en glosas...")
        self.search_bar.setStyleSheet("""
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        """)
        self.search_bar.textChanged.connect(self.filtrar_tabla)

        # ✅ Tabla de Diarios
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["📝 Glosa", "📅 Fecha"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 5px;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #ccc;
            }
            QTableWidget::item:selected {
                background-color: #90CAF9;
                color: black;
            }
        """)

        # ✅ Botones de Acción
        self.btn_add = QPushButton("➕ Agregar Fila")
        self.btn_delete = QPushButton("🗑️ Eliminar Fila")
        self.btn_export = QPushButton("📤 Exportar CSV")
        self.btn_view_transaction = QPushButton("🔍 Ver Transacción")
        self.btn_back = QPushButton("🔙 Volver al Inicio")
        self.btn_update = QPushButton("🔄 Actualizar Diarios")  # Nuevo botón

        # ✅ Estilos de Botones
        self.btn_add.setStyleSheet("background-color: #009688; color: white; padding: 8px; border-radius: 5px;")
        self.btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; border-radius: 5px;")
        self.btn_export.setStyleSheet("background-color: #f39c12; color: white; padding: 8px; border-radius: 5px;")
        self.btn_view_transaction.setStyleSheet("background-color: #2980b9; color: white; padding: 8px; border-radius: 5px;")
        self.btn_back.setStyleSheet("background-color: #34495E; color: white; padding: 8px; border-radius: 5px;")
        self.btn_update.setStyleSheet("background-color: #8e44ad; color: white; padding: 8px; border-radius: 5px;")  # Estilo para el nuevo botón

        # ✅ Conexión de los botones
        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)
        self.btn_view_transaction.clicked.connect(self.ver_transaccion)
        self.btn_back.clicked.connect(self.volver_al_inicio)
        self.btn_update.clicked.connect(self.actualizar_diarios)  # Conectar el nuevo botón

        # ✅ Diseño de los botones
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_view_transaction)
        btn_layout.addWidget(self.btn_update)  # Agregar el nuevo botón
        btn_layout.addWidget(self.btn_back)

        # ✅ Agregar widgets al layout
        self.page2_layout.addWidget(self.label)
        self.page2_layout.addWidget(self.search_bar)
        self.page2_layout.addWidget(self.tableWidget)
        self.page2_layout.addLayout(btn_layout)
        self.setLayout(self.page2_layout)

        # Poblar la tabla inicialmente
        self.actualizar_diarios()

    def obtener_diarios(self):
        """Obtiene los datos de la base de datos y los devuelve en formato lista."""
        resultado_json = mostrar_diario()
        resultado = json.loads(resultado_json)
        return [(diario["glosa"], diario["fecha"]) for diario in resultado]

    def poblar_tabla(self, datos):
        """Llena la tabla y agrega QDateEdit en la columna Fecha."""
        self.tableWidget.setRowCount(len(datos))
        for row, (glosa, fecha) in enumerate(datos):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(glosa))

            date_widget = QDateEdit()
            date_widget.setCalendarPopup(True)
            date_widget.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))
            self.tableWidget.setCellWidget(row, 1, date_widget)

    def agregar_fila(self):
        """Agrega una nueva fila con un QDateEdit en la columna de fecha."""
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        
        # Usar CustomTableItem para la glosa
        nuevo_item = CustomTableItem("(Nuevo)")
        nuevo_item.setFlags(nuevo_item.flags() | QtCore.Qt.ItemIsEditable)
        self.tableWidget.setItem(row, 0, nuevo_item)

        date_widget = QDateEdit()
        date_widget.setCalendarPopup(True)
        date_widget.setDate(QDate.currentDate())
        self.tableWidget.setCellWidget(row, 1, date_widget)

    def eliminar_fila(self):
        """Elimina la fila seleccionada."""
        row = self.tableWidget.currentRow()
        if row >= 0:
            self.tableWidget.removeRow(row)
        else:
            QMessageBox.warning(self, "Error", "Seleccione una fila para eliminar.")

    def filtrar_tabla(self):
        """Filtra la tabla en base al texto ingresado en la barra de búsqueda."""
        filtro = self.search_bar.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            if item and filtro in item.text().lower():
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)

    def exportar_csv(self):
        """Exporta los datos de la tabla a un archivo CSV."""
        path, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "", "Archivos CSV (*.csv)")
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write("Glosa,Fecha\n")
                for row in range(self.tableWidget.rowCount()):
                    glosa = self.tableWidget.item(row, 0).text()
                    fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")
                    file.write(f"{glosa},{fecha}\n")
            QMessageBox.information(self, "Éxito", "El archivo CSV ha sido guardado correctamente.")
 
    def actualizar_estado_boton(self):
        """Habilita o deshabilita el botón dependiendo de si hay un diario seleccionado."""
        if self.tableWidget.currentRow() >= 0:
            self.btn_view_transaction.setEnabled(True)
        else:
            self.btn_view_transaction.setEnabled(False)

    def ver_transaccion(self):
        """Muestra las transacciones de un diario seleccionado."""
        diarios_disponibles = self.obtener_diarios()

        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione un diario para ver las transacciones.")
            return
        
        glosa = self.tableWidget.item(row, 0).text()
        fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")

        if (glosa, fecha) not in diarios_disponibles:
            QMessageBox.warning(self, "Error", "El diario seleccionado no es válido.")
            return

        # Cambiar a la nueva ventana Page4
        self.main_window.stackedWidget.addWidget(Page4(self.main_window, glosa, fecha))
        self.main_window.stackedWidget.setCurrentIndex(self.main_window.stackedWidget.count() - 1)

    def volver_al_inicio(self):
        """Vuelve a la página principal en el stackedWidget."""
        self.main_window.stackedWidget.setCurrentIndex(0)

    def actualizar_diarios(self):
        """Actualiza la tabla y registra los nuevos diarios."""
        # Primero, registrar los nuevos diarios
        for row in range(self.tableWidget.rowCount()):
            glosa_item = self.tableWidget.item(row, 0)
            if glosa_item and glosa_item.text().startswith("(Nuevo)"):
                fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")
                glosa = glosa_item.text().replace("(Nuevo)", "").strip()  # Remover el prefijo
                
                try:
                    registrar_diario(fecha, glosa)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error al registrar el diario: {str(e)}")

        # Luego, actualizar la tabla con los datos más recientes
        datos = self.obtener_diarios()
        self.poblar_tabla(datos)