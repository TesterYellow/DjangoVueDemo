[TOC]



##### 2023.02

###### python第三方库安装版本问题记录

1. 问题描述：电脑安装的原有Python版本【3.6】 和新安装的版本【3.9】冲突导致安装python第三方库时，安装的位置出现问题，安装到旧版本下；
2. 解决方案1：在电脑 系统变量和用户变量的path中删除python旧版本的配置，重新执行安装命令后，成功安装到新版本下；
3. 解决方案2：配置单独的python虚拟环境
   1. 创建虚拟环境文件夹命令：python -m venv venv
      1. 创建成功后目录结构：![image-20230227222800881](C:\Users\56928\AppData\Roaming\Typora\typora-user-images\image-20230227222800881.png)
   2. 启动虚拟环境：进入Scripts目录，直接执行activate命令，成功激活；
   3. 安装依赖包：python -m pip install -r requirements.txt ；



###### pip install lxml==4.4.1 安装问题

1. 问题描述：  running build_ext
       building 'lxml.etree' extension

   error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. 访问错误提示链接，按照操作提示操作安装完成后再次安装 lxml，安装成功；





