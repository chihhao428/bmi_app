from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 获取环境变量中的数据库 URL，并确保它是以 `postgresql://` 开头
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BMIRecord(db.Model):
    __tablename__ = 'bmi_record'  # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 创建一个端点来手动触发表的创建
@app.route('/create_tables')
def create_tables():
    db.create_all()
    return "Tables created successfully!"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / (height / 100) ** 2  # 计算 BMI
        record = BMIRecord(height=height, weight=weight, bmi=bmi)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('index'))

    records = BMIRecord.query.all()
    return render_template('index.html', records=records)




if __name__ == '__main__':
    app.run(debug=True)
