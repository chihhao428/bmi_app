from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 获取环境变量中的数据库 URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("://", "postgres://hrc_user:u7IVhdmQSLnWxgbzNnNdIKalQu1XCJUc@dpg-cpkghm4f7o1s73conon0-a/hrc", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)

    def __init__(self, height, weight, bmi):
        self.height = height
        self.weight = weight
        self.bmi = bmi

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
