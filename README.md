# Proceso de creación: reconocimiento de voz en Mini-office

Este documento resume cómo se añadió la función de reconocimiento de voz (dictado y comandos) a `practicafinalalpha.py`.

## 1. Dependencias

- `SpeechRecognition`: orquesta el reconocimiento y envía audio al backend de Google.
- `PyAudio`: abre el micrófono (wrapper de PortAudio).

En `Pipfile` y `requirements.txt` se añadieron estos paquetes. PortAudio se instaló vía Homebrew (`brew install portaudio`) para compilar PyAudio en macOS.

## 2. Integración en la UI

- Se creó la acción `Dictado por voz` y se añadió a menú **Editar** y la toolbar.
- La acción invoca `dictado_por_voz`, que controla todo el flujo de escucha y escritura.

## 3. Flujo `dictado_por_voz`

1) Importa `speech_recognition` y sale con aviso si falta.
2) Configura un `Recognizer` y abre `Microphone` para grabar (con cursor de espera y mensaje "Escuchando...").
3) Ajusta ruido ambiente y captura audio con `listen(timeout=5, phrase_time_limit=15)`, gestionando errores del micro.
4) Envía el audio a `recognize_google(language="es-ES")`.
5) Si el texto coincide con un comando, lo ejecuta; si no, inserta el dictado en el cursor.
6) Maneja errores de reconocimiento (`UnknownValueError`, `RequestError`) mostrando avisos y restaura el cursor siempre.

## 4. Comandos de voz soportados

- `negrita`: alterna peso de fuente en el cursor.
- `cursiva`: alterna cursiva.
- `subrayado`: alterna subrayado.
- `guardar` / `guardar archivo`: llama a `guardar()`.
- `nuevo` / `nuevo documento`: llama a `nuevo_documento()`.

La detección se hace en `procesar_comando_voz`, que devuelve `True` si se ejecutó un comando; de lo contrario, el texto se inserta tal cual.

## 5. Helpers de formato

- `aplicar_formato` construye un `QTextCharFormat` y lo fusiona con el cursor y el formato actual para que el estilo siga aplicándose al texto siguiente.

## 6. Detalles y buenas prácticas

- Se usa `QApplication.setOverrideCursor` para dar feedback visual y se restaura en un bloque `finally`.
- Se mostraron mensajes en la barra de estado para cada etapa (escuchando, insertado, comandos ejecutados, errores).
- Se ajustó `self.ruta_actual` para coherencia con guardado/autoguardado.

## 7. Uso rápido

1) Instala dependencias (con red): `pip install SpeechRecognition PyAudio` (o `pipenv install`).
2) Ejecuta la app: `python main.py`.
3) Pulsa "Dictado por voz", habla y usa comandos anteriores; si no hay comando, el texto se inserta.

## Archivos relevantes

- `practicafinalalpha.py`: implementación completa (copia en esta carpeta y en la raíz del proyecto).
