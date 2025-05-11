from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import jwt
from datetime import datetime, timedelta
import calendar
import json
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['JWT_EXPIRATION_DELTA'] = 24 * 60 * 60  # 24 hours in seconds

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=True)
    # Thêm trường để liên kết với các bảng khác
    categories = db.relationship('Category', backref='user', lazy=True)
    products = db.relationship('Product', backref='user', lazy=True)
    customers = db.relationship('Customer', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    # Thêm trường user_id để liên kết với người dùng
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
    attributes = db.relationship('CategoryAttribute', backref='category', lazy=True, cascade="all, delete-orphan")

class CategoryAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_required = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    # Thêm trường user_id để liên kết với người dùng
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    attributes = db.relationship('ProductAttribute', backref='product', lazy=True, cascade="all, delete-orphan")

class ProductAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey('category_attribute.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    attribute = db.relationship('CategoryAttribute')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    # Thêm trường user_id để liên kết với người dùng
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    orders = db.relationship('Order', backref='customer', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='completed')
    notes = db.Column(db.Text)
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

# Helper functions
def create_admin_if_not_exists():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password=generate_password_hash('123456'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

def generate_order_number():
    prefix = datetime.now().strftime('%Y%m')
    random_suffix = str(uuid.uuid4().int)[:6]
    return f"ORD-{prefix}-{random_suffix}"

# Authentication middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in session
        if 'token' in session:
            token = session['token']
        
        if not token:
            flash('Yêu cầu đăng nhập để tiếp tục.', 'danger')
            return redirect(url_for('login'))
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            g.user = current_user
        except:
            flash('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.user.is_admin:
            flash('Yêu cầu quyền quản trị viên.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    
    return decorated

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'is_admin': user.is_admin,
                'exp': datetime.utcnow() + timedelta(seconds=app.config['JWT_EXPIRATION_DELTA'])
            }, app.config['SECRET_KEY'], algorithm="HS256")
            
            # Store token in session
            session['token'] = token
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            # Update last login
            user.last_login = datetime.now()
            db.session.commit()
            
            return redirect(url_for('dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        
        if password != confirm_password:
            flash('Mật khẩu không khớp', 'danger')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Tên đăng nhập đã tồn tại', 'danger')
            return render_template('register.html')
        
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Email đã được sử dụng', 'danger')
                return render_template('register.html')
        
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Bạn đã đăng xuất', 'success')
    return redirect(url_for('login'))

# Cập nhật route '/' để chuyển hướng đến '/dashboard' nếu người dùng đã đăng nhập
@app.route('/')
def index_redirect():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

# Cập nhật route '/shop' để sử dụng template base.html
@app.route('/shop')
def index():
    # Get filter parameters
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search', '')
    
    # Base query - chỉ lấy sản phẩm có tồn kho > 0
    query = Product.query.filter(Product.stock > 0)
    
    # Apply filters
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    
    # Get all products with applied filters
    products = query.all()
    
    # Get all categories for the filter dropdown
    categories = Category.query.all()
    
    return render_template('base.html', products=products, categories=categories, 
                          current_category=category_id, search_query=search_query)

@app.route('/products/view/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template('view_product.html', product=product)

# Dashboard - Cập nhật để kết hợp dashboard và shop
@app.route('/dashboard')
@token_required
def dashboard():
    # Get filter parameters for products
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search', '')
    
    # Base query for products - chỉ lấy sản phẩm có tồn kho > 0
    query = Product.query.filter(Product.stock > 0)
    
    # Apply filters
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    
    # Get all products with applied filters
    products = query.all()
    
    # Get all categories for the filter dropdown
    categories = Category.query.all()
    
    # Get counts for dashboard - chỉ lấy dữ liệu của người dùng hiện tại
    product_count = Product.query.filter(db.or_(Product.user_id == g.user.id, Product.user_id == None)).count()
    customer_count = Customer.query.filter(db.or_(Customer.user_id == g.user.id, Customer.user_id == None)).count()
    order_count = Order.query.filter(db.or_(Order.user_id == g.user.id, Order.user_id == None)).count()
    
    # Get recent orders
    recent_orders = Order.query.filter(db.or_(Order.user_id == g.user.id, Order.user_id == None)).order_by(Order.order_date.desc()).limit(5).all()
    
    # Calculate today's sales
    today = datetime.now().date()
    today_orders = Order.query.filter(db.func.date(Order.order_date) == today, db.or_(Order.user_id == g.user.id, Order.user_id == None)).all()
    today_sales = sum(order.total_amount for order in today_orders)
    
    # Get top selling products
    top_products = db.session.query(
        Product.id, Product.name, db.func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).join(Order).filter(db.or_(Order.user_id == g.user.id, Order.user_id == None)).group_by(Product.id).order_by(db.desc('total_sold')).limit(5).all()
    
    return render_template('base.html', 
                          products=products, 
                          categories=categories, 
                          current_category=category_id, 
                          search_query=search_query,
                          product_count=product_count,
                          customer_count=customer_count,
                          order_count=order_count,
                          recent_orders=recent_orders,
                          today_sales=today_sales,
                          top_products=top_products)

# Category routes
@app.route('/categories')
@token_required
def categories():
    categories = Category.query.filter_by(user_id=g.user.id).all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
@token_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        new_category = Category(
            name=name,
            description=description,
            user_id=g.user.id  # Thêm user_id
        )
        
        db.session.add(new_category)
        db.session.commit()
        
        # Handle attributes
        attribute_names = request.form.getlist('attribute_name[]')
        attribute_required = request.form.getlist('attribute_required[]')
        
        for i, name in enumerate(attribute_names):
            if name.strip():  # Only add non-empty attributes
                is_required = i < len(attribute_required) and attribute_required[i] == 'on'
                attr = CategoryAttribute(
                    category_id=new_category.id,
                    name=name,
                    is_required=is_required
                )
                db.session.add(attr)
        
        db.session.commit()
        
        flash('Danh mục đã được thêm thành công', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html')

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@token_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    
    # Kiểm tra xem danh mục có thuộc về người dùng hiện tại không
    if category.user_id != g.user.id:
        flash('Bạn không có quyền chỉnh sửa danh mục này', 'danger')
        return redirect(url_for('categories'))
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        
        # Handle attributes
        # First, get existing attributes to compare
        existing_attr_ids = [attr.id for attr in category.attributes]
        submitted_attr_ids = [int(id) for id in request.form.getlist('attribute_id[]') if id]
        
        # Delete attributes that were removed
        for attr_id in existing_attr_ids:
            if attr_id not in submitted_attr_ids:
                attr = CategoryAttribute.query.get(attr_id)
                db.session.delete(attr)
        
        # Update existing attributes
        for i, attr_id in enumerate(request.form.getlist('attribute_id[]')):
            if attr_id:  # This is an existing attribute
                attr = CategoryAttribute.query.get(int(attr_id))
                attr.name = request.form.getlist('attribute_name[]')[i]
                attr.is_required = 'attribute_required[]' in request.form and request.form.getlist('attribute_required[]')[i] == 'on'
        
        # Add new attributes
        new_attr_indices = [i for i, id in enumerate(request.form.getlist('attribute_id[]')) if not id]
        for i in new_attr_indices:
            name = request.form.getlist('attribute_name[]')[i]
            if name.strip():  # Only add non-empty attributes
                is_required = 'attribute_required[]' in request.form and i < len(request.form.getlist('attribute_required[]')) and request.form.getlist('attribute_required[]')[i] == 'on'
                attr = CategoryAttribute(
                    category_id=category.id,
                    name=name,
                    is_required=is_required
                )
                db.session.add(attr)
        
        db.session.commit()
        
        flash('Danh mục đã được cập nhật thành công', 'success')
        return redirect(url_for('categories'))
    
    return render_template('edit_category.html', category=category)

@app.route('/categories/delete/<int:id>')
@token_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Kiểm tra xem danh mục có thuộc về người dùng hiện tại không
    if category.user_id != g.user.id:
        flash('Bạn không có quyền xóa danh mục này', 'danger')
        return redirect(url_for('categories'))
    
    # Check if category has products
    if category.products:
        flash('Không thể xóa danh mục có sản phẩm liên quan', 'danger')
        return redirect(url_for('categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Danh mục đã được xóa thành công', 'success')
    return redirect(url_for('categories'))

# Product routes
@app.route('/products')
@token_required
def products():
    # Get filter parameters
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search', '')
    
    # Base query - chỉ lấy sản phẩm của người dùng hiện tại
    query = Product.query.filter(db.or_(Product.user_id == g.user.id, Product.user_id == None))
    
    # Apply filters
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    
    # Get all products with applied filters
    products = query.all()
    
    # Get all categories for the filter dropdown - chỉ lấy danh mục của người dùng hiện tại
    categories = Category.query.filter_by(user_id=g.user.id).all()
    
    return render_template('products.html', products=products, categories=categories, 
                          current_category=category_id, search_query=search_query)

@app.route('/products/add', methods=['GET', 'POST'])
@token_required
def add_product():
    # Chỉ lấy danh mục của người dùng hiện tại
    categories = Category.query.filter_by(user_id=g.user.id).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category_id = request.form.get('category_id')
        
        # Handle image upload
        image_path = None
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            filename = secure_filename(image.filename)
            # Add timestamp to filename to avoid duplicates
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            image_path = os.path.join('uploads', filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id if category_id else None,
            image_path=image_path,
            user_id=g.user.id  # Thêm user_id
        )
        
        db.session.add(new_product)
        db.session.flush()  # Get the product ID
        
        # Handle dynamic attributes if category is selected
        if category_id:
            category = Category.query.get(category_id)
            for attr in category.attributes:
                attr_value = request.form.get(f'attribute_{attr.id}')
                if attr_value:
                    product_attr = ProductAttribute(
                        product_id=new_product.id,
                        attribute_id=attr.id,
                        value=attr_value
                    )
                    db.session.add(product_attr)
        
        db.session.commit()
        
        flash('Sản phẩm đã được thêm thành công', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html', categories=categories)

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@token_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    # Kiểm tra xem sản phẩm có thuộc về người dùng hiện tại không
    if product.user_id is not None and product.user_id != g.user.id:
        flash('Bạn không có quyền chỉnh sửa sản phẩm này', 'danger')
        return redirect(url_for('products'))
    
    # Chỉ lấy danh mục của người dùng hiện tại
    categories = Category.query.filter_by(user_id=g.user.id).all()
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        
        # Update category
        new_category_id = request.form.get('category_id')
        if new_category_id:
            product.category_id = new_category_id
        else:
            product.category_id = None
        
        # Handle image upload
        if 'image' in request.files and request.files['image'].filename:
            # Delete old image if exists
            if product.image_path:
                old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product.image_path))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save new image
            image = request.files['image']
            filename = secure_filename(image.filename)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            product.image_path = os.path.join('uploads', filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Handle attributes
        # First, delete all existing attributes
        for attr in product.attributes:
            db.session.delete(attr)
        
        # Then add new attributes based on the selected category
        if product.category_id:
            category = Category.query.get(product.category_id)
            for attr in category.attributes:
                attr_value = request.form.get(f'attribute_{attr.id}')
                if attr_value:
                    product_attr = ProductAttribute(
                        product_id=product.id,
                        attribute_id=attr.id,
                        value=attr_value
                    )
                    db.session.add(product_attr)
        
        db.session.commit()
        
        flash('Sản phẩm đã được cập nhật thành công', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/products/delete/<int:id>')
@token_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    # Kiểm tra xem sản phẩm có thuộc về người dùng hiện tại không
    if product.user_id is not None and product.user_id != g.user.id:
        flash('Bạn không có quyền xóa sản phẩm này', 'danger')
        return redirect(url_for('products'))
    
    # Delete product image if exists
    if product.image_path:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product.image_path))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Sản phẩm đã được xóa thành công', 'success')
    return redirect(url_for('products'))

@app.route('/api/products/by-category/<int:category_id>')
@token_required
def get_products_by_category(category_id):
    # Chỉ lấy sản phẩm của người dùng hiện tại
    products = Product.query.filter_by(category_id=category_id, user_id=g.user.id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'stock': p.stock
    } for p in products])

@app.route('/api/categories/<int:id>/attributes')
@token_required
def get_category_attributes(id):
    category = Category.query.get_or_404(id)
    
    # Kiểm tra xem danh mục có thuộc về người dùng hiện tại không
    if category.user_id != g.user.id:
        return jsonify([])
    
    return jsonify([{
        'id': attr.id,
        'name': attr.name,
        'is_required': attr.is_required
    } for attr in category.attributes])

@app.route('/api/products/<int:id>')
@token_required
def get_product(id):
    product = Product.query.get_or_404(id)
    
    # Kiểm tra xem sản phẩm có thuộc về người dùng hiện tại không
    if product.user_id is not None and product.user_id != g.user.id:
        return jsonify({})
    
    # Get product attributes
    attributes = []
    if product.category_id:
        for attr in product.attributes:
            attributes.append({
                'id': attr.attribute_id,
                'name': attr.attribute.name,
                'value': attr.value
            })
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category_id': product.category_id,
        'image_path': product.image_path,
        'attributes': attributes
    })

# Customer routes
@app.route('/customers')
@token_required
def customers():
    search_query = request.args.get('search', '')
    
    # Base query - chỉ lấy khách hàng của người dùng hiện tại
    query = Customer.query.filter(db.or_(Customer.user_id == g.user.id, Customer.user_id == None))
    
    # Apply search filter
    if search_query:
        query = query.filter(
            db.or_(
                Customer.name.ilike(f'%{search_query}%'),
                Customer.phone.ilike(f'%{search_query}%'),
                Customer.email.ilike(f'%{search_query}%')
            )
        )
    
    customers = query.all()
    return render_template('customers.html', customers=customers, search_query=search_query)

@app.route('/customers/add', methods=['GET', 'POST'])
@token_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        new_customer = Customer(
            name=name,
            phone=phone,
            email=email,
            address=address,
            user_id=g.user.id  # Thêm user_id
        )
        
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Khách hàng đã được thêm thành công', 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@token_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    # Kiểm tra xem khách hàng có thuộc về người dùng hiện tại không
    if customer.user_id is not None and customer.user_id != g.user.id:
        flash('Bạn không có quyền chỉnh sửa khách hàng này', 'danger')
        return redirect(url_for('customers'))
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.phone = request.form.get('phone')
        customer.email = request.form.get('email')
        customer.address = request.form.get('address')
        
        db.session.commit()
        
        flash('Khách hàng đã được cập nhật thành công', 'success')
        return redirect(url_for('customers'))
    
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/delete/<int:id>')
@token_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    
    # Kiểm tra xem khách hàng có thuộc về người dùng hiện tại không
    if customer.user_id is not None and customer.user_id != g.user.id:
        flash('Bạn không có quyền xóa khách hàng này', 'danger')
        return redirect(url_for('customers'))
    
    # Check if customer has orders
    if customer.orders:
        flash('Không thể xóa khách hàng có đơn hàng liên quan', 'danger')
        return redirect(url_for('customers'))
    
    db.session.delete(customer)
    db.session.commit()
    
    flash('Khách hàng đã được xóa thành công', 'success')
    return redirect(url_for('customers'))

@app.route('/customers/view/<int:id>')
@token_required
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    
    # Kiểm tra xem khách hàng có thuộc về người dùng hiện tại không
    if customer.user_id is not None and customer.user_id != g.user.id:
        flash('Bạn không có quyền xem khách hàng này', 'danger')
        return redirect(url_for('customers'))
    
    orders = Order.query.filter_by(customer_id=customer.id).order_by(Order.order_date.desc()).all()
    
    return render_template('view_customer.html', customer=customer, orders=orders)

# Order routes
@app.route('/orders')
@token_required
def orders():
    # Get filter parameters
    customer_id = request.args.get('customer_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    
    # Base query - chỉ lấy đơn hàng của người dùng hiện tại
    query = Order.query.filter(db.or_(Order.user_id == g.user.id, Order.user_id == None))
    
    # Apply filters
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(Order.order_date >= start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(Order.order_date <= end_date)
    
    if status:
        query = query.filter(Order.status == status)
    
    # Get all orders with applied filters
    orders = query.order_by(Order.order_date.desc()).all()
    
    # Get all customers for the filter dropdown - chỉ lấy khách hàng của người dùng hiện tại
    customers = Customer.query.filter_by(user_id=g.user.id).all()
    
    return render_template('orders.html', orders=orders, customers=customers, 
                          current_customer=customer_id, start_date=start_date, 
                          end_date=end_date, current_status=status)

@app.route('/orders/create', methods=['GET', 'POST'])
@token_required
def create_order():
    # Chỉ lấy khách hàng của người dùng hiện tại
    customers = Customer.query.filter_by(user_id=g.user.id).all()
    
    if request.method == 'POST':
        customer_id = int(request.form.get('customer_id'))
        items_json = request.form.get('items')
        notes = request.form.get('notes')
        items = json.loads(items_json)
        
        # Kiểm tra xem khách hàng có thuộc về người dùng hiện tại không
        customer = Customer.query.get(customer_id)
        if customer.user_id is not None and customer.user_id != g.user.id:
            flash('Bạn không có quyền tạo đơn hàng cho khách hàng này', 'danger')
            return redirect(url_for('create_order'))
        
        # Create order
        new_order = Order(
            order_number=generate_order_number(),
            customer_id=customer_id,
            user_id=g.user.id,
            notes=notes,
            total_amount=0
        )
        
        db.session.add(new_order)
        db.session.flush()  # Get the order ID
        
        total_amount = 0
        
        # Add order items
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            price = item['price']
            
            # Kiểm tra xem sản phẩm có thuộc về người dùng hiện tại không
            product = Product.query.get(product_id)
            if product.user_id is not None and product.user_id != g.user.id:
                db.session.rollback()
                flash('Bạn không có quyền sử dụng sản phẩm này', 'danger')
                return redirect(url_for('create_order'))
            
            # Update product stock
            if product.stock < quantity:
                db.session.rollback()
                flash(f'Không đủ tồn kho cho sản phẩm {product.name}', 'danger')
                return redirect(url_for('create_order'))
            
            product.stock -= quantity
            
            # Create order item
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product_id,
                quantity=quantity,
                price=price
            )
            
            db.session.add(order_item)
            
            # Calculate total
            total_amount += price * quantity
        
        # Update order total
        new_order.total_amount = total_amount
        
        db.session.commit()
        
        flash('Đơn hàng đã được tạo thành công', 'success')
        return redirect(url_for('view_order', id=new_order.id))
    
    # Get all products for the order form - chỉ lấy sản phẩm của người dùng hiện tại
    products = Product.query.filter(db.or_(Product.user_id == g.user.id, Product.user_id == None)).all()
    
    # Lấy danh mục của người dùng hiện tại
    categories = Category.query.filter_by(user_id=g.user.id).all()
    
    return render_template('create_order.html', customers=customers, products=products, categories=categories)

@app.route('/orders/view/<int:id>')
@token_required
def view_order(id):
    order = Order.query.get_or_404(id)
    
    # Kiểm tra xem đơn hàng có thuộc về người dùng hiện tại không
    if order.user_id is not None and order.user_id != g.user.id:
        flash('Bạn không có quyền xem đơn hàng này', 'danger')
        return redirect(url_for('orders'))
    
    return render_template('view_order.html', order=order)

@app.route('/orders/history')
@token_required
def order_history():
    # Get filter parameters
    customer_id = request.args.get('customer_id', type=int)
    user_id = request.args.get('user_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query - chỉ lấy đơn hàng của người dùng hiện tại
    query = Order.query.filter(db.or_(Order.user_id == g.user.id, Order.user_id == None))
    
    # Apply filters
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(Order.order_date >= start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(Order.order_date <= end_date)
    
    # Get all orders with applied filters
    orders = query.order_by(Order.order_date.desc()).all()
    
    # Get all customers for the filter dropdown - chỉ lấy khách hàng của người dùng hiện tại
    customers = Customer.query.filter_by(user_id=g.user.id).all()
    
    # Get all users for the filter dropdown
    users = [g.user]  # Chỉ hiển thị người dùng hiện tại
    
    return render_template('order_history.html', orders=orders, customers=customers, 
                          users=users, current_customer=customer_id, current_user=user_id,
                          start_date=start_date, end_date=end_date)

# Reports
@app.route('/reports')
@token_required
def reports():
    return render_template('reports.html', current_year=datetime.now().year)

@app.route('/reports/daily', methods=['GET', 'POST'])
@token_required
def daily_report():
    if request.method == 'POST':
        date_str = request.form.get('date')
    else:
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Get orders for the selected date - chỉ lấy đơn hàng của người dùng hiện tại
    orders = Order.query.filter(db.func.date(Order.order_date) == date_obj, db.or_(Order.user_id == g.user.id, Order.user_id == None)).all()
    
    # Calculate totals
    total_sales = sum(order.total_amount for order in orders)
    order_count = len(orders)
    
    # Get top selling products for the day
    top_products = db.session.query(
        Product.id, Product.name, db.func.sum(OrderItem.quantity).label('total_sold'),
        db.func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(OrderItem).join(Order).filter(
        db.func.date(Order.order_date) == date_obj,
        db.or_(Order.user_id == g.user.id, Order.user_id == None)
    ).group_by(Product.id).order_by(db.desc('total_sold')).limit(5).all()
    
    return render_template('daily_report.html', 
                          date=date_obj,
                          orders=orders,
                          total_sales=total_sales,
                          order_count=order_count,
                          top_products=top_products)

@app.route('/reports/monthly', methods=['GET', 'POST'])
@token_required
def monthly_report():
    if request.method == 'POST':
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
    else:
        today = datetime.now()
        month = int(request.args.get('month', today.month))
        year = int(request.args.get('year', today.year))
    
    # Get all orders for the month - chỉ lấy đơn hàng của người dùng hiện tại
    orders = Order.query.filter(
        db.func.extract('month', Order.order_date) == month,
        db.func.extract('year', Order.order_date) == year,
        db.or_(Order.user_id == g.user.id, Order.user_id == None)
    ).all()
    
    # Calculate daily totals
    daily_data = {}
    for order in orders:
        day = order.order_date.day
        if day not in daily_data:
            daily_data[day] = {
                'total': 0,
                'order_count': 0,
                'item_count': 0
            }
        daily_data[day]['total'] += order.total_amount
        daily_data[day]['order_count'] += 1
        daily_data[day]['item_count'] += len(order.items)
    
    # Get days in month
    days_in_month = calendar.monthrange(year, month)[1]
    
    # Prepare data for chart
    days = list(range(1, days_in_month + 1))
    sales_data = [daily_data.get(day, {}).get('total', 0) for day in days]
    
    # Calculate totals
    total_sales = sum(order.total_amount for order in orders)
    order_count = len(orders)
    
    # Get top selling products for the month
    top_products = db.session.query(
        Product.id, Product.name, db.func.sum(OrderItem.quantity).label('total_sold'),
        db.func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(OrderItem).join(Order).filter(
        db.func.extract('month', Order.order_date) == month,
        db.func.extract('year', Order.order_date) == year,
        db.or_(Order.user_id == g.user.id, Order.user_id == None)
    ).group_by(Product.id).order_by(db.desc('total_sold')).limit(5).all()
    
    month_name = calendar.month_name[month]
    
    return render_template('monthly_report.html',
                          month=month,
                          month_name=month_name,
                          year=year,
                          days=days,
                          sales_data=sales_data,
                          total_sales=total_sales,
                          order_count=order_count,
                          top_products=top_products,
                          daily_data=daily_data)

@app.route('/reports/yearly', methods=['GET', 'POST'])
@token_required
def yearly_report():
    if request.method == 'POST':
        year = int(request.form.get('year'))
    else:
        year = int(request.args.get('year', datetime.now().year))
    
    # Get all orders for the year - chỉ lấy đơn hàng của người dùng hiện tại
    orders = Order.query.filter(
        db.func.extract('year', Order.order_date) == year,
        db.or_(Order.user_id == g.user.id, Order.user_id == None)
    ).all()
    
    # Calculate monthly totals
    monthly_totals = {}
    for order in orders:
        month = order.order_date.month
        if month not in monthly_totals:
            monthly_totals[month] = 0
        monthly_totals[month] += order.total_amount
    
    # Prepare data for chart
    months = list(range(1, 13))
    month_names = [calendar.month_name[month] for month in months]
    sales_data = [monthly_totals.get(month, 0) for month in months]
    
    # Calculate totals
    total_sales = sum(order.total_amount for order in orders)
    order_count = len(orders)
    
    # Get top selling products for the year
    top_products = db.session.query(
        Product.id, Product.name, db.func.sum(OrderItem.quantity).label('total_sold'),
        db.func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(OrderItem).join(Order).filter(
        db.func.extract('year', Order.order_date) == year,
        db.or_(Order.user_id == g.user.id, Order.user_id == None)
    ).group_by(Product.id).order_by(db.desc('total_sold')).limit(10).all()
    
    # Calculate quarterly data
    quarterly_data = [
        sum(sales_data[0:3]),  # Q1
        sum(sales_data[3:6]),  # Q2
        sum(sales_data[6:9]),  # Q3
        sum(sales_data[9:12])  # Q4
    ]
    
    return render_template('yearly_report.html',
                          year=year,
                          months=month_names,
                          sales_data=sales_data,
                          total_sales=total_sales,
                          order_count=order_count,
                          top_products=top_products,
                          quarterly_data=quarterly_data)

# Initialize database and create admin user
with app.app_context():
    db.create_all()
    create_admin_if_not_exists()

# Set up global user
@app.before_request
def load_user():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

if __name__ == '__main__':
    app.run(debug=True)
