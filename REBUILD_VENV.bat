@echo off

chcp 65001
cls

echo "---------- REBUILD ----------"
echo "确保你有：requirements.txt清单 + wheels文件夹"
echo "请把这两个东西放在REBUILD_VENV.bat同一个目录下"
echo "准备好了，按任意键开始重建..."
pause > nul

python -m venv Venv
call .\Venv\Scripts\activate

pip install --no-index --find-links=./wheels -r requirements.txt

echo "---------- FINISHED ----------"
echo "重建完成，建好的venv路径为：./Venv/"
echo "按任意键退出..."
pause > nul
