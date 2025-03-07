# Blog Web 

## Thông tin cá nhân
- Họ tên: Kiều Trương Hàm Hương
- Mã sinh viên: 22719241

## Mô tả project
Ứng dụng web xây dựng bằng Flask với các chức năng: viết blog, đăng nhập/đăng ký, quản lý người dùng qua trang admin, quản lý bài viết cá nhân và phân trang.

## Hướng dẫn cài đặt và chạy
### 1. Yêu cầu hệ thống
- Hệ điều hành: Windowns, Linux, hoặc macOS
- Docker Desktop
- Git ( để clone repository)
### 2. Cài đặt
1. Clone repository:
   ```bash
   git clone https://github.com/HamHuong/flask-tiny-app.git
   cd flask-tiny-app

2. Cài đặt các thư viện Python (nếu không dùng Docker)
   - Tạo môi trường ảo:
     ``` bash
     python -m venv venv
     venv\Scripts\activate
   -  Cài đặt dependencies:
      ``` bash
      pip install -r requirements.txt

3. Xây dựng và chạy chương trình
   - Nếu dùng docker
     ``` bash
     docker-compose up --build
   - Nếu dùng môi trường ảo:
     ``` bash
     python app.py

4. Link dự án
   http://127.0.0.1:5000/

   
