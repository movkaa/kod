@echo off
setlocal EnableDelayedExpansion

:: Создаем 10 текстовых файлов с надписью "тебе конец"
for /l %%i in (1,1,10) do (
    echo тебе конец > "file%%i.txt"
)

:: Открываем их в блокноте
for /l %%i in (1,1,10) do (
    start "" notepad.exe "file%%i.txt"
    timeout /t 1 >nul
)

:: Задержка для открытия окон
timeout /t 2 >nul

:: Расположение окон по разным частям экрана
set coords[1]="0,0,400,300"
set coords[2]="400,0,400,300"
set coords[3]="800,0,400,300"
set coords[4]="0,300,400,300"
set coords[5]="400,300,400,300"
set coords[6]="800,300,400,300"
set coords[7]="0,600,400,300"
set coords[8]="400,600,400,300"
set coords[9]="800,600,400,300"
set coords[10]="1200,300,400,300"

for /l %%i in (1,1,10) do (
    for /f "tokens=1,2,3,4" %%a in ("!coords[%%i]!") do (
        powershell -command "
        Add-Type -Namespace WinAPI -Name User32 -MemberDefinition '
        [DllImport(\"user32.dll\")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight);
        '
        \$hwnd = (Get-Process | Where-Object { \$_.MainWindowTitle -like '*file%%i.txt*' }).MainWindowHandle
        [WinAPI.User32]::MoveWindow(\$hwnd, %%a, %%b, %%c, %%d, \$true)
        "
    )
)

:: Ждем 10 секунд, затем закрываем блокноты
timeout /t 10 >nul

:: Закрываем блокноты по имени файла
taskkill /im notepad.exe /fi "WINDOWTITLE eq file*.txt" /f

echo Все закрыто и файлы удаляются.

:: Удаляем файлы
del "file*.txt"

pause