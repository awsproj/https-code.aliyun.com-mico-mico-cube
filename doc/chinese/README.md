## 介绍
*MiCO CLI* 是MXCHIP的MiCO命令行工具，脚本名称为：mico-cli。它用于完成基于MiCO的完整开发流程，包括：代码库版本管理，维护代码依赖，发布代码，从远程代码仓库更新以及启动MiCO编译系统实现编译，下载，调试等
该文档包含了MiCO CLI的安装和使用方法。

## 目录

1. [使用MiCO CLI](#使用mico-cli)
1. [安装](#安装)
1. [了解工作区和项目根目录](#写在最前-了解工作区和项目根目录)
1. [创建和导入项目](#创建和导入项目)
    1. [创建一个新项目](#创建一个新项目)
    2. [导入一个现有的项目](#导入一个现有的项目)
1. [增加和删除组件](#添加和移除组件)
1. [代码编译](#代码编译)
    1. [选择MiCoder Tool](#选择micoder-tools)
    2. [编译项目](#编译项目)
    3. [编译静态库](#编译静态库)
1. [导出到MiCoder IDE](#导出到-micoder-ide)
1. [推送改动](#推送改动)
    1. [检查本地状态](#检查本地状态)
    2. [推送到远端仓库](#推送到远端仓库)
1. [发布本地项目或组件](#发布本地项目或组件)
1. [升级项目和组件](#升级项目和组件)
    1. [升级到远端版本](#升级到远端版本)
    2. [升级示例](#升级示例)


## 使用MiCO CLI

MiCO CLI的基本工作流程是:

1. 新建或者导入一个项目或组件，并为它创建一个版本库。无论新建还是导入，都会在项目中自动附带一个MiCO OS的版本库.
1. 编译，下载和调试应用程序代码.
1. 发布您的应用程序.
除了以上基本的工作流，MiCO CLI针对长期的开发和维护，提供了额外的版本控制功能。它可以基于版本库进行选择性的升级，使得您的应用程序做包含的MiCO OS和其他组件在持续的更新中仍然能够维持开发时的版本，保障应用程序的可用性。
<span class="tips">**小窍门:** 使用`mico --help`可以列出所有MiCO CLI所支持的指令，特定某一个指令的帮助可以使用`mico <command> --help`。</span>

## 安装

MiCO CLI支持Windows, Linux和macOS。

### 要求

* **Python** - MiCO CLI 是一个Python脚本，所以您需要在系统中安装Python。MiCO CLI在[Python version 2.7.13 ](https://www.python.org/downloads/release/python-2713/)下开发和测试. 不兼容Python 3。
    
    <span class="tips">**注意:** Python的可执行文件目录(`Python`)需要添加到系统的PATH环境变量中，在Python安装时指定。</span>

* **Git or Mercurial** - MiCO CLI 支持Git和Mercurial两种, 任选其一安装即可:
    * [Git](https://git-scm.com/) - 版本 1.9.5 及以上。
    * [Mercurial](https://www.mercurial-scm.org/) - 版本 2.2.2 及以上。

    <span class="tips">**注意:** Git和Mercurial的可执行文件目录需要添加到系统的PATH环境变量中。</span>

* **MiCoder Tools or MiCoder IDE** - MiCO CLI 调用MiCO OS中的脚本来完成诸如编译，下载，调试等各项功能. 这些脚本的运行需要用到MiCoder Tools，您可以直接下载MiCoder Tools或者安装包含了MiCider Tools的MiCoder IDE：
    * MiCoder Tools - 版本1.1及以上。
        * [MiCoder Tools for  Windows 32bit](http://7xnbsm.com1.z0.glb.clouddn.com/MiCoder_v1.1.Win32.zip)
        * [MiCoder Tools for  macOS 32bit](http://7xnbsm.com1.z0.glb.clouddn.com/MiCoder_v1.1.macOS.tar.gz)
        * [MiCoder Tools for  Linux](http://7xnbsm.com1.z0.glb.clouddn.com/MiCoder_v1.1.Linux.tar.gz) 
    * MiCoder IDE  - 版本1.2.1及以上（包含MiCoder Tools）。
        * [MiCoder IDE Windows x86 Installer](http://ok0noocp1.bkt.clouddn.com/MiCoder_IDE_1_2_1_Win32_x86.exe) (Windows 32位)
        * [MiCoder IDE Windows x64 Installer](http://ok0noocp1.bkt.clouddn.com/MiCoder_IDE_1_2_1_Win32_x64.exe) (Windows 64位)
        * [MiCoder IDE macOS Installer](http://ok0noocp1.bkt.clouddn.com/MiCoder_IDE_1_2_macOS.pkg) (macOS)
        * [MiCoder IDE Linux Installer]()(准备中)

### 安装MiCO CLI

您可以从代码仓库中获取开发中的MiCO CLI [https://code.aliyun.com/mico/mico-cli](https://code.aliyun.com/mico/mico-cli):
```
$ git clone https://code.aliyun.com/mico/mico-cli.git
```
克隆完成后，通过以下命令安装MiCO CLI:
```
$ python setup.py install
```
在Linux和Mac上, 需要加上`sudo`获得安装权限.


## 写在最前: 了解工作交换区和项目根目录

MiCO CLI和Git，Mercurial等其命令行工具一样，使用当前路径作为工作交换区。所以当您执行任何MiCO CLI命令之前，需要首先将当前路径切换到包含需要操作的代码目录。例如，如果您需要升级你的 ``mico-example-program``项目中的MiCO OS的源代码：
```
$ cd mico-example-program
$ cd mico-os
$ mico update master   # This will update "mico-os", not "mico-example-program"
```
大量的MiCO CLI功能需要一个基于版本控制 [Git](https://git-scm.com/) 或者 [Mercurial](https://www.mercurial-scm.org/) 的项目根目录. 他使得整个项目以及包含的组件能够自由地切换版本，管理历史记录，与版本库同步，与其他开发者共享等等。MiCO OS也是包含版本管理的开源项目，允许各个开发者向MiCO OS贡献代码。

<span class="warnings">**注意**: MiCO CLI 在以`.component` 为后缀的文件（例如`lib_name.component`）中保存依赖组件的链接信息; 以`.code` 为后缀的文件（例如`name_src.codes`）中保存可选依赖组件的链接信息. 这些文件都是可读的文本文件，但是我们强烈建议不要手动修改文件的内容，而是使用MiCO CLI的相应命令来自动生成和修改，例如：`$ mico sync`。这些文件我们称之为依赖描述文件。</span>


## 创建和导入项目

MiCO CLI可以创建和导入基于MiCO OS 4的软件项目。

### 创建一个新项目

每当你创建一个新项目，MiCO CLI自动导入最新的 [mico OS](https://code.aliyun.com/mico/mico-os)。 每一个发布都包含了所有组件:  代码和编译调试脚本。

接下来让我们来创建一个新的项目 (命名为`mico-os-program`):

```
$ mico new mico-os-program
[mico] Creating new program "mico-os-program" (git)
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os" at latest revision in the current branch
[mico] Updating reference "mico-os" -> "https://code.aliyun.com/mico/mico-os/#89962277c20729504d1d6c95250fbd36ea5f4a2d"
```

这个命令创建了一个新的目录"mico-os-program"，初始化了一个新的版本库并且在项目中导入了一个最新版本的mico-os依赖。

<span class="tips">**Tips:** 使用参数`--scm [name|none]`， 您能够选择版本库的格式，或者选择不初始化版本库。</span>

使用`mico ls`列出项目中所有导入的组件

```
$ cd mico-os-program
$ mico ls -a
mico-os-program (mico-os-program)
`- mico-os (https://code.aliyun.com/mico/mico-os/#89962277c207)
```

<span class="notes">**Note**: 如果您从一个现有的空目录开始，可以使用`mico new .`命令来初始化MiCO项目，并且在该文件夹中初始化版本仓库。</span>


### 创建不包含MiCO OS的新项目

你可以通过命令参数 `--create-only` 来创建一个不包含MiCO OS的空工程。

### 导入一个现有的项目

你可以使用 `mico import` 命令从一个版本仓库克隆一个项目到本地，并且部署所有依赖项：

```
$ mico import https://code.aliyun.com/mico/helloworld.git
[mico] Importing program "helloworld" from "https://code.aliyun.com/mico/helloworld.git" at latest revision in the current branch
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os.git" at rev #dd36dc4228b5
$ cd helloworld
```

如果你在"import"命令中不指定完整的路径，MiCO CLI会自动加上默认的路径前缀 (https://code.aliyun.com/mico) 。例如，以下命令:
 
```
$ mico import helloworld
```

与这个命令等价
 
```
$ mico import https://code.aliyun.com/mico/helloworld.git
```

### 从一个现有的 Git 或 GitHub 克隆导入

如果你在工作区中手动克隆了一个Git版本库，现有想要添加所有丢失的依赖组件。可以使用 `deploy` 命令：

```
$ mico deploy
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os.git" at rev #dd36dc4228b5
```

然后，不要忘了将当前项目路径设置为项目根目录:

```
$ mico new .
```

## 添加和移除组件

在编写MiCO代码时，常常需要在应用程序中添加另一个组件（依赖），或者移除一个现有的组件。

MiCO CLI添加和删除功能不等同于``hg``, ``git``版本管理软件的内置功能，而是针对MiCO项目的特点进行了改造：

* 将新的组件添加到项目中不等同于从版本库中克隆一个仓库，所以不要使用 `hg` 或 `git` 命令，而要使用 `mico add` 来添加组件。它可以保证所有的依赖（组件以及子组件）都能被同时生成出来。
* 移除一个组件也不仅仅是删除这个组件目录 - 依赖描述文件（`.component`）也需要删除和升级。使用 `mico remove` 命令来移除组件，而不要简单地使用 `rm` 命令。

### 添加组件

使用 `mico add` 命令添加组件的最新版本：

```
$ mico add https://code.aliyun.com/mico/Lib_aws.git
```

可以使用URL#hash格式来添加一个组件的特定版本 format to add a library at a specific revision:

```
$ mico add https://code.aliyun.com/mico/Lib_aws.git/#e5a0dcb43ecc
```

### 移除组件

如果不再需要一个组件，你能够使用 `mico remove` 命令来删除这个组件：

```
$ mico remove Lib_aws
```

## 代码编译

### 选择MiCoder Tools

完成项目创建和导入后，你需要为MiCO CLI设置MiCoder Tools的路径，以便MiCO CLI调用这些工具来编译MiCO项目。

你可以通过以下命令来设置MiCoder Tools的路径：

```
$ mico config --global MICODER ~/MiCO_SDK/MiCO/MiCoder
[mico] /Users/william/MiCO_SDK/MiCO/MiCoder now set as default MICODER in program "helloworld"
```

`-G` 或 `--global` 开关可以让MiCO CLI设置一个全局的参数，而不是针对当前项目的私有参数。

你可以通过下面的命令查看 MiCO CLI 的有效配置参数：

```
$ mico config --list
[mico] Global config:
TOOLS_ROOT=/Users/william/Develop/MiCO_SDK/MiCO/MiCoder/

[mico] Local config (/Users/william/Develop/mico-program/helloworld):
MICODER=/Users/william/Develop/MiCO_SDK/MiCO/MiCoder
```


### 编译项目

使用`mico make` 命令来编译项目:
```
$ mico make helloworld@MK3165
make helloworld@MK3165
Making config file for first time
processing components: helloworld MK3165 FreeRTOS LwIP wolfSSL MiCO
MiCO core based on pre-build library: ===MiCO.3165.GCC.a=== 
Skipping building bootloader due to "total" is not set

Compiling App_Helloworld
Compiling Board_MK3165
Compiling FreeRTOS
... [SNIP] ...
Making build/helloworld@MK3165/libraries/STM32F4xx_Peripheral_Libraries.a
Making helloworld@MK3165.elf

Making helloworld@MK3165.hex
Making helloworld@MK3165.bin

                        MICO MEMORY MAP                            
|=================================================================|
| MODULE                                   | ROM       | RAM      |
|=================================================================|
| App_Helloworld                           | 141       | 0        |
... [SNIP] ...
| STM32F4xx_Peripheral_Drivers             | 9299      | 236      |
| STM32F4xx_Peripheral_Libraries           | 5948      | 16       |
| *fill*                                   | 253       | 926      |
|=================================================================|
| TOTAL (bytes)                            | 243524    | 34971    |
|=================================================================|
Build complete
Making .gdbinit
Making .openocd_cfg
```

*make* 编译参数如下:

* `<target>`用于选择编译目标. 目标由参与编译的各个组件构成, 以下的每一个组件用'@'分割开来。
    * `Application` （项目中需要编译的应用程序组件，即应用程序在项目中的路径，并将`/`替换成`.`）
    * `Board` ( `mico-os/board/*`中定义的硬件平台组件 )
    * `[RTOS]` ( `mico-os/MiCO/rtos/*`中定义的RTOS内核组件, 默认使用 `FreeRTOS` )
    * `[Network Stack]` ( `mico-os/MiCO/net/*`中定义的网络协议栈组件，默认使用 `LwIP` )
    * `[TLS]` ( `mico-os/MiCO/security/TLS/*`中定义的安全传输组件, 默认使用 `wolfSSL` )
    * `[debug | release_log | release]` ( 编译选项默认使用`release_log` ） 
<span class="notes">**Note**: 如果你使用moc平台，例如 `MK3031`, `MK3080`, 添加 `moc` 等同于同时添加 `mocOS@mocIP@mocTLS`。 </span>

* `[download]` 下载目标固件到硬件平台。
* `[run|debug]` 通过仿真器复位硬件并运行程序或者连接到目标处理器进行调试。
* `[JTAG=xxx]` mico-os/makefiles/OpenOCD/interface 中定义的JTAG接口配置文件。默认使用`jlink_swd`。
* `[VERBOSE=1]` (可选) 显示编译过程中运行的命令。
* `[JOBS=<jobs>]` (可选) 控制多线程编译，提高编译速度。默认值是 4。可以根据处理器核心的数量来设置这个参数，也可以使用 `JOBS=1` 来执行单线程的顺序编译.

编译生成的可执行文件，ELF文件，内存使用和链接数据可以在 `build/<target>/binary` 目录下找到。


### 编译静态库


## 导出到 MiCoder IDE

MiCoder IDE可以导入MiCO项目，这样不仅可以在图形化界面下编写代码，还可以很方便地调试。MiCO CLI会自动在项目根目录下生成MiCoder IDE的工程文件(`.project` 和 `.cproject`) ，然后你随时可以用MiCoder IDE导入当前项目。

1. 启动 MiCoder IDE。
1. 导入MiCoder工程。 (点击 File > Import, 选择 General > Existing Projects into Workspace)
1. 修改当前调试的项目 （点击 Debug Configurations > GDB Hardware Debugging > MiCO, 将  Project 设置成当前 project )，点击Apply。
1. 连接仿真器硬件，设置断点，启动调试。
 

## 推送改动

### 检查本地状态

在软件开发过程中，你总是会对你的代码或者是依赖的组件中的代码进行修改。通过运行 `mico status` 命令，你可以递归地获得当前项目以及所有依赖组件的修改状态，如果版本库中有没有提交的修改，指令的运行结果会显示这些改动。
例如：


```
[mico] Status for "helloworld":
 M helloworld/helloworld.c

[mico] Status for "mico-os":
 M platform/MCU/STM32F4xx/platform_init.c
```

你可以提交或者丢弃这些改动。

### 推送到远端仓库

使用 `mico publish`命令将本地的改动推送到远端。`publish` 是递归执行的，它首先推送树叶依赖项，然后更新上层的依赖描述文件，再推送上层. 

下面举一个例子说明，假设我们的项目的依赖关系如下（使用 `mico ls` 命令）：

```
my-mico-os-example (a5ac4bf2e468)
|- mico-os (5fea6e69ec1a)
`- my-libs (e39199afa2da)
   |- my-libs/iot-client (571cfef17dd0)
   `- my-libs/test-framework (cd18b5a50df4)
```

我们假设在 `iot-client` 组件上作了修改。  `mico publish` 会执行以下操作：

1. 检测树叶依赖项 `iot-client` ，并且询问你是否要提交改动。
2. 检测父项 `my-libs`。
 * 更新 `my-libs` 的依赖描述文件（ `iot-client.component`  文件），将描述文件中的链接地址更新到最新的 `iot-client` 版本。
 * 再询问您是否要提交`my-libs` 的改动。
3. 最终检查 `my-mico-os-example` 项目，更新依赖描述文件并提交。 

## 发布本地项目或组件

当你新建一个新的（本地）基于版本控制的项目或者组件，他们的版本历史仅存在于本地，而没有远程仓库同步。你可以按照以下步骤将本地版本库推送到远端，而不丢失本地保存的历史版本：


1. 首先在远程服务器上创建一个新的版本库，服务器可以是一个公共的代码管理服务（ GitHub, Bitbucke，code.aliyun 等），你自己的私有服务，甚至是你本地系统上的另一个地址 (例如创建一个本地版本库 `mico-os-example/local-lib`)。
3. 关联远程仓库。
 * 使用Git命令 `git remote add origin <url-or-paht-to-your-remote-repo>`.
4. 运行 `mico publish` 来发布您的改动。


在使用了嵌套的本地版本库，应先从叶子版本库开始。


### 从原始仓库派生的工作流: Forking

Git支持非对称工作流：发布／推送的远端仓库和原始("origin")不同。这就使得新的版本存放在一个由原始仓库派生的版本仓库中的同时，又可以和原始的仓库保持同步。通过这种方式，在一个有没有权限的仓库派生的仓库中修改代码，完成版本的同步，最终向原始仓库提交推送请求。

为了实现这个功能，应首先导入一个MiCO OS项目或者MiCO OS本身，然后设置推送目标到一个由原始仓库派生（"Fork"）的远程仓库。例如：


```
$ git remote set-url --push origin https://code.aliyun.com/william/repo-fork.git
```

这样，每次你使用`git`来提交或者推送，或是使用 `mico publish`，新的版本将会推送到你的派生仓库。你仍然可以从原始仓库中通过 `mico update` 或 `git pull`更新版本。如果你希望从你的衍生仓库拉取版本，可以使用`git pull https://github.com/screamerbg/repo-fork [branch]`。

通过上面描述的工作流，MiCO CLI 保持了与原始版本库（最终你会提交一个推送请求）的联系，并且记录了你推送到衍生版本库的版本记录。在原始仓库接受您的衍生仓库生成的推送请求（ pull request ）之前，所有记录的版本链接对于其他开发者都是无效的。一旦推送请求被接受，您的衍生仓库中的版本就变成了原始版本库的一部分，版本链接也就生效了。


## 升级项目和组件

你可以从远程仓库中拉取改动到本地项目和组件。

在升级时，有两种主要的应用场景：

* 升级到 *持续更新* 版本, 例如一个分支的最新版本。
* 升级到 *特定* 版本，版本通过提交的哈希值或者标签名称来定义。

每一种场景又两种案例：

* 更新并保留本地的改动 - *肮脏* 升级。
* 更新并删除本地的改动 - *干净* 升级。

和其他的MiCO CLI命令一行，`mico update` 命令使用当前目录作为工作交换区，所以在执行`mico update` 之前，应首先将当前的工作目录切换到需要更新的版本库目录。例如，如果你需要更新mico-os，先使用 `cd mico-os` 。

<span class="tips">**Tip: 同步组件链接:** 在触发更新之前，你可能需要同步您之前对项目架构所做的改动，``mico sync`` 命令可以自动更新必须的组件依赖描述文件，并且删除无效的描述文件。</span>

### 防止覆盖 本地修改

如果在执行升级时，如果本地的改动会被覆盖， `update` 命令会直接报错。这是MiCO CLI的设计初衷，防止任何本地未提交的改动被覆盖，从而丢失代码。所以在升级时如果出错，看一下本地的改动（提交，或者使用下面的选项），然后重新运行`update`。

### 升级到远端版本

___升级项目___

要将你的项目升级到远程仓库的另一个版本，先进入项目的根目录，然后运行：

```
$ mico update [branch|tag|revision]
```

该命令从远程仓库读取版本，将当前项目升级到指定的分支，标签和版本。如果都没有指定，则升级到当前分支的最新版本。该命令是递归执行的，新版本项目中的所有依赖和子依赖都同步更新。


___升级组件___

当你将当前工作目录切换到组件的目录下，执行 `mico update` 可以升级组件和他的依赖项到另一个版本，而不是父项目中依赖描述文件中指定的版本。这个功能允许你使用非原本项目树中指定的版本来进行实验，而不需要去修改软件项目或是上级组件。

### 升级示例

以下示例帮助你理解MiCO CLI的各种升级选项。

**案例 1: 我要升级一个项目或者组件到指定的或当前分支的最新版本**

__我希望保留本地未提交的改动__ 

运行 `mico update [branch]`。
如果本地有改动则命令会报错，除非你用版本控制工具（Git）将这些改动提交到一个分支 `git commit`，或者储藏起来`git stash`。

__我需要一个干净的升级（丢弃所有本地未提交的改动）__

运行 `mico update [branch] --clean`

在 `mico update` 命令中指定另一个远程分支，仅仅将这个分支check out出来，而不会合并或者fast-forward。你也可以使用 `mico update`命令，不加参数来获得远程仓库中的最新版本并与本地版本进行合并（fast-forward）。“mico update”和`git pull`等价。

<span class="warnings">**Warning**: `--clean` 告诉MiCO CLI升级项目或者组件以及他们的依赖项，并且覆盖所有本地的改动。这个操纵无法复原，所以要谨慎执行。</span>

**Case 2: 我要升级一个项目或者组件到指定版本或者标签**
 
__我希望保留本地未提交的改动__ 

运行 `mico update [branch]`。
如果本地有改动则命令会报错，除非你用版本控制工具（Git）将这些改动提交到一个分支 `git commit`，或者储藏起来`git stash`。

__我需要一个干净的升级（丢弃所有本地未提交的改动）__

运行 `mico update <tag_name|revision> --clean`

__当我有未发布的本地组件__

这里有额外的三个选项来处理本地未发布的组件：

* `mico update --clean-deps` - 升级当前项目和组件以及他们的依赖项，丢弃所有本地未发布的版本库。所以用这个参数需要谨慎，因为你的本地未发布的版本库是无法恢复的。

* `mico update --clean-files` - 升级当前项目和组件以及他们的依赖项，丢弃所有未提交的改动，删除所有未跟踪或者忽略的文件。所以用这个参数需要谨慎，因为你的本地未发布的版本库是无法恢复的。

* `mico update --ignore` - 升级当前项目和组件以及他们的依赖项，丢弃所有未提交的改动并且忽略所有本地未发布的版本库（这些版本库不会被删除或修改，仅仅是忽略了）。

__合并升级选项__

在以下场景中，升级选项可以合并起来使用：

* `mico update --clean --clean-deps --clean-files` - 升级当前项目和组件以及他们的依赖项，丢弃所有本地未发布的版本库，丢弃所有未提交的改动，删除所有未跟踪或者忽略的文件。这个现象丢弃了所有你在本地项目和组件中所做的改动，恢复项目的布局。

* `mico update --clean --ignore` - 升级当前项目和组件以及他们的依赖项，但是忽略所有的本地未提交的版本库。MiCO CLI尽可能地从远端公共仓库获取新的版本。
