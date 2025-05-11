  Hệ Thống Quản Lý Đơn Bán Hàng
 1. Giới Thiệu
Hệ thống Quản lý Đơn Bán Hàng là một ứng dụng web toàn diện được phát triển bằng Flask, giúp doanh nghiệp quản lý hiệu quả quy trình bán hàng từ đầu đến cuối. Hệ thống cung cấp giao diện trực quan, dễ sử dụng cho việc quản lý sản phẩm, khách hàng, đơn hàng và báo cáo.
Được thiết kế với giao diện người dùng thân thiện và cơ sở dữ liệu linh hoạt (hỗ trợ cả MySQL và SQLite), hệ thống phù hợp với các doanh nghiệp vừa và nhỏ, cửa hàng bán lẻ, và các đơn vị kinh doanh trực tuyến.

 2. Tính Năng ChínhyChínhy
  2.1. Quản Lý Danh Mục
- Tạo, chỉnh sửa và xóa danh mục sản phẩm
- Phân loại sản phẩm theo thuộc tính
- Mô tả chi tiết cho từng danh mục
- Hỗ trợ danh mục đa cấp (danh mục con)
- Tìm kiếm và lọc danh mục

  2.2. Quản Lý Sản Phẩm
- Thêm, sửa, xóa thông tin sản phẩm
- Tải lên và quản lý hình ảnh sản phẩm
- Theo dõi tồn kho tự động
- Cảnh báo khi hàng sắp hết
- Tìm kiếm sản phẩm nâng cao
- Nhập/xuất danh sách sản phẩm từ Excel
- Lịch sử thay đổi giá

  2.3. Quản Lý Khách Hàng
- Lưu trữ thông tin liên hệ đầy đủ
- Lịch sử mua hàng của khách
- Phân loại khách hàng (VIP, thường xuyên, mới)
- Ghi chú đặc biệt cho từng khách hàng
- Tìm kiếm và lọc khách hàng
- Xuất danh sách khách hàng

  2.4. Quản Lý Đơn Hàng
- Tạo đơn hàng mới với giao diện trực quan
- Thêm nhiều sản phẩm vào đơn hàng
- Áp dụng giảm giá và khuyến mãi
- Tính toán tự động tổng tiền
- Theo dõi trạng thái đơn hàng
- In hóa đơn và phiếu giao hàng
- Lịch sử đơn hàng chi tiết

  2.5. Báo Cáo Thống Kê
- Báo cáo doanh thu theo ngày, tháng, năm
- Báo cáo sản phẩm bán chạy
- Báo cáo tồn kho
- Báo cáo khách hàng tiềm năng
- Biểu đồ trực quan
- Xuất báo cáo ra Excel, PDF
- Tùy chỉnh thời gian báo cáo

  2.6. Hệ Thống Người Dùng
- Đăng ký và đăng nhập an toàn
- Phân quyền người dùng (admin, nhân viên, kế toán)
- Khôi phục mật khẩu qua email
- Lịch sử hoạt động người dùng
- Thay đổi thông tin cá nhân

  3. Cấu Trúc Cơ Sở Dữ Liệu
  3.1. Bảng DanhMuc (Categories)
- MaDM (ID): Khóa chính, tự động tăng
- TenDM (Name): Tên danh mục
- MoTa (Description): Mô tả chi tiết
- ThuocTinh (Attributes): Các thuộc tính của danh mục

  3.2. Bảng SanPham (Products)
- MaSP (ID): Khóa chính, tự động tăng
- TenSP (Name): Tên sản phẩm
- MaDM (CategoryID): Khóa ngoại liên kết với bảng DanhMuc
- MoTa (Description): Mô tả sản phẩm
- Gia (Price): Giá sản phẩm
- TonKho (Stock): Số lượng tồn kho
- AnhSP (Image): Đường dẫn đến hình ảnh sản phẩm

  3.3. Bảng KhachHang (Customers)
- MaKH (ID): Khóa chính, tự động tăng
- TenKH (Name): Tên khách hàng
- DT (Phone): Số điện thoại
- Email: Địa chỉ email
- DiaChi (Address): Địa chỉ giao hàng

  3.4. Bảng DonHang (Orders)
- MaDH (ID): Khóa chính, tự động tăng
- MaKH (CustomerID): Khóa ngoại liên kết với bảng KhachHang
- NgayDat (OrderDate): Ngày đặt hàng
- TongTien (TotalAmount): Tổng giá trị đơn hàng
- TrangThai (Status): Trạng thái đơn hàng
- GhiChu (Notes): Ghi chú đơn hàng

  3.5. Bảng ChiTietDonHang (OrderDetails)
- MaCTDH (ID): Khóa chính, tự động tăng
- MaDH (OrderID): Khóa ngoại liên kết với bảng DonHang
- MaSP (ProductID): Khóa ngoại liên kết với bảng SanPham
- SoLuong (Quantity): Số lượng sản phẩm
- DonGia (UnitPrice): Đơn giá tại thời điểm mua
- ThanhTien (Subtotal): Thành tiền

  3.6. Bảng BaoCao (Reports)
- MaBaoCao (ID): Khóa chính, tự động tăng
- LoaiBaoCao (Type): Loại báo cáo (ngày, tháng, năm)
- NgayBaoCao (ReportDate): Ngày tạo báo cáo
- NoiDung (Content): Nội dung báo cáo (JSON)

  4. Hướng Dẫn Cài Đặt
  4.1. Yêu Cầu Hệ Thống
- Python 3.6 hoặc cao hơn
- Pip (trình quản lý gói Python)
- MySQL (tùy chọn, nếu không sử dụng SQLite)
- Trình duyệt web hiện đại (Chrome, Firefox, Edge)

4.2. Cài Đặt Môi Trường
4.2.1. Windows
1. Tải và cài đặt Python từ [python.org](https://www.python.org/downloads/)
2. Mở Command Prompt và kiểm tra cài đặt:
  python --version
 pip --version
 3. Tạo và kích hoạt môi trường ảo:
  python -m venv venv
 venv\Scripts\activate
  4.2.2. macOS/Linux
1. Cài đặt Python (nếu chưa có):
    macOS với Homebrew
 brew install python

   Ubuntu/Debian
 sudo apt update
 sudo apt install python3 python3-pip python3-venv
 2. Tạo và kích hoạt môi trường ảo:
  python3 -m venv venv
 source venv/bin/activate
   4.3. Cài Đặt Ứng Dụng

1. Clone hoặc tải mã nguồn:
  git clone https://github.com/username/sales_management_system.git
 cd sales_management_system
 2. Cài đặt các thư viện cần thiết:
  pip install -r requirements.txt
 3. Thiết lập cơ sở dữ liệu:

  Sử dụng SQLite (đơn giản nhất): 
    Không cần thiết lập thêm, SQLite sẽ tự động được tạo
   Sử dụng MySQL: 
    Cài đặt MySQL và tạo cơ sở dữ liệu
 mysql -u root -p
 CREATE DATABASE sales_management;
 EXIT;

   Nhập cấu trúc cơ sở dữ liệu
 mysql -u root -p sales_management < create_database.sql
 4. Cấu hình ứng dụng:
 - Mở file `app.py` hoặc `app_sqlite.py`
 - Kiểm tra và cập nhật thông tin kết nối cơ sở dữ liệu (nếu cần)

  5. Các Thư Viện Cần Cài
  5.1. Thư Viện Core
-  Flask (2.0.1+) : Framework web chính
 
  pip install Flask==2.0.1
 
-  Flask-SQLAlchemy (2.5.1+) : ORM cho cơ sở dữ liệu
 
  pip install Flask-SQLAlchemy==2.5.1
 
-  Flask-Login (0.5.0+) : Quản lý phiên đăng nhập
 
  pip install Flask-Login==0.5.0
 
-  Flask-WTF (0.15.1+) : Xử lý form và validation
 
  pip install Flask-WTF==0.15.1

  5.2. Thư Viện Cơ Sở Dữ Liệu
-  SQLAlchemy (1.4.23+) : ORM cho Python
 
  pip install SQLAlchemy==1.4.23
 
-  PyMySQL (1.0.2+) : Kết nối MySQL (nếu sử dụng MySQL)
 
  pip install PyMySQL==1.0.2
 
-  Alembic (1.7.1+) : Quản lý migration cơ sở dữ liệu
 
  pip install alembic==1.7.1
 
  5.3. Thư Viện Xử Lý Dữ Liệu
-  Pandas (1.3.2+) : Phân tích và xử lý dữ liệu
 
  pip install pandas==1.3.2
 
-  NumPy (1.21.2+) : Tính toán số học
 
  pip install numpy==1.21.2
 
-  openpyxl (3.0.7+) : Xử lý file Excel
 
  pip install openpyxl==3.0.7 
  5.4. Thư Viện Bảo Mật
-  Werkzeug (2.0.1+) : Tiện ích bảo mật
 
  pip install Werkzeug==2.0.1
 
-  itsdangerous (2.0.1+) : Mã hóa dữ liệu
 
  pip install itsdangerous==2.0.1
 
-  Flask-Bcrypt (0.7.1+) : Mã hóa mật khẩu
 
  pip install Flask-Bcrypt==0.7.1

  5.5. Thư Viện Giao Diện
-  Flask-Bootstrap (3.3.7.1+) : Tích hợp Bootstrap
 
  pip install Flask-Bootstrap==3.3.7.1
 
-  Chart.js (qua CDN) : Tạo biểu đồ

  5.6. Thư Viện Kiểm Thử
-  pytest (6.2.5+) : Framework kiểm thử
 
  pip install pytest==6.2.5
 
-  locust (2.2.1+) : Kiểm thử hiệu năng
 
  pip install locust==2.2.1
 
  5.7. Cài Đặt Tất Cả Thư Viện
 
pip install -r requirements.txt
 
  6. Cách Khởi Chạy Web
  6.1. Khởi Động Cơ Bản
1.  Kích hoạt môi trường ảo :
  bash
   Windows
 venv\Scripts\activate

   macOS/Linux
 source venv/bin/activate
 2.  Khởi động với SQLite  (đơn giản nhất):
  bash
 python app_sqlite.py
  Ứng dụng sẽ chạy tại http://localhost:5000

3.  Khởi động với MySQL :
  bash
 python app.py
  Đảm bảo MySQL server đang chạy và thông tin kết nối chính xác

  6.2. Khởi Động Nâng Cao
1.  Chế độ phát triển với Flask CLI :
  bash
   Thiết lập biến môi trường
 export FLASK_APP=app.py  Linux/macOS
 set FLASK_APP=app.py   Windows

 export FLASK_ENV=development  Linux/macOS
 set FLASK_ENV=development   Windows

   Khởi động server
 flask run
 2.  Chế độ debug với tự động tải lại :
  bash
 export FLASK_DEBUG=1  Linux/macOS
 set FLASK_DEBUG=1   Windows
 flask run
 3.  Chỉ định host và port :
  bash
   Cho phép truy cập từ các thiết bị khác trong mạng LAN
 flask run --host=0.0.0.0 --port=8080
 4.  Khởi động với Gunicorn (production) :
  bash
   Cài đặt Gunicorn
 pip install gunicorn

   Khởi động với 4 worker
 gunicorn -w 4 -b 0.0.0.0:5000 app:app
 5.  Khởi động với uWSGI (production) :
  bash
   Cài đặt uWSGI
 pip install uwsgi

   Khởi động
 uwsgi --http 0.0.0.0:5000 --module app:app --processes 4 --threads 2
 6.  Khởi động với biến môi trường từ file :
  bash
   Tạo file .env
 echo "FLASK_APP=app.py" > .env
 echo "FLASK_ENV=development" >> .env
 echo "DATABASE_URL=mysql+pymysql://user:password@localhost/sales_management" >> .env

   Cài đặt python-dotenv
 pip install python-dotenv

   Khởi động
 flask run
   7. Kiểm Thử Hệ Thống
  7.1. Kiểm Thử Đơn Vị (Unit Testing)
1.  Cài đặt pytest :
  bash
 pip install pytest pytest-flask
 2.  Tạo file kiểm thử :
 Tạo thư mục `tests` và các file kiểm thử:
  tests/
 ├── conftest.py     Cấu hình pytest
 ├── test_auth.py    Kiểm thử xác thực
 ├── test_products.py  Kiểm thử quản lý sản phẩm
 ├── test_customers.py   Kiểm thử quản lý khách hàng
 └── test_orders.py    Kiểm thử quản lý đơn hàng
 3.  Chạy kiểm thử :
  bash
   Chạy tất cả kiểm thử
 pytest

   Chạy kiểm thử cụ thể
 pytest tests/test_products.py

   Chạy với báo cáo chi tiết
 pytest -v

   Chạy với báo cáo coverage
 pytest --cov=app tests/
 4.  Ví dụ file kiểm thử đơn vị :
    tests/test_products.py
 def test_add_product(client, auth):
   Đăng nhập
   auth.login()
     Gửi request thêm sản phẩm
   response = client.post('/products/add', data={
     'TenSP': 'Sản phẩm test',
     'MaDM': 1,
     'MoTa': 'Mô tả test',
     'Gia': 100000,
     'TonKho': 10
   }, follow_redirects=True)
     Kiểm tra kết quả
   assert response.status_code == 200
   assert b'Sản phẩm test' in response.data

  7.2. Kiểm Thử Tích Hợp (Integration Testing)
1.  Kiểm thử luồng đơn hàng hoàn chỉnh :
  def test_complete_order_flow(client, auth):
   Đăng nhập
   auth.login()
     Thêm khách hàng
   client.post('/customers/add', data={...})
     Tạo đơn hàng
   client.post('/orders/create', data={...})
     Thêm sản phẩm vào đơn hàng
   client.post('/orders/1/add_product', data={...})
     Hoàn tất đơn hàng
   client.post('/orders/1/complete', data={...})
     Kiểm tra tồn kho đã giảm
   response = client.get('/products/1')
   assert b'9' in response.data  Tồn kho giảm 1 
  7.3. Kiểm Thử Hiệu Năng (Performance Testing)
1.  Cài đặt Locust :
  bash
 pip install locust
 2.  Tạo file kiểm thử hiệu năng :
    locustfile.py
 from locust import HttpUser, task, between

 class WebsiteUser(HttpUser):
   wait_time = between(1, 5)
     @task
   def index_page(self):
     self.client.get("/")
       @task(3)
   def view_products(self):
     self.client.get("/products")
       @task(2)
   def view_customers(self):
     self.client.get("/customers")
 3.  Chạy kiểm thử hiệu năng :
  bash
 locust
  Truy cập http://localhost:8089 để cấu hình và chạy kiểm thử

  7.4. Kiểm Thử Giao Diện Người Dùng (UI Testing)
1.  Cài đặt Selenium :
  bash
 pip install selenium
 2.  Tạo file kiểm thử UI :
    tests/test_ui.py
 from selenium import webdriver
 from selenium.webdriver.common.keys import Keys

 def test_login_ui():
   driver = webdriver.Chrome()
   driver.get("http://localhost:5000/login")
     Nhập thông tin đăng nhập
   driver.find_element_by_name("email").send_keys("admin@example.com")
   driver.find_element_by_name("password").send_keys("admin123")
   driver.find_element_by_name("password").send_keys(Keys.RETURN)
     Kiểm tra đã chuyển đến dashboard
   assert "Dashboard" in driver.title
     driver.close()
  8. Những Cách Người Dùng Hoạt Động
  8.1. Đăng Ký / Đăng Nhập
Người dùng → Giao diện đăng nhập → Nhập email/mật khẩu → Gửi POST request → Flask app xử lý → 
Kiểm tra thông tin trong DB → Tạo phiên đăng nhập → Chuyển hướng đến Dashboard

 Chi tiết kỹ thuật :
- Route: `/login` và `/register`
- Controller: `auth_bp` trong `app.py`
- Model: `User` trong `app.py`
- Xác thực: Flask-Login
- Bảo mật: Mật khẩu được mã hóa với Werkzeug

  8.2. Quản Lý Sản Phẩm
Người dùng → Trang sản phẩm → Nhấn "Thêm sản phẩm" → Điền form → Tải lên hình ảnh → 
Gửi POST request → Flask app xử lý → Lưu thông tin vào DB → Lưu hình ảnh vào thư mục uploads → 
Chuyển hướng đến danh sách sản phẩm với thông báo thành công

 Chi tiết kỹ thuật :
- Routes: `/products`, `/products/add`, `/products/<id>/edit`, `/products/<id>/delete`
- Controller: `product_bp` trong `app.py`
- Model: `SanPham` trong `app.py`
- Xử lý file: `werkzeug.utils.secure_filename`
- Validation: Flask-WTF

  8.3. Tạo Đơn Hàng Mới
Người dùng → Trang đơn hàng → Nhấn "Tạo đơn hàng" → Chọn khách hàng từ dropdown → 
Tìm kiếm và thêm sản phẩm → Điều chỉnh số lượng → Thêm ghi chú → Nhấn "Lưu đơn hàng" → 
Flask app xử lý → Tạo đơn hàng trong DB → Tạo chi tiết đơn hàng → Cập nhật tồn kho → 
Chuyển hướng đến trang chi tiết đơn hàng
 
 Chi tiết kỹ thuật :
- Routes: `/orders/create`, `/orders/<id>`, `/orders/<id>/add_product`
- Controller: `order_bp` trong `app.py`
- Models: `DonHang` và `ChiTietDonHang` trong `app.py`
- Transaction: SQLAlchemy session với commit/rollback
- AJAX: Cập nhật giỏ hàng động

  8.4. Xem Báo Cáo
Người dùng → Trang báo cáo → Chọn loại báo cáo (ngày/tháng/năm) → Chọn khoảng thời gian → 
Nhấn "Tạo báo cáo" → Flask app xử lý → Truy vấn DB lấy dữ liệu đơn hàng → 
Tính toán doanh thu, sản phẩm bán chạy → Tạo biểu đồ với Chart.js → 
Hiển thị báo cáo → Người dùng có thể xuất ra PDF/Excel
 
 Chi tiết kỹ thuật :
- Routes: `/reports`, `/reports/daily`, `/reports/monthly`, `/reports/yearly`
- Controller: `report_bp` trong `app.py`
- Models: `DonHang`, `ChiTietDonHang`, `BaoCao`
- Xử lý dữ liệu: Pandas
- Biểu đồ: Chart.js
- Xuất file: openpyxl, reportlab

  8.5. Quản Lý Khách Hàng
Người dùng → Trang khách hàng → Tìm kiếm khách hàng → Xem chi tiết → Xem lịch sử mua hàng → 
Chỉnh sửa thông tin → Gửi POST request → Flask app xử lý → Cập nhật DB → 
Chuyển hướng đến trang chi tiết khách hàng với thông báo thành công
 
 Chi tiết kỹ thuật :
- Routes: `/customers`, `/customers/<id>`, `/customers/<id>/edit`
- Controller: `customer_bp` trong `app.py`
- Model: `KhachHang` trong `app.py`
- Tìm kiếm: SQLAlchemy query filters
- Phân trang: Flask-SQLAlchemy pagination

 9. Xử Lý Lỗi Thường Gặp
  9.1. Lỗi Kết Nối MySQL
 Triệu chứng : Lỗi `socket.create_connection()` hoặc `OperationalError: (2003, "Can't connect to MySQL server")`

 Nguyên nhân và giải pháp :
-  MySQL chưa khởi động :
 bash
  Windows
  net start mysql

  macOS
  brew services start mysql

  Linux
  sudo systemctl start mysql
 
-  Thông tin kết nối không chính xác :
  Kiểm tra và cập nhật thông tin trong `app.py`:
 
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/sales_management'
 
-  Firewall chặn kết nối :
  Kiểm tra cấu hình firewall và mở port 3306 nếu cần.

-  Thư viện pymysql chưa cài đặt :
 bash
  pip install pymysql
 
  9.2. Lỗi Flask Context
 Triệu chứng : Lỗi `RuntimeError: Working outside of application context` khi chạy `db.create_all()`

 Nguyên nhân và giải pháp :
-  Sử dụng app context không đúng cách :
 
  Cách đúng
  with app.app_context():
  db.create_all()
  create_admin_if_not_exists()
 
-  Cấu trúc ứng dụng không đúng :
  Đảm bảo `db` được khởi tạo sau `app`:
 
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = '...'
  db = SQLAlchemy(app)
 
-  Sử dụng phiên bản Flask cũ :
 bash
  pip install --upgrade flask flask-sqlalchemy
 
  9.3. Lỗi Tải Lên Hình Ảnh
 Triệu chứng : Không thể tải lên hình ảnh hoặc hình ảnh không hiển thị

 Nguyên nhân và giải pháp :
-  Thư mục uploads không tồn tại :
 
  import os
  if not os.path.exists('static/uploads'):
  os.makedirs('static/uploads')
 
-  Quyền truy cập thư mục không đủ :
 bash
  Linux/macOS
  chmod 755 static/uploads

-  Cấu hình form không đúng :
  html
  <form method="POST" enctype="multipart/form-data">

-  Xử lý file không đúng :
 
  from werkzeug.utils import secure_filename
  filename = secure_filename(file.filename)
  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

 10. Triển Khai Ứng Dụng
  10.1. Triển Khai Trên VPS/Dedicated Server
1.  Chuẩn bị server :
  bash
   Cài đặt các gói cần thiết
 sudo apt update
 sudo apt install python3 python3-pip python3-venv nginx
 2.  Cài đặt và cấu hình ứng dụng :
  bash
   Clone mã nguồn
 git clone https://github.com/username/sales_management_system.git
 cd sales_management_system

   Tạo môi trường ảo và cài đặt dependencies
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 pip install gunicorn
 3.  Cấu hình Gunicorn :
 Tạo file `wsgi.py`:
  from app import app

 if __name__ == "__main__":
   app.run()
 4.  Tạo service systemd :
  bash
 sudo nano /etc/systemd/system/sales_app.service
  Nội dung:
  [Unit]
 Description=Gunicorn instance to serve sales management app
 After=network.target

 [Service]
 User=ubuntu
 Group=www-data
 WorkingDirectory=/home/ubuntu/sales_management_system
 Environment="PATH=/home/ubuntu/sales_management_system/venv/bin"
 ExecStart=/home/ubuntu/sales_management_system/venv/bin/gunicorn --workers 3 --bind unix:sales_app.sock -m 007 wsgi:app

 [Install]
 WantedBy=multi-user.target
 5.  Cấu hình Nginx :
  bash
 sudo nano /etc/nginx/sites-available/sales_app
  Nội dung:
  server {
   listen 80;
   server_name your_domain.com;

   location / {
     include proxy_params;
     proxy_pass http://unix:/home/ubuntu/sales_management_system/sales_app.sock;
   }

   location /static {
     alias /home/ubuntu/sales_management_system/static;
   }
 }
 6.  Kích hoạt cấu hình :
  bash
 sudo ln -s /etc/nginx/sites-available/sales_app /etc/nginx/sites-enabled
 sudo systemctl start sales_app
 sudo systemctl enable sales_app
 sudo systemctl restart nginx
   10.2. Triển Khai Trên Docker

1.  Tạo Dockerfile :
 dockerfile
 FROM python:3.9-slim

 WORKDIR /app

 COPY requirements.txt .
 RUN pip install --no-cache-dir -r requirements.txt

 COPY . .

 EXPOSE 5000

 CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
 2.  Tạo docker-compose.yml :
  yaml
 version: '3'
 services:
   web:
   build: .
   ports:
   - "5000:5000"
   volumes:
   - ./static/uploads:/app/static/uploads
   environment:
   - FLASK_ENV=production
   - DATABASE_URL=mysql+pymysql://user:password@db/sales_management
   depends_on:
   - db
   db:
   image: mysql:5.7
   environment:
   - MYSQL_ROOT_PASSWORD=rootpassword
   - MYSQL_DATABASE=sales_management
   - MYSQL_USER=user
   - MYSQL_PASSWORD=password
   volumes:
   - mysql_data:/var/lib/mysql
 volumes:
   mysql_data:
 3.  Xây dựng và chạy container :
  bash
 docker-compose up -d
  11. Đóng Góp

Chúng tôi rất hoan nghênh mọi đóng góp cho dự án! Dưới đây là cách bạn có thể tham gia:
1.  Fork dự án  trên GitHub
2.  Tạo nhánh tính năng  (`git checkout -b feature/amazing-feature`)
3.  Commit thay đổi  (`git commit -m 'Add some amazing feature'`)
4.  Push lên nhánh  (`git push origin feature/amazing-feature`)
5.  Tạo Pull Request 

 12. Giấy Phép
Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
 13. Liên Hệ

Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ:
- Email: example@example.com
- GitHub Issues: https://github.com/username/sales_management_system/issues
