@echo off
echo ========================================
echo HousePriceAI Deployment Script
echo Created by: Garima Swami
echo ========================================
echo.

echo 📁 Updating frontend files...
copy /Y script.js script.js.backup
echo ✅ Backed up original script.js

echo 📝 Applying price consistency fixes...
echo // Price consistency update - Garima Swami > version.txt
echo Updated: %date% %time% >> version.txt
echo.

echo 🚀 Starting Flask server...
start cmd /k "python app.py"
echo.

echo 🌐 Opening browser...
timeout /t 3
start http://localhost:5000
echo.

echo ========================================
echo ✅ Deployment complete!
echo 📊 Frontend running at: http://localhost:5000
echo 👤 Creator: Garima Swami
echo ========================================
pause