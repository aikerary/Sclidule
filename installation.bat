@echo off

rem Copiar el archivo a la carpeta de sistema
copy "%~dp0sclidule_windows.exe" C:\Windows\System32

rem Verificar si la copia fue exitosa
if %errorlevel% equ 0 (
    echo Instalación exitosa
) else (
    echo Error al copiar el archivo sclidule.exe a C:\Windows\System32, por favor ejecuta el script como administrador
)

