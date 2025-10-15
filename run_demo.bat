@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  Todo & Pomodoro Widget Demo - Quick Start
REM ============================================

set "ROOT=%~dp0"
pushd "%ROOT%"

echo.
echo ============================================
echo   Todo & Pomodoro Widget Demo - Quick Start
echo ============================================
echo.

where py >nul 2>&1
if errorlevel 1 (
  echo [ERROR] 未找到 Python。請先從 https://www.python.org/downloads/ 安裝 Python 3.10 或更新版本。
  goto :END
)

where node >nul 2>&1
if errorlevel 1 (
  echo [ERROR] 未找到 Node.js。請先從 https://nodejs.org/ 下載並安裝 LTS 版本。
  goto :END
)

where npm >nul 2>&1
if errorlevel 1 (
  echo [ERROR] 未找到 npm。請確認 Node.js 安裝包含 npm。
  goto :END
)

echo.
echo [1/4] 準備後端虛擬環境...
pushd backend
if not exist .venv (
  echo     -> 建立虛擬環境 .venv
  py -m venv .venv
)
echo     -> 安裝後端依賴 (pip install)
call .venv\Scripts\python.exe -m pip install --upgrade pip
call .venv\Scripts\python.exe -m pip install -r requirements.txt
popd

echo.
echo [2/4] 準備前端依賴...
pushd frontend
if not exist node_modules (
  echo     -> 第一次安裝前端依賴 (npm install)
  call npm install
) else (
  echo     -> 已檢測到 node_modules，跳過 npm install
)
popd

echo.
echo [3/4] 啟動後端伺服器 (會開啟新視窗)...
start "Widget Backend" cmd /k "cd /d "%ROOT%backend" && call .venv\Scripts\activate.bat && uvicorn app.main:app --reload"

echo.
echo [4/4] 啟動前端開發伺服器 (會開啟新視窗)...
start "Widget Frontend" cmd /k "cd /d "%ROOT%frontend" && npm run dev"

echo.
echo 一切準備完成！請在瀏覽器開啟 http://127.0.0.1:5173/ 查看小組件。
echo 後端 API 位於 http://127.0.0.1:8000/docs
echo.
echo 關閉時只需在各自視窗中按 Ctrl+C 或直接關閉視窗即可。
echo.
pause

:END
popd
endlocal
