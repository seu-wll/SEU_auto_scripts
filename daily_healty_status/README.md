# 每日上报自动化脚本

鉴于每次手动填报太麻烦，辅导员又催的紧，遂想到做一个自动化签到脚本，并最后放到云服务器上。下面说一下如何在本地和云服务器上运行脚本。

## 本地

#### 环境

1. windows10
2. python3
3. chrome 版本 88.0.4324.104（正式版本） （64 位）

#### 运行

1. Clone过来后，在项目文件下创建webdriver文件夹，同时创建login_information.csv文件。

2. 在chrome的“关于”中找到自己的版本号，然后去[镜像网站]( http://npm.taobao.org/mirrors/chromedriver)下载对应的chromedriver放到webdrive下面。

3. 在csv文件中按照 账号,密码 的格式逐行填写要填报的人的名字。
4. 直接运行即可

## 云服务器

#### 环境

1. 阿里ECS突发性能型 t5(免费一个月)
2. python 3
3. Ubuntu 18.04



#### 运行

**初始化服务器**

我们的任务是每天定时签到，只在部分时刻cpu资源消耗大，所以采用突发性能服务器。领取了免费的阿里云服务器之后选择Ubuntu 18.04作为系统。这一步他会让你输入两个密码，一个是进行连接操作时候的密码，一个是服务器自己的密码，我们在后续连接时都用的是后者。



**在windows上安装openSSH服务**

这一步是为了让windows能够和远程服务器连接

1. 下载openSSH windows版（注：该版本是64位）

   > ​	链接: https://pan.baidu.com/s/19V2W_e1Agl4GSouW6U3JAQ   提取码: xgjp

2. 解压到C:\Program Files\OpenSSH  不要放在别的路径下，官方这样要求的

3. 用管理员身份运行cmd到openSSH路径下,依次执行

    1）安装sshd服务

    ```bash
    powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
    ```

    2）开放22号端口（如果你在windows关闭了防火墙并配置了入站规则可以不执行如下命令，多执行不影响）

    ```bash
    netsh advfirewall firewall add rule name=sshd dir=in action=allow 		protocol=TCP localport=22
    ```

    3）配置开机自启sshd服务

    ```bash
    sc config sshd start= auto
    ```

4. 将C:\Program Files\OpenSSH添加到path中，免得每次都要切到C:\Program Files\OpenSSH才能使用ssh，启动ssh服务

5. 测试。在cmd中输入```ssh root@'IP'```,IP是你的公网Ip地址，在云服务器的控制台可以查看到。输入服务器的账号密码。如果能够进入root用户说明成功连接。

6. ssh出于安全考虑，每次连接都会提示输入密码，为了避免麻烦，就要配置密钥对。

   1）生成密钥对命令。在cmd中执行下面的命令。

   ```bash
   ssh-keygen -t rsa
   ```

   这里采用rsa算法，你也可以使用其他算法，但dsa默认不支持，这里是个坑，最好生成rsa密钥，ssh支持，随自己吧。

   运行输出结果大概如图：

   ```
   Generating public/private rsa key pair.
   Your identification has been saved in ./test.
   Your public key has been saved in ./test.pub.
   The key fingerprint is:
   SHA256:S7N4ThFZs21lICbyOUV2EQEUxc61rNw6X+ig0Kzk1fM test@mail.com
   The key's randomart image is:
   +---[RSA 4096]----+
   |      . .o%=B=o  |
   |       o O *.o.  |
   |        * .ooo . |
   |         o .o o  |
   |        S  . o   |
   |       o B .o .. |
   |      . B + +.. .|
   |       * + .o= . |
   |        + .  oE  |
   +----[SHA256]-----+
   ```

   运行成功后会在当前目录生成`test`（私钥匙）和`test_pub`（公钥）文件

   ```bash
   -rw-------  1 Ryou  staff  3434  8 23 13:10 test
   -rw-r--r--  1 Ryou  staff   739  8 23 13:10 test.pub
   ```

   2）用```cd ~/.ssh```到指定目录下，然后打开```vi authorized_keys``` ，把```id_rsa.pub```的内容放到里面。

7. 重启远程服务器，下次登录时便可以直接重连。



**在vscode上连接服务器**

1. 安装`VsCode`官方插件`Remote - SSH`
2. 建立新连接,我们点击侧边远程连接的图标，鼠标移至`TAG`栏,选择SSH Targets，点击`+`在弹出框里输入`ssh`连接```ssh root@'IP'```
3. 点击生成的远程连接，打开终端即可。



**在服务器上部署环境**

ECS买过来基本都预装好了python3，在usr/bin 目录下，如果没有的话，就自己预装一下。

1. 下载对应的python库，pip3一键安装。

2. 安装chrome。用下面的命令安装Google Chrome

   ```
   wget install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
   ```

   安装必要的库

   ```
   yum install mesa-libOSMesa-devel gnu-free-sans-fonts wqy-zenhei-fonts
   ```
   用```google-chrome --version```命令查看chrome的版本号
   
3. 安装 chromedriver,从刚才的镜像网站直接下载对应的版本。比如我的版本是88.0.4324，那么执行下面指令。
   ```
	wget http://npm.taobao.org/mirrors/chromedriver/88.0.4324/chromedriver_linux64.zip
   ```

   将下载的文件解压，放在如下位置

   ```
   unzip chromedriver_linux64.zip
   
   mv chromedriver /usr/bin/
   ```
   
   给予执行权限
   
   ```
   chmod +x /usr/bin/chromedriver
   ```
   
4. 运行代码，查看是否成功（python下）
   
   ```python
   from selenium import webdriver
   driver = webdriver.Chrome()
   ```
   
   如果发出这样的错误是没有关系的，这个是因为没有图标打不开的缘故，在之后的代码里面用无头浏览器即可
   
    ```python
   Message: unknown error: Chrome failed to start: exited abnormally.
     (unknown error: DevToolsActivePort file doesn't exist)
    ```
   
   

**运行程序**

1. 同样在目录下创建login_information.csv文件，此时不需要创建webdriver,因为webdriver和执行的python3解释器在一个目录下，会直接找到。

2. 更改webdriver的参数。

   ```python
   chrome_options = Options()
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')
   chrome_options.add_argument('--headless')
   browser = webdriver.Chrome(chrome_options=chrome_options)
   ```

3. 运行，查看终端是否输出成功填报。



**定时执行**

我们采用crontab定时服务

1. 用root权限编辑以下文件

   ```
    	code /etc/crontab
   ```
   
2. 在文件末尾添加以下命令
   ```
    	01 0 * * * root /usr/bin/python3 /root/try/try.py >> /root/try/try.log
   ```
 有关crontab的编写格式
   ```  
   *   *   *   *   *   user    command
   分  时  日  月  周   用户    命令
   ```
    每个类型严格空一格，指明解释器，运行文件。最后加上>> .log是为了让print的内容输出到log里面，>>是直接在log尾部添加，>直接覆盖。
   
3. 将代码里面的相对路径改为绝对路径
   ```python
 with open('/root/try/login_information.csv') as f
   ```
4. 只要云服务器一直开着，便会一直自动执行，可以从try.log里面查看是否运行。
   
   
   



