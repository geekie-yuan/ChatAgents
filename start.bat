@echo off
echo ===================================
echo Yuan's Chat Agents - 启动脚本
echo ===================================
echo.

REM 检查虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境，请先运行 setup.bat
    pause
    exit /b 1
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 检查 .env 文件
if not exist ".env" (
    echo [警告] 未找到 .env 文件，请确保已配置 API 密钥
    echo.
)

echo [1/2] 启动后端服务...
echo.
start "Backend" cmd /k "venv\Scripts\activate.bat && python app.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

echo [2/2] 启动前端应用...
echo.
start "Frontend" cmd /k "venv\Scripts\activate.bat && streamlit run streamlit_app.py"

echo.
echo ===================================
echo 应用已启动！
echo ===================================
echo 前端: http://localhost:8501
echo 后端: http://localhost:8080
echo ===================================
echo.
echo 按任意键关闭此窗口...
pause >nul
