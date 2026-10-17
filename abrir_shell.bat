@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo Se abrira el shell de Django. Copia las lineas y pega la captura en el registro.
echo.
py -X utf8 manage.py shell
