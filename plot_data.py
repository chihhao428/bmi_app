import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 获取环境变量中的数据库 URL，并确保它是以 `postgresql://` 开头
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 从数据库读取数据
df = pd.read_sql("SELECT * FROM bmi_record", engine)

# 创建图表
fig = px.scatter(df, x='height', y='weight', size='bmi', color='bmi',
                 title='BMI Scatter Plot',
                 labels={'height': 'Height (cm)', 'weight': 'Weight (kg)', 'bmi': 'BMI'})

# 显示图表
fig.show()
