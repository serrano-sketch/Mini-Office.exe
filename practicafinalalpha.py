from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget,
                               QToolBar, QMenuBar, QMessageBox, QMenu, QStatusBar,
                               QFileDialog, QLineEdit, QPushButton, QWidget,
                               QHBoxLayout, QVBoxLayout, QColorDialog, QFontDialog, QLabel)
from PySide6.QtGui import (
    QAction,
    QKeySequence,
    QIcon,
    QTextCursor,
    QTextDocument,
    QFont,
    QTextCharFormat,
)
from PySide6.QtCore import Qt, QTimer
import sys
import os

class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ruta_actual = None
        self.cambios_pendientes = False
        self.setWindowTitle("Mini-ofice")
        self.resize(900, 600)


        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)
        self.editor.setPlaceholderText("Aqui el texto: ")
        self.editor.textChanged.connect(self.texto_cambiado)


        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.label_palabras = QLabel("Palabras: 0")
        self.status.addPermanentWidget(self.label_palabras)


        self.temporizador= QTimer()
        self.temporizador.setSingleShot(True)
        self.temporizador.timeout.connect(self.actualizar_contador)
        self.actualizar_contador()


        self.timer_autoguardar = QTimer(self)
        self.timer_autoguardar.timeout.connect(self.autoguardar)
        self.timer_autoguardar.start(10000)


        self.crear_acciones()
        self.crear_menus()
        self.crear_toolbar()
        self.crear_dock_busqueda()
        self.conectar_busqueda()


        




    
    
    def actualizar_contador(self):
        texto = self.editor.toPlainText().strip()
        if texto == "":
            cuenta = 0
        else:
            cuenta = len([p for p in texto.split() if p])
        self.label_palabras.setText(f"Palabras: {cuenta}")



    def crear_acciones(self):
        self.accion_nuevo = QAction("Nuevo", self)
        self.accion_nuevo.setShortcut(QKeySequence.New)
        self.accion_nuevo.triggered.connect(self.nuevo_documento)
        self.accion_nuevo.setIcon(QIcon.fromTheme("document-new"))

        self.accion_guardar = QAction("Guardar", self)
        self.accion_guardar.setShortcut(QKeySequence.Save)
        self.accion_guardar.triggered.connect(self.guardar)
        self.accion_guardar.setIcon(QIcon.fromTheme("document-save"))
        

        self.accion_salir = QAction("Salir", self)
        self.accion_salir.setShortcut(QKeySequence.Quit)
        self.accion_salir.triggered.connect(self.close) 
        self.accion_salir.setIcon(QIcon.fromTheme("application-exit"))


        self.accion_copiar = QAction("Copiar", self)
        self.accion_copiar.setShortcut(QKeySequence.Copy)
        self.accion_copiar.triggered.connect(self.editor.copy)
        self.accion_copiar.setIcon(QIcon.fromTheme("edit-copy"))


        self.accion_pegar = QAction("Pegar", self)
        self.accion_pegar.setShortcut(QKeySequence.Paste)
        self.accion_pegar.triggered.connect(self.editor.paste)
        self.accion_pegar.setIcon(QIcon.fromTheme("edit-paste"))

        self.accion_cortar = QAction("Cortar", self)
        self.accion_cortar.setShortcut(QKeySequence.Cut)
        self.accion_cortar.triggered.connect(self.editor.cut) 
        self.accion_cortar.setIcon(QIcon.fromTheme("edit-cut"))  

        self.accion_abrir = QAction("Abrir", self)
        self.accion_abrir.setShortcut(QKeySequence.Open)
        self.accion_abrir.triggered.connect(self.abrir_archivo)
        self.accion_abrir.setIcon(QIcon.fromTheme("document-open"))

        self.accion_color_fondo =QAction ("Color de fondo", self)
        self.accion_color_fondo.triggered.connect(self.cambiar_color_fondo)
        self.accion_color_fondo.setIcon(QIcon("icons/Background.png"))

        self.accion_fuente = QAction("Cambiar fuente", self)
        self.accion_fuente.triggered.connect(self.cambiar_fuente)
        self.accion_fuente.setIcon(QIcon("icons/font-type.png"))

        self.accion_buscar = QAction("Buscar / Reemplazar", self)
        self.accion_buscar.setShortcut(QKeySequence.Find)
        self.accion_buscar.triggered.connect(self.toggle_dock_busqueda)
        self.accion_buscar.setIcon(QIcon.fromTheme("edit-find"))

        self.accion_dictado = QAction("Dictado por voz", self)
        self.accion_dictado.triggered.connect(self.dictado_por_voz)
        self.accion_dictado.setIcon(QIcon.fromTheme("media-record"))




        self.accion_info = QAction("Acerca de Mini Word", self)
        self.accion_info.triggered.connect(self.mostrar_info)
        self.accion_info.setIcon(QIcon.fromTheme("help-about"))




    def crear_menus(self):
        menubar = self.menuBar()


        menu_archivo = menubar.addMenu("Archivo")
        menu_archivo.addAction(self.accion_nuevo)
        menu_archivo.addAction(self.accion_abrir)
        menu_archivo.addAction(self.accion_guardar)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        
        

        menu_editar = menubar.addMenu("Editar")
        menu_editar.addAction(self.accion_copiar)
        menu_editar.addAction(self.accion_pegar)
        menu_editar.addAction(self.accion_cortar)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accion_buscar)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accion_dictado)

        menu_formato = menubar.addMenu("Formato")
        menu_formato.addAction(self.accion_color_fondo)
        menu_formato.addAction(self.accion_fuente)

       


        

        menu_ayuda = menubar.addMenu("Ayuda")
        menu_ayuda.addAction(self.accion_info)



    def crear_toolbar(self):
        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)
        toolbar.addAction(self.accion_nuevo)
        toolbar.addAction(self.accion_abrir)
        toolbar.addAction(self.accion_guardar)
        toolbar.addSeparator()
        toolbar.addAction(self.accion_copiar)
        toolbar.addAction(self.accion_pegar)
        toolbar.addAction(self.accion_cortar)
        toolbar.addSeparator()
        toolbar.addAction(self.accion_buscar)
        toolbar.addAction(self.accion_color_fondo)
        toolbar.addAction(self.accion_fuente)
        toolbar.addAction(self.accion_dictado)

    def crear_dock_busqueda(self):
        
        self.dock = QDockWidget("Buscar / Reemplazar", self)
        self.dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)

        
        contenedor = QWidget()
        layout_principal = QVBoxLayout()

        fila_buscar = QHBoxLayout()
        self.caja_buscar = QLineEdit()
        self.caja_buscar.setPlaceholderText("Texto a buscar...")
        self.boton_buscar_siguiente = QPushButton("Buscar siguiente")
        self.boton_buscar_anterior = QPushButton("Buscar anterior")
        fila_buscar.addWidget(self.caja_buscar)
        fila_buscar.addWidget(self.boton_buscar_siguiente)
        fila_buscar.addWidget(self.boton_buscar_anterior)
        layout_principal.addLayout(fila_buscar)

        
        fila_reemplazar = QHBoxLayout()
        self.caja_reemplazar = QLineEdit()
        self.caja_reemplazar.setPlaceholderText("Reemplazar con...")
        self.boton_reemplazar = QPushButton("Reemplazar")
        self.boton_reemplazar_todo = QPushButton("Reemplazar todo")
        fila_reemplazar.addWidget(self.caja_reemplazar)
        fila_reemplazar.addWidget(self.boton_reemplazar)
        fila_reemplazar.addWidget(self.boton_reemplazar_todo)
        layout_principal.addLayout(fila_reemplazar)

        
        self.etiqueta_info = QLabel("")
        layout_principal.addWidget(self.etiqueta_info)

        contenedor.setLayout(layout_principal)
        self.dock.setWidget(contenedor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.hide()  

    def toggle_dock_busqueda(self):
        
        self.dock.setVisible(not self.dock.isVisible())

    def conectar_busqueda(self):
        
        self.boton_buscar_siguiente.clicked.connect(self.buscar_siguiente)
        self.boton_buscar_anterior.clicked.connect(self.buscar_anterior)
        self.boton_reemplazar.clicked.connect(self.reemplazar_uno)
        self.boton_reemplazar_todo.clicked.connect(self.reemplazar_todo)

    def buscar_siguiente(self):
        texto = self.caja_buscar.text()
        if not texto:
            return

        cursor = self.editor.document().find(texto, self.editor.textCursor())
        if cursor.isNull():
            
            cursor = self.editor.document().find(texto)
            if cursor.isNull():
                self.etiqueta_info.setText("No se encontró el texto")
                return
            else:
                self.etiqueta_info.setText("Reiniciado desde el inicio")

        self.editor.setTextCursor(cursor)
        self.etiqueta_info.setText("Coincidencia encontrada")


    def buscar_anterior(self):
        texto = self.caja_buscar.text()
        if not texto:
            return

        cursor = self.editor.textCursor()
        pos_actual = cursor.selectionStart()

        
        doc = self.editor.document()
        posiciones = []
        cur = QTextCursor(doc)
        while True:
            cur = doc.find(texto, cur)
            if cur.isNull():
                break
            posiciones.append(cur.selectionStart())

        prev = max([p for p in posiciones if p < pos_actual], default=None)
        if prev is None:
            self.etiqueta_info.setText("No se encontró anterior")
            return

        nuevo_cursor = self.editor.textCursor()
        nuevo_cursor.setPosition(prev)
        nuevo_cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(texto))
        self.editor.setTextCursor(nuevo_cursor)
        self.etiqueta_info.setText("Coincidencia anterior encontrada")


    def reemplazar_uno(self):
        buscar = self.caja_buscar.text()
        reemplazo = self.caja_reemplazar.text()
        if not buscar:
            return

        cursor = self.editor.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == buscar:
            cursor.insertText(reemplazo)
            self.etiqueta_info.setText("Texto reemplazado")
        else:
            self.buscar_siguiente()


    def reemplazar_todo(self):
        buscar = self.caja_buscar.text()
        reemplazo = self.caja_reemplazar.text()
        if not buscar:
            return

        texto = self.editor.toPlainText()
        reemplazado = texto.replace(buscar, reemplazo)
        self.editor.setPlainText(reemplazado)
        self.etiqueta_info.setText("Todos los reemplazos realizados")


    

    def nuevo_documento(self):
        self.editor.clear()
        self.ruta_actual = None
        self.cambios_pendientes = False
        self.setWindowTitle("Mini-ofice — Sin título")
        self.status.showMessage("Nuevo documento", 2000)

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir documento", "", "Archivos de texto (*.txt);;Todos los archivos (*)")

        if not ruta:
            return

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                texto = archivo.read()
                self.editor.setPlainText(texto)
                self.ruta_actual = ruta
                self.cambios_pendientes = False
                self.setWindowTitle(f"Mini-ofice — {os.path.basename(ruta)}")
                self.status.showMessage(f"Archivo abierto: {ruta}", 4000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar(self):
        if not self.ruta_actual:
            ruta, _ = QFileDialog.getSaveFileName(self, "Guardar documento", "", "Archivos de texto (*.txt)")
            if not ruta:
                self.status.showMessage("Guardado cancelado", 2000)
                return
            self.ruta_actual = ruta

        try:
            with open(self.ruta_actual, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.status.showMessage(f"Archivo guardado: {self.ruta_actual}", 3000)
            self.cambios_pendientes = False
            self.setWindowTitle(f"Mini-ofice — {os.path.basename(self.ruta_actual)}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el archivo:\n{e}")

    
    def cambiar_color_fondo(self):
        
        color = QColorDialog.getColor(parent=self, title="Seleccionar color de fondo")

        
        if not color.isValid():
            return

        
        self.editor.setStyleSheet(f"QTextEdit {{ background-color: {color.name()}; }}")
        self.status.showMessage(f"Color de fondo cambiado a {color.name()}", 3000)


    def cambiar_fuente(self):
        
        fuente, ok = QFontDialog.getFont(self.editor.font(), self, "Seleccionar fuente")

        if ok:  
            self.editor.setFont(fuente)
            self.status.showMessage(f"Fuente cambiada a {fuente.family()}", 3000)

    def aplicar_formato(self, *, bold=None, italic=None, underline=None):
        """Aplica formato al cursor actual y lo deja activo para texto nuevo."""
        cursor = self.editor.textCursor()
        fmt = QTextCharFormat()
        if bold is not None:
            fmt.setFontWeight(QFont.Bold if bold else QFont.Normal)
        if italic is not None:
            fmt.setFontItalic(italic)
        if underline is not None:
            fmt.setFontUnderline(underline)

        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)

    def procesar_comando_voz(self, texto):
        comando = texto.lower().strip()

        if comando == "negrita":
            activar = self.editor.fontWeight() != QFont.Bold
            self.aplicar_formato(bold=activar)
            self.status.showMessage(f"Negrita {'activada' if activar else 'desactivada'}", 3000)
            return True

        if comando == "cursiva":
            activar = not self.editor.fontItalic()
            self.aplicar_formato(italic=activar)
            self.status.showMessage(f"Cursiva {'activada' if activar else 'desactivada'}", 3000)
            return True

        if comando == "subrayado":
            activar = not self.editor.fontUnderline()
            self.aplicar_formato(underline=activar)
            self.status.showMessage(f"Subrayado {'activado' if activar else 'desactivado'}", 3000)
            return True

        if comando in {"guardar archivo", "guardar"}:
            self.guardar()
            return True

        if comando in {"nuevo documento", "nuevo"}:
            self.nuevo_documento()
            return True

        return False

    def dictado_por_voz(self):
        try:
            import speech_recognition as sr
        except ImportError:
            QMessageBox.warning(self, "Dependencia faltante", "Instala 'SpeechRecognition' y 'PyAudio' para usar el dictado por voz.")
            return

        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                self.status.showMessage("Escuchando...", 2000)
                QApplication.setOverrideCursor(Qt.WaitCursor)
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Micrófono", f"No se pudo capturar audio:\n{e}")
            return

        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            if not self.procesar_comando_voz(texto):
                cursor = self.editor.textCursor()
                cursor.insertText(texto + " ")
                self.editor.setTextCursor(cursor)
                self.status.showMessage("Dictado insertado", 3000)
            else:
                self.status.showMessage(f"Comando por voz ejecutado: {texto}", 3000)
        except sr.UnknownValueError:
            QMessageBox.information(self, "Dictado", "No se entendió el audio.")
        except sr.RequestError as e:
            QMessageBox.warning(self, "Dictado", f"No se pudo procesar el audio:\n{e}")
        finally:
            QApplication.restoreOverrideCursor()

    def texto_cambiado(self):
        self.cambios_pendientes = True
        self.temporizador.start(200)



    def autoguardar(self):
        if not self.cambios_pendientes:
            return

        if self.ruta_actual:
            try:
                with open(self.ruta_actual, "w", encoding="utf-8") as archivo:
                    archivo.write(self.editor.toPlainText())
                self.status.showMessage(f"Autoguardado en {self.ruta_actual}", 2000)
                self.cambios_pendientes = False
            except Exception as e:
                self.status.showMessage(f"Error al autoguardar: {e}", 4000)
        else:
            self.status.showMessage("Autoguardado pendiente (sin nombre)", 2000)



    def mostrar_info(self):
        QMessageBox.information(self, "Acerca de", "Mini Word creado por Serra ")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()


    ventana.show()
    sys.exit(app.exec())
