@ECHO OFF
@CHCP 65001
SET BASE_DIR=%~dp0
CD /d %BASE_DIR%

if exist "%BASE_DIR%python3.11" (
    %BASE_DIR%python3.11\python.exe %BASE_DIR%main.py
) else (
    python main.py
)
