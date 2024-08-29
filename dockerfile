# 使用Python 3镜像为基础镜像
FROM python:3

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器的/app目录下
COPY . /app

# 安装Python依赖，使用阿里云的镜像源加速下载
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 暴露应用端口
EXPOSE 8976

# 根据环境变量设置启动命令
# 启动容器时，可以通过-e RUNNINGENV=<环境>来指定环境，比如：
# 生产环境：docker run -e RUNNINGENV=prd ...
# 测试环境：docker run -e RUNNINGENV=test ...
# 开发环境：docker run -e RUNNINGENV=dev ...
CMD ["sh", "-c", "python main.py $RUNNINGENV"]
