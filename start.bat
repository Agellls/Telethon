@echo off
setlocal enabledelayedexpansion

echo.
echo 🚀 Telethon Resend - Docker Startup
echo.

REM Check if .env file exists
if not exist .env (
    echo ❌ File .env tidak ditemukan!
    echo 📝 Salin .env.example ke .env dan isi dengan credentials Anda
    echo    copy .env.example .env
    pause
    exit /b 1
)

REM Load and validate .env file
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" (
        set "%%a=%%b"
    )
)

REM Check required variables
set required_vars=API_ID API_HASH SOURCE_CHAT TARGET_GROUP
set missing_vars=

for %%var in (%required_vars%) do (
    if not defined %%var (
        if not "!missing_vars!"=="" (
            set "missing_vars=!missing_vars!, %%var"
        ) else (
            set "missing_vars=%%var"
        )
    )
)

if not "!missing_vars!"=="" (
    echo ❌ Harap penuhi kebutuhan environment terlebih dahulu!
    echo ❌ Missing: !missing_vars!
    pause
    exit /b 1
)

echo ✅ Environment variables valid
echo 🐳 Starting Docker container...
echo.

REM Run docker-compose
docker-compose up --build

pause
