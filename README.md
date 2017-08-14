# README

使用Python 3.6.0版本

数据库配置

```shell
mysql.server start #启动MySQL服务器
mysql -u root -p #用root账户登录MySQL
create database codewithfun; 新建名为codewithfun的数据库
create user 'codewithfun'@'localhost' identified by 'codewithfun'; #新建名称和密码均为codewithfun的用户
grant all privileges on codewithfun.* to 'codewithfun'@'localhost'; #赋予codewithfun用户对codewithfun数据库所有表的所有权限
quit; #退出root账户
```

克隆仓库到本地

```shell
git clone https://github.com/YuNanlong/codewithfun.git
```

启动docker客户端（可以下载客户端软件）

```shell
cd codewithfun
cd docker
docker build -t test:v1 . #以上命令不要忘记加句点
```

启动网站服务器

```shell
cd .. #回到docker的父目录，也就是项目目录
source venv/bin/activate #启动Python虚拟环境
pip3 install -r requirements.txt #安装必要第三方库与工具
python3 manage.py makemigrations #进行数据库迁移
python3 manage.py migrate
python3 manage.py runserver #启动服务器
```

