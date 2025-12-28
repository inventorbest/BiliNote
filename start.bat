@echo off
chcp 65001 >nul
title BiliNote 启动器

echo ========================================
echo      BiliNote 启动脚本
echo ========================================
echo.

:: 检查是否在正确的目录
if not exist "backend" (
    echo [错误] 请在 BiliNote 根目录运行此脚本！
    pause
    exit /b 1
)

:: 启动后端
echo [1/2] 正在启动后端服务...
cd backend
start "BiliNote Backend" cmd /k "python main.py"
cd ..

:: 等待后端启动
timeout /t 3 /nobreak >nul

:: 启动前端
echo [2/2] 正在启动前端服务...
cd BillNote_frontend
start "BiliNote Frontend" cmd /k "pnpm dev"
cd ..

echo.
echo ========================================
echo  启动完成！
echo  后端地址: http://localhost:8483
echo  前端地址: http://localhost:5173
echo ========================================
echo.
echo 按任意键关闭此窗口（服务会继续运行）...
pause >nul
