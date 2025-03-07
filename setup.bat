@echo off

:: Kiểm tra Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python không được cài đặt. Vui lòng cài đặt Python trước!
    exit /b 1
)

:: Kiểm tra pip
where pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pip không được cài đặt. Vui lòng cài đặt pip trước!
    exit /b 1
)

:: Tạo virtual environment
echo Tạo virtual environment...
python -m venv venv

:: Kích hoạt virtual environment
echo Kích hoạt virtual environment...
call venv\Scripts\activate

:: Cài đặt các thư viện
echo Cài đặt các thư viện...
pip install flask flask-sqlalchemy werkzeug

:: Tạo dữ liệu giả lập
echo Tạo dữ liệu giả lập...
python seed_data.py

:: Chạy ứng dụng
echo Chạy ứng dụng...
python app.py