@echo off
setlocal

:: 📍 Настройки
set NAME=tgcleaner
set SCRIPT=tg_cleaner.py
set ICON=tg.ico

:: 🔨 Сборка .exe с иконкой
echo 🔨 Сборка .exe...
pyinstaller --onefile --console --icon=%ICON% --name %NAME% %SCRIPT%

:: 🗃️ Удаление временных файлов
echo 🧹 Чистим...
rmdir /s /q build >nul 2>&1
del %NAME%.spec >nul 2>&1

:: 🧷 Создание ярлыка на рабочем столе
echo 📎 Создаём ярлык на рабочем столе...
set LINK="%USERPROFILE%\Desktop\%NAME%.lnk"
set TARGET=%CD%\dist\%NAME%.exe

powershell -NoProfile -Command ^
  "$s = (New-Object -COM WScript.Shell).CreateShortcut(%LINK%); ^
   $s.TargetPath = '%TARGET%'; ^
   $s.IconLocation = '%TARGET%'; ^
   $s.Save()"

echo ✅ Готово! .exe и ярлык созданы.
pause
endlocal
