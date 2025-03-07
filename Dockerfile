# Sử dụng image Python chính thức
FROM python:3.11-slim

# Đặt thư mục làm việc
WORKDIR /app

# Copy toàn bộ project vào container
COPY . .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir flask flask-sqlalchemy werkzeug

# Mở cổng 5000 (cổng mặc định của Flask)
EXPOSE 5000

# Lệnh để chạy ứng dụng
CMD ["python", "app.py"]