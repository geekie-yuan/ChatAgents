@echo off
echo ===================================
echo Yuan's Chat Agents - 安装脚本
echo ===================================
echo.

REM 检查 Python 版本
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.11+
    pause
    exit /b 1
)

echo [1/4] 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo [错误] 创建虚拟环境失败
    pause
    exit /b 1
)
echo [完成] 虚拟环境已创建

echo.
echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat
echo [完成] 虚拟环境已激活

echo.
echo [3/4] 安装依赖包...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)
echo [完成] 依赖包已安装

echo.
echo [4/4] 配置环境变量...
if not exist ".env" (
    copy .env.sample .env
    echo [完成] 已创建 .env 文件
    echo [提示] 请编辑 .env 文件，填入您的 API 密钥
) else (
    echo [跳过] .env 文件已存在
)

echo.
echo ===================================
echo 安装完成！
echo ===================================
echo 下一步：
echo 1. 编辑 .env 文件，填入 API 密钥
echo 2. 运行 start.bat 启动应用
echo ===================================
echo.
pause
