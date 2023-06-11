# Requisitos

# Entorno virtual para Python3

Es necesario para poder instalar las librerías de manera aislada del sistema operativo.
```bash
sudo apt install -y git zip unzip python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev gradle openjdk-17-jdk python3-kivy virtualenv
# Creamos la carpeta del entorno en la raíz del proyecto
python3 -m virtualenv kivy_venv

# Activamos dicho entorno
source kivy_venv/bin/activate
# Debería aparecer algo en la consola como lo siguiente
(kivy_venv) usuario@usuario-Standard-PC-Q35-ICH9-2009:~/android1/kivy_venv
# Instalamos las dependencias necesarias para Kivy
# Actualizamos pip
python3 -m pip install --upgrade pip setuptools virtualenv
# Instalando las librerías de Kivy
python3 -m pip install pyjnius "kivy[base]"

```

# Crear un APK - Crear el entorno de buildozer

Para crear un APK necesitamos crear un entorno de buildozer, para ello dentro del entorno virtual debemos instalar su paquete y dentro de la 
carpeta de la app debemos ejecutar el último comando.

```bash
# Instalamos el paquete de buildozer con el entorno activado.
python3 -m pip install buildozer cython
# Entramos en el directorio de la app
cd app/
# Iniciamos los parametros de la aplicacion
buildozer init
# Creará un fichero llamado buildozer.spec, que debemos editar para cambiar el nombre de la app y poner la appi adecuada de Android.
# Información de la API de Android -> https://apilevels.com/
# Para ello editamos con nano o cualquier otro editor los ajustes
nano buildozer.spec
```
# Compilar la aplicacion
Para compilar el APK, debemos ejecutar los siguientes comandos dentro del entorno.

```bash
# Crear un APK 
buildozer -v android debug
# Copiar el apk, se encuentra en una carpeta llamada bin
cp bin/NombreDeTuAplicación-0.1-debug.apk /path
```
