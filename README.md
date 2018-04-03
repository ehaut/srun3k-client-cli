# A Command line interface for Srun3k Client for HAUT
### 深澜命令行客户端 
----------

### 欢迎使用SRUN3000 命令行版认证客户端 ###

之前我研究过Qt版本的SRUN3000认证客户端，由于某个朋友建议希望开发跨平台的版本，所以又有了此项目。

这是本人的第一个Python作品，参考了学长的python版以及某`shadowsocks`的源代码，写的很渣，请轻拍。

----------
### 特点: ###
- 可以在命令行中使用该客户端，没有UI的要求，适合嵌入式设备。
- 使用python完成命令行输入，读取配置文件，信息加密，认证和读取状态的操作。
- 使用`six`库完成Python2和Python3的兼容

----------


### Install: ###
Debian / Ubuntu:

	apt-get install python-pip
	pip install srun-cli #For Python2.7
	pip3 install srun-cli #For Python3

CentOS:
	
	yum install python-setuptools && easy_install pip
	pip install srun-cli #For Python2.7
	pip3 install srun-cli #For Python3

Windows:(If you installed Python,如果您安装Python和pip，环境变量配置正确的话）

	pip install srun-cli #For Python2.7
	pip3 install srun-cli #For Python3

Then you can use it on your command line interface.

您就可以在命令行使用。

### Usage: ###

	srun-cli -u 201600000000 -k yourpassword

Check all the options via `-h`. You can also use a [Configuration] file instead.

通过使用-h选项查看帮助,你可以发现所有选项。

**The username and password is *the required fields*.**

除了用户名和密码是必填项，其他都可以根据情况选填。

You can use a configuration file instead of command line arguments.

您也可以使用配置文件替代命令行参数。

Create a config file `/etc/srun/config.json`. Example:

创建配置文件如下所示：

```
{
   "username":"201600000000",
   "password":"yourpassword"	
}
```
Explanation of the fields:

下面这些选项都可以加入到配置文件中。

|Name|Explanation|
| :-: | :-: |
|server_addr|The authenticate server address
|server_port|The authenticate server port
|username|Your login name|
|password|Your login password|
|acid|ACID value|
|type|TYPE value|
|drop|DROP value|
|pop|POP value|
|mac|MAC address|

To use it.

使用配置文件。

	srun-cli -c /etc/srun/config.json
