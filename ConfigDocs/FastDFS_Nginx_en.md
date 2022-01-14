### The installation and configuration of FastDFS and Nginx involve many steps, here are the major steps:
#### Install the dependency package of fastDFS
1. Download and unzip the file, libfastcommon-master.zip
2. Go to the directory of libfastcommon-master
3. ```run sudo ./make.sh```
4. ```run sudo ./make.sh install```

#### Install fastDFS
1. Download and unzip the file, fastdfs-master.zip
2. Go to the directory of fastdfs-master
3. ```run sudo ./make.sh```
4. ```run sudo ./make.sh install```

#### Configure the tracker server

1. ```sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf```
2. Create a directory under /home/python/, "fastdfs/tracker"
```
mkdir –p /home/python/fastdfs/tracker
```
3. Edit the .conf file of tracker: /etc/fdfs/tracker.conf    
```
sudo vim /etc/fdfs/tracker.conf
base_path=/home/python/fastdfs/tracker
```

#### Configure the storage server
1. ```sudo cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf```
2. Create a directory under /home/python/fastdfs/, "storage"
```
mkdir –p /home/python/fastdfs/storage
```
3. Edit the .conf file of storage: /etc/fdfs/storage.conf
```
sudo vim /etc/fdfs/storage.conf
Edit the following parts：
base_path=/home/python/fastdfs/storage
store_path0=/home/python/fastdfs/storage
tracker_server=ip address of ubuntu:22122
```
#I changed the network mode from NAT to bridged adapter for Ubuntu in VirtualBox.

#### Start tracker and storage
```
fdfs_trackerd /etc/fdfs/tracker.conf start
fdfs_storaged /etc/fdfs/storage.conf start
```

#### Test if the installation is successful
1. ```sudo cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf```
2. Edit the .conf file of client: /etc/fdfs/client.conf
```
sudo vim /etc/fdfs/client.conf
Edit the following parts:
base_path=/home/python/fastdfs/tracker
tracker_server=ip address of ubuntu:22122
```
3. upload file and test：
```fdfs_upload_file /etc/fdfs/client.conf "the path of the file that you want to upload" ``` 
If return something like "group1/M00/00/00/###############################.jpg", it means you upload the file successfully.

#### Install nginx and fastdfs-nginx-module
1. Download and unzip nginx-1.8.1.tar.gz
2. Download and unzip fastdfs-nginx-module-master.zip
3. Go to the directory of nginx-1.8.1
4. Run the following
```
sudo ./configure --prefix=/usr/local/nginx/ --add-module=fastdfs-nginx-module-master(***abs path of its directory***)/src
sudo ./make
sudo ./make install
```
5. ```sudo cp fastdfs-nginx-module-master(***abs path of its directory***)/src/mod_fastdfs.conf  /etc/fdfs/mod_fastdfs.conf```
6. ```sudo vim /etc/fdfs/mod_fastdfs.conf```
```
Edit the following part:
connect_timeout=10
tracker_server=ip address of ubuntu:22122
url_have_group_name=true
store_path0=/home/python/fastdfs/storage
```
7. ```sudo cp fastdfs-master(***abs path of its directory***)/http.conf  /etc/fdfs/http.conf```
8. ```sudo cp fastdfs-master(***abs path of its directory***)/mime.types /etc/fdfs/mime.types```
9. ```sudo vim /usr/local/nginx/conf/nginx.conf```
Add the server info in the http part:
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
10. Start nginx
```
sudo /usr/local/nginx/sbin/nginx
```
#Some dependency packages may need to be installed to install the nginx successfully.
