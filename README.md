# ElectronPy
A Visualization tool of Halomonas bluephagenesis TD01 metabolic network based on Electron with Python, communicate by thrift


## 原理

![原理](https://github.com/kekegg/HalomonasBluephagenesisTD01/blob/main/td01_1.png)
![原理](https://github.com/kekegg/HalomonasBluephagenesisTD01/blob/main/td01_2.png)

## 环境部署

1. 首先创建一个文件夹.

2. 进入文件夹,初始化`npm`项目:`npm init`

3. 初始化后会出现一个 `package.json` 文件,这里会说明该 `npm` 项目的基本信息.

4. 在 `package.json` 中修改 `scripts` ,增加一行命令(缩写):
```
{
  "name": "electronpy",
  "version": "0.0.0",
  "description": "A test project for electron with python",
  "main": "index.js",
  "scripts": {
    "start": "electron ."
  },
  "author": "",
  "license": ""
}

```

5. 下载npm所需环境
```
npm install electron
npm install thrift
```
> 这一步后会看到新建了一个`node_modules`文件夹,这里会保存npm的第三方包(local的,如果安装命令加了-g,就会全局安装)

6. 创建并激活Python虚拟环境(如果没有这一步,打包的体积会巨大,因为会把乱七八糟有的没的的包都给打包进去)
```
python -m venv envpy
source envpy/bin/activate # Ubuntu, bash/zsh activate, in other platform, please activate by other scripts
pip install thrift # install thrift in this python env
```

7. 安装[thrift](https://thrift.apache.org/)本体
> Windows直接下载exe即可,放在本地目录里或者放在特定文件夹,然后加入PATH里就行.
> Linux/Unix 需要下载tar.gz, 解压安装
```
./configure
sudo make
sudo make install
thrift -version         # Test whether the thrift is installed well or not
```

## 新建各种文件

1. [生成接口文件](https://thrift.apache.org/tutorial/)

thrift提供的接口[变量格式](https://thrift.apache.org/docs/types)在官网有说明

```
# test.thrift in root path
service userService {
    string test1(1:string name)
}
```

生成nodejs接口文件
```
# thrift -out 存储路径 --gen 接口语言 thrift接口文件名
thrift --gen js:node test.thrift 
thrift -out py --gen py test.thrift 
```

## Electron打包

打包分为三步:

1. 打包Python文件
2. 修改js中调用Python的代码
3. 打包Electron

### 打包Python

Python 打包工具比较经典的是 `pyinstaller`, 但是打包的时候打包依赖项有点坑, 还有一个比较新的打包工具为 `nuitka` 用它打包可能会更方便一点点.而且它会把代码编译好,据说执行效率会更高

首先安装这个打包工具 `pip install nuitka`, 如果是Windows用户,可能需要安装别的依赖工具,Mac用户安装Xcode-commandline-tool后应该就可以了

执行打包命令

```
python -m nuitka py/thrift_server.py --follow-imports
```

这里的 `--follow-imports` 会把依赖文件一同打包进去,如果不加这一命令,就会出现依赖错误.

打包完成后,根目录下会出现 `thrift_server.bin` 文件,这个就是Python编译好的二进制文件

### 修改调用
接下来要在 `index.js` 中修改一下调用,之前的调用其实就只是用Python执行了.py文件,现在要改为执行这个新的二进制文件.

```js
let script = path.join(__dirname, 'thrift_server.bin')
pyProc = require('child_process').execFile(script)
```

此时可以再 `npm start` 运行一下看是不是正常的,如果正常就可以做最后的打包了

### Electron 打包

Electron的打包相对就正常得多,首先安装Electron打包工具
```
npm install electron-packager
```
然后打包
```
./node_modules/.bin/electron-packager . --overwrite --ignore=py$
```

这样会打包本机架构的包,比如在Ubuntu x64 下就会打包出 `electronpy-linux-x64` 文件夹,里面的 `electronpy` 就是编译好的二进制程序了,其他架构下编译出来的文件会有一点不同.




## 参考链接

* [Github:AlexTan-b-z/Electron-Python](https://github.com/AlexTan-b-z/Electron-Python)
* [Thrift](https://thrift.apache.org/)
* [Electron 例子](https://blog.csdn.net/weixin_41231535/article/details/105480435?spm=1001.2014.3001.5501)
* [Client on Node.js: Uncaught ReferenceError: require is not defined](https://stackoverflow.com/questions/19059580/client-on-node-js-uncaught-referenceerror-require-is-not-defined)
* [Electron require() is not defined](https://stackoverflow.com/questions/44391448/electron-require-is-not-defined)
* [nodejs thrift java_nodejs怎么调用thrift接口](https://blog.csdn.net/weixin_29009401/article/details/114205640)
* [使用 Web Serial API 在浏览器上实现基于 WEB 的串口通信](https://blog.csdn.net/weixin_41231535/article/details/115218293?spm=1001.2014.3001.5501)
* [numpy教程](https://www.runoob.com/numpy/numpy-tutorial.html)
* [Nuitka-Python 打包 Linux](https://zhuanlan.zhihu.com/p/353577753)
* [你不知道的Electron (二)-了解Electron打包](https://zhuanlan.zhihu.com/p/45250432)
