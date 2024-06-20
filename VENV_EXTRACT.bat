@echo off

chcp 65001
cls

call .\Scripts\activate.bat

pip freeze > requirements.txt
pip download -r requirements.txt -d ./wheels

echo "---------- FINISHED ----------"
echo "提取产物：requirements.txt清单 + wheels文件夹"
echo "请把这两个东西保存好，可以用来重建venv"
echo "按任意键退出..."
pause > nul
