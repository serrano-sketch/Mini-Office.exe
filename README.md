# Mini Office — Creación del ejecutable

## Requisitos
- Python 3.13
- pipx y pipenv

## 1) Preparación de herramientas
```bash
python -m pip install --user pipx
python -m pipx ensurepath   # reabre la terminal
pipx install pipenv
```

## 2) Crear el entorno
```bash
pipenv --python 3.13
```

## 3) Instalar dependencias
```bash
pipenv install pyside6 pyinstaller
```

## 4) Probar la app en el entorno
```bash
pipenv shell
python main.py
```

Notas:
- `Pipfile`: paquetes usados
- `Pipfile.lock`: versiones exactas

## 5) Construcción del ejecutable (PyInstaller)
Modos:
- onedir (por defecto): carpeta con muchos archivos
- onefile: archivo único `.exe`

Básico:
```bash
pyinstaller --onefile main.py
```
Genera:
- `build/`
- `dist/`  ← aquí queda el `.exe`
- `main.spec`

Variantes útiles:
```bash
pyinstaller --onefile --noconsole main.py
pipenv run pyinstaller --onefile --noconsole --name MiApp main.py
pipenv run pyinstaller --onefile --noconsole --name MiApp --icon=icono.ico main.py
pipenv run pyinstaller --onefile --noconsole --name MiApp --add-data "resources;resources" main.py
```
- `--add-data "resources;resources"` copia la carpeta `resources` al paquete

Spec file:
- PyInstaller crea `main.spec` (script, recursos, nombre)
- Puedes editarlo y reconstruir:
```bash
pyinstaller main.spec
```
