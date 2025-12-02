# Generar mini-office.exe

Este documento explica dos formas de generar un ejecutable `mini-office.exe` similar al ubicado en `~\.local\bin\mini-office.exe`.

## Opción A — Shim con pipx/pip (recomendado)

- Requisitos
  - Python 3.8+ y `pip`
  - `pipx` (genera shims en `~\.local\bin`)
  - Asegurar `~\.local\bin` en el `PATH`

- Instalar herramientas
  - `py -m pip install --upgrade pip build pipx`

- Añadir `~\.local\bin` al PATH del usuario (si falta)
  - `if (-not ($env:Path -split ";" | Where-Object {$_ -match "\\.local\\bin$"})) { [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\\.local\\bin", "User"); "PATH actualizado. Cierra y abre la terminal." }`

- Estructura mínima del proyecto
  - `mini_office/cli.py` con una función `main()`
  - `pyproject.toml` con entry point de consola
  - Ejemplo:
    - `mini_office/cli.py`
      - `def main():`
      - `    print("Mini Office listo")`
    - `pyproject.toml`
      - `[build-system]`
      - `requires = ["setuptools", "wheel"]`
      - `build-backend = "setuptools.build_meta"`
      - `[project]`
      - `name = "mini-office"`
      - `version = "0.1.0"`
      - `description = "Mini Office CLI"`
      - `requires-python = ">=3.8"`
      - `[project.scripts]`
      - `mini-office = "mini_office.cli:main"`

- Construir (opcional) o instalar en editable
  - Opción rápida (instalar desde el fuente con pipx):
    - `pipx install .`
  - O usando wheel:
    - `py -m build`
    - `pipx install dist\mini_office-0.1.0-py3-none-any.whl`

- Verificar instalación
  - `Get-Command mini-office`
  - `mini-office --help`
  - `where mini-office`  (debería apuntar a `~\.local\bin\mini-office.exe`)

- Actualizar/desinstalar
  - `pipx upgrade mini-office`
  - `pipx reinstall mini-office`
  - `pipx uninstall mini-office`

- Notas
  - Con `pip install --user .` también se crea el shim en `~\AppData\Roaming\Python\PythonXY\Scripts`, pero `pipx` es más limpio y aísla dependencias.
  - El `.exe` en `~\.local\bin` es un lanzador (shim) que ejecuta el entry point del paquete instalado.

## Opción B — EXE standalone con PyInstaller

- Requisitos
  - Python 3.8+ y `pip`

- Instalar PyInstaller
  - `py -m pip install --upgrade pyinstaller`

- Comando de compilación (un solo binario)
  - `py -m PyInstaller --onefile --name mini-office mini_office/cli.py`

- Artefactos generados
  - `dist\mini-office.exe`  (ejecutable final)

- Probar
  - ` .\dist\mini-office.exe`
  - Opcional: mover a `~\.local\bin` o a otra carpeta en el PATH:
    - `New-Item -ItemType Directory -Force $env:USERPROFILE\.local\bin | Out-Null`
    - `Move-Item -Force dist\mini-office.exe $env:USERPROFILE\.local\bin\mini-office.exe`

- Empaquetar con datos/recursos (si aplica)
  - Añade `--add-data "ruta\\origen;destino_relativo"` por cada recurso.
  - Ejemplo: `py -m PyInstaller --onefile --name mini-office --add-data "assets;assets" mini_office/cli.py`

## Solución de problemas

- `mini-office` no se reconoce
  - Asegura que `~\.local\bin` está en PATH y reinicia la terminal.
  - `Get-Command mini-office -All`
- Conflictos de versiones
  - `pipx uninstall mini-office && pipx install .`
- Ver dependencia rota
  - `pipx runpip mini-office freeze`

## Subir README a Git

- Clonar:
  - `git clone https://github.com/serrano-sketch/Mini-Office.exe.git`
  - `cd Mini-Office.exe`
- Crear README.md (PowerShell):
  - `$content = @' ...contenido de este README... '@`
  - `Set-Content -Encoding UTF8 -Path README.md -Value $content`
- Commit y push (ajusta rama si es `master`):
  - `git add README.md`
  - `git commit -m "docs: add README for building mini-office.exe"`
  - `git push origin main`
