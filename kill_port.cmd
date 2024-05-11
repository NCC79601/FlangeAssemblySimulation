@echo off
echo Checking if port 65500 is in use...
for /f "tokens=5" %%i in ('netstat -ano ^| findstr :65500') do (
    echo Port 65500 is being used by process with PID %%i, preparing to terminate the process...
    taskkill /F /PID %%i
    if %errorlevel% equ 0 (
        echo Process terminated successfully!
    ) else (
        echo Failed to terminate the process! Please check permissions or process status.
    )
)
pause