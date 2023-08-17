from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# 路由：主頁
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/employees')
def index1():
    excel_file = 'employees.xlsx'  # Excel文件路徑
    df = pd.read_excel(excel_file)
    data = df.to_dict(orient='records')

    return render_template('index1.html', data=data)

@app.route('/records')
def index2():
    excel_file = 'records.xlsx'  # Excel文件路徑
    df = pd.read_excel(excel_file)
    data = df.to_dict(orient='records')

    return render_template('index2.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)