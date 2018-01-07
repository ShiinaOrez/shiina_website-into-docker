# 建立在python-2.7的基础上
FROM python:2.7-slim

#设置工作空间为/sw
WORKDIR /sw

#把当前目录下的文件拷贝到容器的/sw里
ADD . /sw

#安装requirements.txt中指定的依赖
RUN pip install -r requirements.txt

#开放80端口
EXPOSE 80

#清除所有数据
CMD ["python","shiina_website/manage.py","shell"]\

&& ["from","shiina_website/app","import","db"]\

&& ["db.drop_all()"]\

&& ["db.create_all()"]\

&& ["quit()"]\

&& ["python","shiina_website/manage.py","db","upgrade"]\

&& ["python","shiina_website/manage.py","runserver","--host","0.0.0.0","--port","80"]
