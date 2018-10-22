#!/bin/bash

git clone https://github.com/rtfd/readthedocs.org.git --depth=1
cd readthedocs.org
mkdir ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.mirrors.ustc.edu.cn/simple
[install]
trusted-host=pypi.mirrors.ustc.edu.cn
EOF
pip install --trusted-host mirrors.aliyun.com --index-url http://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata test_data

