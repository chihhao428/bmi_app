from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import os

# 创建 Flask 应用
app = Flask(__name__)

# 获取环境变量中的 DATABASE_URL，并确保它是以 'postgresql://' 开头
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 配置数据库连接字符串
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 定义 BMI 记录模型
class BMIRecord(db.Model):
    __tablename__ = 'bmi_record'  # 指定表名为 bmi_record
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

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

@app.route('/plot')
def plot():
    # 从数据库中查询数据
    records = BMIRecord.query.all()
    
    # 提取身高、体重和 BMI 数据
    heights = [record.height for record in records]
    weights = [record.weight for record in records]
    bmis = [record.bmi for record in records]
    
    # 创建子图
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Height vs Weight", "BMI Distribution","Height vs BMI","Height vs Weight"))

    # 添加身高 vs 体重散点图
    fig.add_trace(
        go.Scatter(x=heights, y=weights, mode='markers', name='Height vs Weight'),
        row=1, col=1
    )

    # 添加 BMI 直方图
    fig.add_trace(
        go.Histogram(x=bmis, nbinsx=20, name='BMI Distribution'),
        row=1, col=2
    )

    # 创建折线图
    #fig = go.Figure()
    fig.add_trace(go.Scatter(x=heights, y=bmis, mode='lines', name='BMI'),row=2,col=1)
    fig.add_trace(go.Scatter(x=heights, y=weights, mode='lines', name='Weight'),row=2,col=2)

    # 更新图表布局
    fig.update_layout(title_text="BMI and Weight Analysis", xaxis_title="Height (cm)")

    # 将图表以 HTML 格式返回
    return fig.to_html()

    # 更新图表布局
    fig.update_layout(title_text="BMI Records Analysis", showlegend=False)

    # 将图表以 HTML 格式返回
    return fig.to_html()

# 在应用启动时创建表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
