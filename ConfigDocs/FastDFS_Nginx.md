### fastDFS和Nginx的安装和配置比较长，以下为其主要部分
#### 安装fastdfs依赖包
1. 解压缩libfastcommon-master.zip
2. 进入到libfastcommon-master的目录中
3. ```执行 sudo ./make.sh```
4. ```执行 sudo ./make.sh install```

#### 安装fastdfs
1. 解压缩fastdfs-master.zip
2. 进入到 fastdfs-master目录中
3. ```执行 sudo ./make.sh```
4. ```执行 sudo ./make.sh install```

#### 配置跟踪服务器tracker

1. ```sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf```
2. 在/home/python/目录中创建目录 fastdfs/tracker
```
mkdir –p /home/python/fastdfs/tracker
```
3. 编辑/etc/fdfs/tracker.conf配置文件    
```
sudo vim /etc/fdfs/tracker.conf
base_path=/home/python/fastdfs/tracker
```

#### 配置存储服务器storage
1. ```sudo cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf```
2. 在/home/python/fastdfs/ 目录中创建目录 storage
```
mkdir –p /home/python/fastdfs/storage
```
3. 编辑/etc/fdfs/storage.conf配置文件
```sudo vim /etc/fdfs/storage.conf```
修改内容：
```
base_path=/home/python/fastdfs/storage
store_path0=/home/python/fastdfs/storage
tracker_server=ubuntu虚拟机的ip地址:22122
```
#需要在VirtualBox里将虚拟机的网络模式改为桥接，再用ifconfig获得其ip地址

#### 启动tracker 和 storage
```
fdfs_trackerd /etc/fdfs/tracker.conf start
fdfs_storaged /etc/fdfs/storage.conf start
```

#### 测试是否安装成功
1. ```sudo cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf```
2. 编辑/etc/fdfs/client.conf配置文件  ```sudo vim /etc/fdfs/client.conf```
修改内容:
```
base_path=/home/python/fastdfs/tracker
tracker_server=ubuntu虚拟机的ip地址:22122
```
3. 上传文件测试：
```fdfs_upload_file /etc/fdfs/client.conf``` 要上传的图片文件 
如果返回类似group1/M00/00/00/###############################.jpg的文件id则说明文件上传成功

#### 安装nginx及fastdfs-nginx-module
1. 解压缩 nginx-1.8.1.tar.gz
2. 解压缩 fastdfs-nginx-module-master.zip
3. 进入nginx-1.8.1目录中
4. 执行
```
sudo ./configure --prefix=/usr/local/nginx/ --add-module=fastdfs-nginx-module-master解压后的目录的绝对路径/src
sudo ./make
sudo ./make install
```
5. ```sudo cp fastdfs-nginx-module-master解压后的目录中src下的mod_fastdfs.conf  /etc/fdfs/mod_fastdfs.conf```
6. ```sudo vim /etc/fdfs/mod_fastdfs.conf```
修改内容：
```
connect_timeout=10
tracker_server=ubuntu虚拟机的ip地址:22122
url_have_group_name=true
store_path0=/home/python/fastdfs/storage
```
7. ```sudo cp 解压缩的fastdfs-master目录中的http.conf  /etc/fdfs/http.conf```
8. ```sudo cp 解压缩的fastdfs-master目录中的mime.types /etc/fdfs/mime.types```
9. ```sudo vim /usr/local/nginx/conf/nginx.conf```
在http部分中添加配置信息如下：
```
server {
            listen       8888;
            server_name  localhost;
            location ~/group[0-9]/ {
                ngx_fastdfs_module;
            }
            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
            root   html;
            }
        }
```
10. 启动nginx
```
sudo /usr/local/nginx/sbin/nginx
```
在安装nginx时可能需要下载各种依赖包。
