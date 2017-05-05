# MiCO Cube Reference Manual

## Introduction

**MiCO Cube** is the name of the MXCHIP MiCO developing manage tools, packaged as mico-cube, which enables the full mico workflow: repositories version control, maintaining dependencies, publishing code, updating from remotely hosted repositories and invoking MXCHIP MiCO's own build system and export functions, among other operations.

This document covers the installation and usage of MiCO Cube.

## Table of Contents

1. [Using MiCO Cube](#using-mico-cube)
1. [Installing and upgrading](#Installation)
    1. [Requirements](#requirements)
    2. [Installing MiCO Cube](#installing-mico-cube)
    3. [Upgrading MiCO Cube](#upgrading-mico-cube)
1. [Understanding working context and program root](#before-you-begin-understanding-the-working-context-and-program-root)
1. [Creating and importing programs](#creating-and-importing-programs)
    1. [Creating a new program](#creating-a-new-program-for-mico-os)
    2. [Importing an existing program](#importing-an-existing-program)
    3. [Importing from a Git clone](#importing-from-a-git-clone)
1. [Adding and removing components](#adding-and-removing-mico-components)
1. [Compiling code](#compiling-code)
    1. [MiCoder Tools selection](#micoder-tools-selection)
    2. [Compiling your program](#compiling-your-program)
    3. [Compiling static libraries](#compiling-static-libraries)
1. [Exporting to MiCoder IDE](#exporting-to-micoder-ide)
1. [Publishing your changes](#publishing-your-changes)
    1. [Checking status](#checking-status)
    2. [Pushing upstream](#pushing-upstream)
1. [Publishing a local program or component](#publishing-a-local-program-or-component)
    1. [Checking status](#checking-status)
    2. [Pushing upstream](#pushing-upstream)
1. [Updating programs and components](#updating-programs-and-components)
    1. [Updating to an upstream version](#updating-to-an-upstream-version)
    2. [Update examples](#update-examples)
1. [Troubleshooting](#troubleshooting)


## Using MiCO Cube

The basic workflow for MiCO Cube is to:

1. Initialize a new repository, for either a new application (or component) or an imported one. In both cases, this action also brings in the MiCO OS codebase.
1. Build, download and debug the application code.
1. Publish your application.

But MiCO Cube goes much further than the basic workflow. To support long-term development, MiCO Cube offers nuanced source control, support for selective updates of the codebase. It makes your application always functional while the included MiCO components are keeping update.

<span class="tips">**Tip:** To list all MiCO Cube commands, use `mico --help`. A detailed command-specific help is available by using `mico <command> --help`.</span>

## Installation

Windows, Linux and Mac OS X support MiCO Cube. 

### Requirements

* **Python** - MiCO Cube is a Python script, so you'll need Python to use it. We test MiCO Cube with [version 2.7.13 of Python](https://www.python.org/downloads/release/python-2713/). It is not compatible with Python 3.

    <span class="tips">**Note:** The directories of Python executables (`Python`) and Python installed script (`<Python dictory>/Scripts`) need to be in your system's PATH.</span>

* **Git or Mercurial** - MiCO Cube supports both Git and Mercurial repositories, so you'll need to install both:
    * [Git](https://git-scm.com/) - version 1.9.5 or later.
    * [Mercurial](https://www.mercurial-scm.org/) - version 2.2.2 or later.

    <span class="tips">**Note:** The directories of Git and Mercurial executables (`git` and `hg`) need to be in your system's PATH.</span>

* **MiCoder Toolchain or MiCoder IDE** - MiCO Cube invokes scripts in MiCO OS for various features, such as compiling, downloading and debugging. To run these scripts, you will need either MiCoder Tools **or** MiCoder IDE that includes MiCoder Tools, download and extract to a folder:
    * MiCoder ToolChain - version 1.1 or later.
        * [MiCoder Tools for  Windows 32bit](http://7xnbsm.com1.z0.glb.clouddn.com/MiCoder_v1.1.Win32.zip)
        * [MiCoder Tools for  macOS 32bit](http://7xnbsm.com1.z0.glb.clouddn.com/MiCoder_v1.1.macOS.tar.gz)
        * [MiCoder Tools for  Linux](http://7xnbsm.com1.z0.glb.clouddn.com/MiCoder_v1.1.Linux.tar.gz) 
    * MiCoder IDE
        * [MiCoder IDE Windows x86 Installer](http://ok0noocp1.bkt.clouddn.com/MiCoder_IDE_1_2_1_Win32_x86.exe) (Windows 32位)
        * [MiCoder IDE Windows x64 Installer](http://ok0noocp1.bkt.clouddn.com/MiCoder_IDE_1_2_1_Win32_x64.exe) (Windows 64位)
        * [MiCoder IDE macOS Installer](http://ok0noocp1.bkt.clouddn.com/MiCoder_IDE_1_2_macOS.pkg) (macOS)
        * [MiCoder IDE Linux Installer]()(Comming soon)

### Installing MiCO Cube

You can use command `pip install mico-cube` to install MiCO Cube:
```
$pip install mico-cube
Collecting mico-cube
  Downloading mico-cube-1.0.6.tar.gz
Installing collected packages: mico-cube
  Running setup.py install for mico-cube ... done
Successfully installed mico-cube-1.0.6
```
On Linux or Mac, you may need to run with `sudo`.

### Upgrading MiCO Cube

Once MiCO Cube installed，you can use command `pip install --upgrade mico-cube` to upgrade MiCO Cube to latest version.
```
$pip install --upgrade mico-cube
Collecting mico-cube
  Downloading mico-cube-1.0.6.tar.gz
Installing collected packages: mico-cube
  Found existing installation: mico-cube 1.0.0
    Uninstalling mico-cube-1.0.0:
      Successfully uninstalled mico-cube-1.0.0
  Running setup.py install for mico-cube ... done
Successfully installed mico-cube-1.0.6
```
On Linux or Mac, you may need to run with `sudo`.

<span class="tips">**Note:** MiCO Cube is compatible with [Virtual Python Environment (virtualenv)](https://pypi.python.org/pypi/virtualenv). You can read more about isolated Python virtual environments [here](http://docs.python-guide.org/en/latest/).</span>


## Before you begin: understanding the working context and program root

MiCO Cube uses the current directory as a working context, in a similar way to Git, Mercurial and many other command-line tools. This means that before calling any MiCO Cube command, you must first change to the directory containing the code you want to act on. For example, if you want to update the mico OS sources in your ``mico-example-program`` directory:

```
$ cd mico-example-program
$ cd mico-os
$ mico update master   # This will update "mico-os", not "my-program"
```

Various MiCO Cube features require a program root, which whenever possible should be under version control - either [Git](https://git-scm.com/) or [Mercurial](https://www.mercurial-scm.org/). This makes it possible to seamlessly switch between revisions of the whole program and its libraries, control the program history, synchronize the program with remote repositories, share it with others and so on. Version control is also the primary and preferred delivery mechanism for mico OS source code, which allows everyone to contribute to mico OS.

<span class="warnings">**Warning**: MiCO Cube stores information about component in reference files that use the `.component` extension (such as `lib_name.component`), and optional codes in reference files that use the `.codes` extension (such as `name_src.codes`). Although these files are human-readable, we *strongly* advise that you don't edit these manually - let MiCO Cube manage them instead: `$ mico sync`. </span>


## Creating and importing programs

MiCO Cube can create and import programs based on MiCO OS 4.

### Creating a new program for mico OS 4

When you create a new program, MiCO Cube automatically imports the latest [mico OS release](https://code.aliyun.com/mico/mico-os). Each release includes all the components: code and build scripts. 

With this in mind, let's create a new program (we'll call it `mico-os-program`):

```
$ mico new mico-os-program
[mico] Creating new program "mico-os-program" (git)
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os" at latest revision in the current branch
[mico] Updating reference "mico-os" -> "https://code.aliyun.com/mico/mico-os/#89962277c20729504d1d6c95250fbd36ea5f4a2d"
```

This creates a new folder "mico-os-program", initializes a new repository and imports the latest revision of the mico-os dependency to your program tree.

<span class="tips">**Tip:** You can control which source control management is used, or prevent source control management initialization, by using `--scm [name|none]` option.</span>

Use `mico ls` to list all the components imported to your program:

```
$ cd mico-os-program
$ mico ls -a
mico-os-program (mico-os-program)
`- mico-os (https://code.aliyun.com/mico/mico-os/#89962277c207)
```

<span class="notes">**Note**: If you want to start from an existing folder in your workspace, you can simply use `mico new .`, which will initialize an mico program, as well as a new Git or Mercurial repository in that folder. </span>


### Creating a new program without OS version selection

You can create plain (empty) programs, by using the `--create-only` option.

### Importing an existing program

Use `mico import` to clone an existing program and all its dependencies to your machine:

```
$ mico import https://code.aliyun.com/mico/helloworld.git
[mico] Importing program "helloworld" from "https://code.aliyun.com/mico/helloworld.git" at latest revision in the current branch
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os.git" at rev #dd36dc4228b5
$ cd helloworld
```

You can use the "import" command without specifying a full URL; a default prefix (https://code.aliyun.com/mico) is added to the URL. For example, this command:
 
```
$ mico import helloworld
```

is equivalent to this command:
 
```
$ mico import https://code.aliyun.com/mico/helloworld.git
```

### Importing from a Git clone

If you have manually cloned a Git repository into your workspace and you want to add all missing libraries, then you can use the `deploy` command:

```
$ mico deploy
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os.git" at rev #dd36dc4228b5
```

Don't forget to set the current directory as the root of your program:

```
$ mico new .
```

## Adding and removing MiCO components

While working on your code, you may need to add another mico component (dependency) to your application, or remove existing components. 

The MiCO Cube add and remove features aren't simply built-in versions of ``hg``, ``git`` and ``rm``; their functionality is tailored to the way mico OS and MiCO Cube work:

* Adding a new component to your program is not the same as just cloning the repository. Don't clone a component using `hg` or `git`; use `mico add` to add the component. This ensures that all dependencies - components or subcomponents - are populated as well.
* Removing a component from your program is not the same as deleting the library directory - there are library reference files that will need updating or cleaning. Use `mico remove` to remove the component; don't simply remove its directory with `rm`.

### Adding a component

Use `mico add` to add the latest revision of a component:

```
$ mico add https://code.aliyun.com/mico/Lib_aws.git/
```

Use the URL#hash format to add a component at a specific revision:

```
$ mico add https://code.aliyun.com/mico/Lib_aws.git/#e5a0dcb43ecc
```

### Removing a library

If at any point you decide that you don't need a library any more, you can use `mico remove` with the path of the library:

```
$ mico remove Lib_aws
```

## Compiling code

### MiCoder Tools selection

After importing a program or creating a new one, you need to tell MiCO Cube where to find the MiCoder Tools that you want to use for compiling your source tree.

The only way to do this is using MiCO Cube configuration: `mico config`.


#### Through MiCO Cube configuration

You can set the MiCoder Tools location via the command:

```
$ mico config --global MICODER ~/MiCO_SDK/MiCO/MiCoder
[mico] /Users/william/MiCO_SDK/MiCO/MiCoder now set as default MICODER in program "helloworld"
```

The `-G` or `--global` switch tells MiCO Cube to set this as a global setting, rather than local for the current program.

You can see the active MiCO Cube configuration via:

```
$ mico config --list
[mico] Global config:
MICODER=/Users/william/Develop/MiCO_SDK/MiCO/MiCoder/

[mico] Local config (/Users/william/Develop/mico-program/helloworld):
MICODER=/Users/william/Develop/MiCO_SDK/MiCO/MiCoder
```

More information about MiCO Cube configuration is available in the [configuration section](#mico-cube-configuration) of this document.

### Compiling your program

Use the `mico make` command to compile your code:
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

The arguments for *compile* are:

* `<target>` to select a target. Target is compiled by components, One each of the following mandatory [and optional] components separated by '@'
    * `Application` ( Application's directory under the program root, and replace `/` by `.` in path ) 
    * `Board` ( Hardware platform component defined under `mico-os/board/*` )
    * `[RTOS]` ( RTOS component defined under `mico-os/MiCO/rtos/*`, default is `FreeRTOS` )
    * `[Network Stack]` ( Network stack component defined under `mico-os/MiCO/net/*`, default is `LwIP` )
    * `[TLS]` ( TLS component defined under `mico-os/MiCO/security/TLS/*`, default is `wolfSSL` )
    * `[debug | release_log | release]` ( Building for debug or release configurations, defalut is `release_log` ）
<span class="notes">**Note**: If you are building a moc platform like `MK3031`, `MK3080`, add `moc` as a component equals to `mocOS@mocIP@mocTLS`. </span>

* `[download]` Download firmware image to target platform.
* `[run|debug]` Reset and run an application on the target hardware or connect to the target platform and run the debugger.
* `[total]` Build all targets related to this application and board.
* `[JTAG=xxx]` JTAG interface configuration file from the mico-os/makefiles/OpenOCD/interface dirctory, default is `jlink_swd`.
* `[VERBOSE=1]` (optional) Shows the commands as they are being executed.
* `[JOBS=<jobs>]` (optional) to control the compile threads on your machine. The default value is 4, which infers the number of threads from the number of cores on your machine. You can use `JOBS=1` to trigger a sequential compile of source code.

The compiled binary, ELF image, memory usage and link statistics can be found in the `build/<target>/binary` subdirectory of your program.、


### Compiling static libraries
Use the `mico makelib` command to build a static library of your own code.
The arguments for *mico makelib* are:
*`[--new]`for generating the prerequisite, `.mk` file, of compiling static libraries.
*`<source>`to select the directory of the source.

**Example:**
* 1. Assuming that the project directory is `helloworld`, the code, `mystaticlib.h` and `mystaticlib.c`, to be compiled is in directory `helloworld\mico-os\staticlib`. Open `mico cube`, change working directory to `helloworld`, run command `mico makelib --new`. A `.mk` file named `staticlib_src` will be created in directory `helloworld\mico-os\staticlib`.

```
$ mico makelib --new mico-os\staticlib
```

* 2. Add items -- arguments,definitions and file paths -- to the `.mk` file. In this case, a header file and a source file were added:

```
#
#  UNPUBLISHED PROPRIETARY SOURCE CODE
#  Copyright (c) 2016 MXCHIP Inc.
#
#  The contents of this file may not be disclosed to third parties, copied or
#  duplicated in any form, in whole or in part, without the prior written
#  permission of MXCHIP Corporation.
#

NAME := staticlib

# Add compiler flags here
$(NAME)_CFLAGS :=

# Add definations here
$(NAME)_DEFINES :=

# Add includes path here, should be realtive path to current directory
$(NAME)_INCLUDES := ./mystaticlib.h

# Add sources path here, should be realtive path to current directory
$(NAME)_SOURCES := ./mystaticlib.c
```

* 3. Run `mico makelib` command in `mico cube`, the static libraries will show in `helloworld\mico-os`.

```
$ mico makelib mico-os\mystaticlib

Compiling mico-os\mystaticlib/./mystaticlib.c
Make staticlib.Cortex-M3.GCC.release.a DONE

Compiling mico-os\mystaticlib/./mystaticlib.c
Make staticlib.Cortex-M4.GCC.release.a DONE

Compiling mico-os\mystaticlib/./mystaticlib.c
Make staticlib.Cortex-M4F.GCC.release.a DONE
```


## Exporting to MiCoder IDE

If you need to debug your code, a good way to do that is to export your source tree to MiCoder IDE, so you can use the IDE's debugging facilities. MiCO Cube generate MiCoder project file (`.project` and `.cproject`) under program's directory automatically. You can import program using MiCOder IDE and debug. 

1. Start MiCoder IDE.
1. Import application to MiCoder IDE. (From the File > Import, select General > Existing Projects into Workspace)
1. Change current debug project to current project (From the Debug Configurations > GDB Hardware Debugging > MiCO, change Project to current project ), and apply
1. Set breakpoints, and start a debug session.

## Publishing your changes

### Checking status

As you develop your program, you'll edit parts of it - either your own code or code in some of the libraries that it depends on. You can get the status of all the repositories in your program (recursively) by running `mico status`. If a repository has uncommitted changes, this command will display these changes. 

Here's an example:

```
[mico] Status for "helloworld":
 M helloworld/helloworld.c

[mico] Status for "mico-os":
 M platform/MCU/STM32F4xx/platform_init.c
```

You can then commit or discard these changes.

### Pushing upstream

To push the changes in your local tree upstream, run `mico publish`. `publish` works recursively, pushing the leaf dependencies first, then updating the dependents and pushing them too. 

This is best explained by an example. Let's assume that the list of dependencies of your program (obtained by running `mico ls`) looks like this:

```
my-mico-os-example (a5ac4bf2e468)
|- mico-os (5fea6e69ec1a)
`- my-libs (e39199afa2da)
   |- my-libs/iot-client (571cfef17dd0)
   `- my-libs/test-framework (cd18b5a50df4)
```

Let's assume that you make changes to `iot-client`. `publish` detects the change on the leaf `iot-client` dependency and asks you to commit it. Then it detects that `my-libs` depends on `iot-client`, updates the `my-libs` dependency on `iot-client` to its latest version (by updating the `iot-client.component` file) and asks you to commit it. This propagates up to `my-libs` and finally to your program `my-mico-os-example`.

## Publishing a local program or component

When you create a new (local) source-control managed program or component, its revision history exists only locally; the repository is not associated with the remote one. To publish the local repository without losing its revision history, please follow these steps:

1. Create a new empty repository on the remote site. This can be based on a public repository hosting service (GitHub, Bitbucke), your own service or even a different location on your system.
2. Copy the URL/location of the new repository in your clipboard and open command-line in the local repository directory (for example change directory to `mico-os-example/local-lib`).
3. To associate the local repository:
 * For Git - run `git remote add origin <url-or-paht-to-your-remote-repo>`.
4. Run `mico publish` to publish your changes.

In a scenario with nested local repositories, start with the leaf repositories first.

### Forking workflow

Git enables asymmetric workflow where the publish/push repository may be different than the original ("origin") one. This allows new revisions to land in a fork repository while maintaining an association with the original repository.

To achieve this, first import an mico OS program or mico OS itself and then associate the push remote with your fork. For example:

```
$ git remote set-url --push origin https://github.com/screamerbg/repo-fork.git
```

Each time you `git` commit and push, or use `mico publish`, the new revisions will be pushed against your fork. You can fetch from the original repository using `mico update` or `git pull`. If you explicitly want to fetch or pull from your fork, then you can use `git pull https://github.com/screamerbg/repo-fork [branch]`.

Through the workflow explained above, MiCO Cube will maintain association to the original repository (which you may want to send a pull request to) and will record references with the revision hashes that you push to your fork. Until your pull request (PR) is accepted, all recorded references will be invalid. Once the PR is accepted, all revision hashes from your fork will become part the original repository, so all references will become valid.

## Updating programs and components

You can update programs and libraries on your local machine so that they pull in changes from the remote sources (GitHub or Mercurial). 

There are two main scenarios when updating:

* Update to a *moving* revision, such as the tip of a branch.
* Update to a *specific* revision that is identified by a revision hash or tag name.

Each scenario has two cases:

* Update with local uncommitted changes - *dirty* update.
* Update without local uncommitted changes - *clean* update.

As with any MiCO Cube command, `mico update` uses the current directory as a working context, meaning that before calling `mico update`, you should change your working directory to the one you want to update. For example, if you're updating mico-os, use `cd mico-os` before you begin updating.

<span class="tips">**Tip: Synchronizing component references:** Before triggering an update, you may want to synchronize any changes that you've made to the program structure by running ``mico sync``, which will update the necessary library references and get rid of the invalid ones.</span>

### Protection against overwriting local changes

The update command will fail if there are changes in your program or library that `update` could overwrite. This is by design: MiCO Cube does not run operations that would result in overwriting local changes that are not yet committed. If you get an error, take care of your local changes (commit or use one of the options below), then rerun `update`.

### Updating to an upstream version

___Updating a program___

To update your program to another upstream version, go to the root folder of the program and run:

```
$ mico update [branch|tag|revision]
```

This fetches new revisions from the remote repository, updating the program to the specified branch, tag or revision. If none of these are specified, then it updates to the latest revision in the current branch. This series of actions is performed recursively against all dependencies and subdependencies in the program tree.

___Updating a library___

You can change the working directory to a library folder and use `mico update` to update that library and its dependencies to a different revision than the one referenced in the parent program or library. This allows you to experiment with different versions of libraries/dependencies in the program tree without having to change the parent program or library.

### Update examples

To help understand what options you can use with MiCO Cube, check the examples below.

**Case 1: I want to update a program or a library to the latest version in a specific or current branch**

__I want to preserve my uncommitted changes__ 

Run `mico update [branch]`. You might have to commit or stash your changes if the source control tool (Git or Mercurial) throws an error that the update will overwrite local changes.

__I want a clean update (and discard uncommitted changes)__

Run `mico update [branch] --clean`

Specifying a branch to `mico update` will only check out that branch and won't automatically merge or fast-forward to the remote/upstream branch. You can run `mico update` to merge (fast-forward) your local branch with the latest remote branch. On Git you can do `git pull`.

<span class="warnings">**Warning**: The `--clean` option tells MiCO Cube to update that program or library and its dependencies and discard all local changes. This action cannot be undone; use with caution.</span>

**Case 2: I want to update a program or a library to a specific revision or a tag**
 
__I want to preserve my uncommitted changes__ 

Run `mico update <tag_name|revision>`. You might have to commit or stash your changes if they conflict with the latest revision.

__I want a clean update (discard changes)__

Run `mico update <tag_name|revision> --clean`

__When you have unpublished local component__

There are three additional options that modify how unpublished local component are handled:

* `mico update --clean-deps` - update the current program or library and its dependencies and discard all local unpublished repositories. Use this with caution because your local unpublished repositories cannot be restored unless you have a backup copy.

* `mico update --clean-files` - update the current program or library and its dependencies, discard local uncommitted changes and remove any untracked or ignored files. Use this with caution because your local unpublished repositories cannot be restored unless you have a backup copy.

* `mico update --ignore` - update the current program or library and its dependencies and ignore any local unpublished libraries (they won't be deleted or modified, just ignored).

__Combining update options__

You can combine the options above for the following scenarios:

* `mico update --clean --clean-deps --clean-files` - update the current program or library and its dependencies, remove all local unpublished libraries, discard local uncommitted changes and remove all untracked or ignored files. This wipes every single change that you made in the source tree and restores the stock layout.

* `mico update --clean --ignore` - update the current program or library and its dependencies, but ignore any local repositories. MiCO Cube will update whatever it can from the public repositories.

Use these with caution because your uncommitted changes and unpublished libraries cannot be restored.