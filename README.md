python -m pip install --user pipx
python -m pipx ensurepath (reabrid la terminal)
pipx install pipenv
Inicializar el entorno → pipenv --python 3.13
Instalar dependencias → pipenv install pyside6 pyinstaller
Entrar al subshell →pipenv shell
python main.py
Pipfile → qué paquetes usamos
Pipfile.lock → versiones exactas
Analiza tu script Python
Encuentra las dependencias
Genera un ejecutable para tu sistema
Modos:
→onedir (por defecto): carpeta con muchos archivos
→onefile: un único .exe
pyinstaller --onefile main.py
Crea varios archivos y carpetas:
Carpeta build/
Carpeta dist/ → ENCONTRAREMOS NUESTRO EJECUTABLE
Fichero main.spec
pyinstaller --onefile --noconsole main.py
Cambiar el nombre del ejecutable → pipenv run pyinstaller --onefile --noconsole --name
MiApp main.py
Añadir icono: → pipenv run pyinstaller --onefile --noconsole --name MiApp
--icon=icono.ico main.py
Añadir carpetas: --add-data "resources;resources"
→Copia la carpeta resources dentro del paquete
→La pone en una carpeta virtual también llamada resources
Al ejecutar PyInstaller se crea main.spec.
■ Qué script se empaqueta
■ Recursos extra
■ Nombre del ejecutable
Podemos editar el .spec y luego reconstruir con:
pyinstaller main.spec
