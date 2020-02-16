---
title: 使用setuptools和twine把项目打成pip包
date: 2020-1-25 16:25
categories: 技术文章
tags:
    - Python
---

本文章是在打包web-mysql和nested-list时根据官方教程在实践后后写下的，可以边参考官方教程边阅读本文章，这样可能有助于您理解如何去把项目打包成一个pip软件包

本人使用的是Python3，操作可能会和Python2有点不同，同时使用的命令是参考了其他的教程，和官方命令也不太一样，免去了许多参数的选择，更加简单。

如果希望更加全面地理解和打包pip软件包请参考

官方教程：<https://packaging.python.org/tutorials/packaging-projects/>

需要使用到的东西
---

两个Python包：setuptools、twine

一个PyPI账号：<https://pypi.org/>

打一个pip软件包一定要有这两个工具，setuptools用于创建构建脚本，twine用于上传项目，上传的pip包都会放在这里PyPI

打包一个项目的文件结构
---

```Text
软件包根目录/
    打包的项目/
        __init__.py
        ...
    setup.py
    LICENSE
    README.md
```

根目录的名字不知道对项目名有没有影响，我都是直接取发行名称

在这个目录下，最简单的配置包括4个部分：

```Text
要打包的项目：你准备打包成pip包的项目
setup.py：构建脚本，里面写的是软件包的相关信息和代码配置信息
LICENSE：软件包使用的许可证
README.md：说明文件
```

打包配置
---

打包的项目就不说了，可能你是直接打包已有项目，也可能是打算打包从头写的项目，打包的关键步骤主要是setup.py的配置和上传命令的使用，上传项目时软件包的信息都是根据setup里面的配置来上传的

**把官方setup.py的配置简化一下就是以下的样子,三个点代表省略:**

```Python
import setuptools

# 这里从README导入详细说明
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE", # pip软件包发行的名称
    version="0.0.1", # 本次上传的版本
    author="Example Author", # 作者名称
    author_email="author@example.com", # 作者邮箱
    description="A small example package", # 软件包摘要
    long_description=long_description, # 软件包详细说明
    long_description_content_type="text/markdown", # 引用详细说明的文件格式
    url="https://github.com/pypa/sampleproject", # 项目的主页地址，大部分是使用该项目在自己代码储存库的地址
    license="MIT" # 许可证类型
    packages=setuptools.find_packages(), # 要打包的所有Python包列表
    # 是列出了你的包的额外元数据，给你的包进行分类，下面的意思是“该软件包仅与Python 3兼容，已获得MIT许可，与操作系统无关”
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 能够使用你的项目的Python版本
    python_requires='>=3.6',
    # 你的项目的依赖项，安装你的软件包时，pip也会自动安装以下依赖项，举个例子--pymysql
    install_requires = [
        'pymysql',
        ...
    ]
    ...
)
```

**官方全部字段的配置说明：<https://packaging.python.org/guides/distributing-packages-using-setuptools/>**

**配置文件的时候有几个注意点：**
**1、上传不同版本的软件包，version要修改，因为生成的压缩包版本后缀是根据这一行配置的**
**2、packages可以手动列出需要打包的Python包列表，如果使用`find_package()`的话则是脚本自动发现所有软件包和子软件包**
**3、关于classifiers的配置根据不同项目配置都不一样，参考官方分类器列表：<https://pypi.org/classifiers/>**
**4、如果设置了python_requires，那么所有不符合要求的Python版本都会被pip阻止安装这个软件包**

**配置完setup.py，接下来就是根据你的需要选择许可证：<https://choosealicense.com/>**
**选择完许可证要把许可证文本写入LICENSE文件，或者也可以在使用GitHub Desktop创建仓库时创建许可证，如果setup.py里有配置license这一项记得修改成对应的类型**

打包
---

打包前，要先check一下，看看setup的配置是否有效

在软件包根目录使用命令：`setup.py check`

如果只显示了running check就是正常的

如果没问题使用sdist进行打包

`setup.py sdist`

生成的压缩包会放在dist/下面，把这些包上传就完成了，但是上传前还要进行一次检查，看看压缩包是否符合要求

检查命令：`twine check dist/*`

上传命令：`twine upload dist/*`

输入用户名和密码就可以了

**这里也有几个注意点：**
**1、有些教程会使用`setup.py register`来进行注册上传，但是这个方法其实已经弃用了，官方推荐是直接使用`twine upload`**
**2、dist/*是指dist下的全部文件，如果上传的压缩包含有以前的版本，因为该版本已经上传过了，会有错误提示，可以把以前版本的压缩包删掉，也可以自己选择上传的包，而不是全部上传**
**3、我这里没有配置用户文件，配置文件可以免去验证用户的流程**
**4、官方推荐是注册令牌来代替用户名和密码上传，注册令牌是一种更安全可靠的方式**

如果以上步骤都没问题，你就可以在自己的账号上面看到上传的pip软件包了

——更多内容待更新——
