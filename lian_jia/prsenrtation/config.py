import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)

MYSQL_CONN = "jdbc:mariadb://root:123456@localhost:3306/lian_jia"

conn_param = {"user": "root", "password": "123456", "driver": "com.mysql.cj.jdbc.Driver"}
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "jdbc:mariadb://root:123456@localhost:3306/lian_jia"
# 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 创建数据库的操作对象
db = SQLAlchemy(app)
