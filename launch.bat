@echo off

REM Crear entorno virtual si no existe
IF NOT EXIST "env" (
    echo Creando entorno virtual...
    python -m venv env
)

REM Activar entorno virtual
call env\Scripts\activate

REM Instalar requerimientos si existen
IF EXIST ".\Project\requirements.txt" (
    echo Instalando dependencias...
    pip install -r .\Project\requirements.txt
)

echo === Entorno listo.
REM pero si desea mantener la consola abierta para que siga dentro del venv
cmd /k