@echo off

chcp 65001
cls

".\Venv\Scripts\python.exe" ".\main.py"

echo "按任意键退出程序..."
pause > nul
exit
