## Introduction

*MiCO CLI* is the name of the MXCHIP MiCO command-line tool, packaged as mico-cli, which enables the full mico workflow: repositories version control, maintaining dependencies, publishing code, updating from remotely hosted repositories and invoking MXCHIP MiCO's own build system and export functions, among other operations.

This document covers the installation and usage of mico CLI.

## Table of Contents

1. [Using mico CLI](#using-mico-cli)
1. [Installing and uninstalling](#installing-mico-cli)
1. [Understanding working context and program root](#before-you-begin-understanding-the-working-context-and-program-root)
1. [Creating and importing programs](#creating-and-importing-programs)
    1. [Creating a new program](#creating-a-new-program-for-mico-os-5)
    2. [Importing an existing program](#importing-an-existing-program)
1. [Adding and removing libraries](#adding-and-removing-libraries)
1. [Compiling code](#compiling-code)
    1. [Toolchain selection](#toolchain-selection)
    2. [Compiling your program](#compiling-your-program)
    3. [Compiling static libraries](#compiling-static-libraries)
    4. [Compile configuration system](#compile-configuration-system)
    5. [Compile-time customizations](#compile-time-customizations)
1. [Exporting to desktop IDEs](#exporting-to-desktop-ides)
1. [Testing](#testing)
    1. [Finding available tests](#finding-available-tests)
    2. [Compiling and running tests](#compiling-and-running-tests)
    3. [Limiting the test scope](#limiting-the-test-scope)
    4. [Test directory structure](#test-directory-structure)
1. [Publishing your changes](#publishing-your-changes)
    1. [Checking status](#checking-status)
    2. [Pushing upstream](#pushing-upstream)
1. [Updating programs and libraries](#updating-programs-and-libraries)
    1. [Updating to an upstream version](#updating-to-an-upstream-version)
    2. [Update examples](#update-examples)
1. [mico CLI configuration](#mico-cli-configuration)
1. [Troubleshooting](#troubleshooting)


## Using mico CLI

The basic workflow for mico CLI is to:

1. Initialize a new repository, for either a new application (or library) or an imported one. In both cases, this action also brings in the mico OS codebase.
1. Build the application code.
1. Test your build.
1. Publish your application.

But mico CLI goes much further than the basic workflow. To support long-term development, mico CLI offers nuanced source control, including selective updates of libraries and the codebase, support for multiple toolchains and manual configuration of the system.

<span class="tips">**Tip:** To list all mico CLI commands, use `mico --help`. A detailed command-specific help is available by using `mico <command> --help`.</span>

## Installation

Windows, Linux and Mac OS X support mico CLI. We're keen to learn about your experience with mico CLI on other operating systems at the [mico CLI development page](https://code.aliyun.com/mico/mico-cli).

### Requirements

* **Python** - mico CLI is a Python script, so you'll need Python to use it. We test mico CLI with [version 2.7.11 of Python](https://www.python.org/downloads/release/python-2711/). It is not compatible with Python 3.

* **Git and Mercurial** - mico CLI supports both Git and Mercurial repositories, so you'll need to install both:
    * [Git](https://git-scm.com/) - version 1.9.5 or later.
    * [Mercurial](https://www.mercurial-scm.org/) - version 2.2.2 or later.

    <span class="tips">**Note:** The directories of Git and Mercurial executables (`git` and `hg`) need to be in your system's PATH.</span>

* **Command-line compiler or IDE toolchain** - mico CLI invokes the [mico OS 5](https://code.aliyun.com/mico/mico-os) tools for various features, such as compiling, testing and exporting to industry standard toolchains. To compile your code, you will need either a compiler or an IDE:
    * Compilers: GCC ARM, ARM Compiler 5, IAR.
    * IDE: Keil uVision, DS-5, IAR Workbench.


### Video tutorial for manual installation 

<span class="images">[![Video tutorial](http://img.youtube.com/vi/cM0dFoTuU14/0.jpg)](https://www.youtube.com/watch?v=cM0dFoTuU14)</span>

### Installing mico CLI

You can get the latest stable version of mico CLI through PyPI by running:

```
$ pip install mico-cli
```

On Linux or Mac, you may need to run with `sudo`.

Alternatively, you can get the development version of mico CLI by cloning the development repository [https://code.aliyun.com/mico/mico-cli](https://code.aliyun.com/mico/mico-cli):

```
$ git clone https://github.com/ARMmico/mico-cli
```

Once cloned, you can install mico CLI as a python package:

```
$ python setup.py install
```

On Linux or Mac, you may need to run with `sudo`.

<span class="tips">**Note:** mico CLI is compatible with [Virtual Python Environment (virtualenv)](https://pypi.python.org/pypi/virtualenv). You can read more about isolated Python virtual environments [here](http://docs.python-guide.org/en/latest/).</span>

### Uninstalling mico CLI

To uninstall mico CLI, simply run:

```
pip uninstall mico-cli
```

## Quickstart video

<span class="images">[![Video tutorial](http://img.youtube.com/vi/PI1Kq9RSN_Y/0.jpg)](https://www.youtube.com/watch?v=PI1Kq9RSN_Y)</span>

## Before you begin: understanding the working context and program root

mico CLI uses the current directory as a working context, in a similar way to Git, Mercurial and many other command-line tools. This means that before calling any mico CLI command, you must first change to the directory containing the code you want to act on. For example, if you want to update the mico OS sources in your ``mico-example-program`` directory:

```
$ cd mico-example-program
$ cd mico-os
$ mico update master   # This will update "mico-os", not "my-program"
```

Various mico CLI features require a program root, which whenever possible should be under version control - either [Git](https://git-scm.com/) or [Mercurial](https://www.mercurial-scm.org/). This makes it possible to seamlessly switch between revisions of the whole program and its libraries, control the program history, synchronize the program with remote repositories, share it with others and so on. Version control is also the primary and preferred delivery mechanism for mico OS source code, which allows everyone to contribute to mico OS.

<span class="warnings">**Warning**: mico CLI stores information about libraries and dependencies in reference files that use the `.lib` extension (such as `lib_name.lib`). Although these files are human-readable, we *strongly* advise that you don't edit these manually - let mico CLI manage them instead.</span>


## Creating and importing programs

mico CLI can create and import programs based on both mico OS 2 and mico OS 5.

### Creating a new program for mico OS 5

When you create a new program, mico CLI automatically imports the latest [mico OS release](https://code.aliyun.com/mico/mico-os). Each release includes all the components: code, build tools and IDE exporters. 

With this in mind, let's create a new program (we'll call it `mico-os-program`):

```
$ mico new mico-os-program
[mico] Creating new program "mico-os-program" (git)
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os" at latest revision in the current branch
[mico] Updating reference "mico-os" -> "https://code.aliyun.com/mico/mico-os/#89962277c20729504d1d6c95250fbd36ea5f4a2d"
```

This creates a new folder "mico-os-program", initializes a new repository and imports the latest revision of the mico-os dependency to your program tree.

<span class="tips">**Tip:** You can control which source control management is used, or prevent source control management initialization, by using `--scm [name|none]` option.</span>

Use `mico ls` to list all the libraries imported to your program:

```
$ cd mico-os-program
$ mico ls -a
mico-os-program (mico-os-program)
`- mico-os (https://code.aliyun.com/mico/mico-os/#89962277c207)
```

<span class="notes">**Note**: If you want to start from an existing folder in your workspace, you can simply use `mico new .`, which will initialize an mico program, as well as a new Git or Mercurial repository in that folder. </span>

### Creating a new program for mico OS 2

mico CLI is also compatible with mico OS 2 programs based on the [mico library](https://mico.org/users/mico_official/code/mico/), and it will automatically import the latest [mico library release](https://mico.org/users/mico_official/code/mico/) if you use the `--micolib` option:

```
$ mico new mico-classic-program --micolib
[mico] Creating new program "mico-classic-program" (git)
[mico] Adding library "mico" from "https://mico.org/users/mico_official/code/mico/builds" at latest revision in the current branch
[mico] Downloading mico library build "f9eeca106725" (might take a minute)
[mico] Unpacking mico library build "f9eeca106725" in "D:\Work\examples\mico-classic-program\mico"
[mico] Updating reference "mico" -> "https://mico.org/users/mico_official/code/mico/builds/f9eeca106725"
[mico] Couldn't find build tools in your program. Downloading the mico 2.0 SDK tools...
```
### Creating a new program without OS version selection

You can create plain (empty) programs, without either mico OS 5 or mico OS 2, by using the `--create-only` option.

### Importing an existing program

Use `mico import` to clone an existing program and all its dependencies to your machine:

```
$ mico import https://code.aliyun.com/mico/mico-os-example-blinky
[mico] Importing program "mico-os-example-blinky" from "https://code.aliyun.com/mico/mico-os-example-blinky" at latest revision in the current branch
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os" at rev #dd36dc4228b5
$ cd mico-os-example-blinky
```

mico CLI also supports programs based on mico OS 2, which it automatically detects and which do not require additional options:

```
$ mico import https://mico.org/teams/mico/code/mico_blinky/
[mico] Importing program "mico_blinky" from "https://mico.org/teams/mico/code/mico_blinky" at latest revision in the current branch
[mico] Adding library "mico" from "http://mico.org/users/mico_official/code/mico/builds" at rev #f9eeca106725
[mico] Couldn't find build tools in your program. Downloading the mico 2.0 SDK tools...
$ cd mico-os-example-blinky
```

You can use the "import" command without specifying a full URL; a default prefix (https://code.aliyun.com/mico) is added to the URL. For example, this command:
 
```
$ mico import mico-os-example-blinky
```

is equivalent to this command:
 
```
$ mico import https://code.aliyun.com/mico/mico-os-example-blinky
```

### Importing from a Git or GitHub clone

If you have manually cloned a Git repository into your workspace and you want to add all missing libraries, then you can use the `deploy` command:

```
$ mico deploy
[mico] Adding library "mico-os" from "https://code.aliyun.com/mico/mico-os" at rev #dd36dc4228b5
```

Don't forget to set the current directory as the root of your program:

```
$ mico new .
```

## Adding and removing libraries

While working on your code, you may need to add another library (dependency) to your application, or remove existing libraries. 

The mico CLI add and remove features aren't simply built-in versions of ``hg``, ``git`` and ``rm``; their functionality is tailored to the way mico OS and mico CLI work:

* Adding a new library to your program is not the same as just cloning the repository. Don't clone a library using `hg` or `git`; use `mico add` to add the library. This ensures that all dependencies - libraries or sublibraries - are populated as well.
* Removing a library from your program is not the same as deleting the library directory - there are library reference files that will need updating or cleaning. Use `mico remove` to remove the library; don't simply remove its directory with `rm`.

### Adding a library

Use `mico add` to add the latest revision of a library:

```
$ mico add https://developer.mico.org/users/wim/code/TextLCD/
```

Use the URL#hash format to add a library at a specific revision:

```
$ mico add https://developer.mico.org/users/wim/code/TextLCD/#e5a0dcb43ecc
```

___Specifying a destination directory___

If you want to specify a directory to which to add your library, you can give an additional argument to ``add``, which names that directory. For example, If you'd rather add the previous library in a directory called "text-lcd" (instead of TextLCD):

```
$ mico add https://developer.mico.org/users/wim/code/TextLCD/ text-lcd
```

Although mico CLI supports this functionality, we don't encourage it - adding a library with a name that differs from its source repository can easily lead to confusion.

### Removing a library

If at any point you decide that you don't need a library any more, you can use `mico remove` with the path of the library:

```
$ mico remove text-lcd
```

## Compiling code

### Toolchain selection

After importing a program or creating a new one, you need to tell mico CLI where to find the toolchains that you want to use for compiling your source tree.

There are two ways to do this:
* Through the mico CLI configuration.
* Via mico_settings.py file in the root of your program, which is automatically created (if it doesn't already exist). 

#### Through mico CLI configuration

You can set the ARM Compiler  5 location via the command:

```
$ mico config --global ARM_PATH "C:\Program Files\ARM"
[mico] C:\Program Files\ARM now set as global ARM_PATH
```

The `-G` switch tells mico CLI to set this as a global setting, rather than local for the current program.

Supported settings for toolchain paths are `ARM_PATH`, `GCC_ARM_PATH` and `IAR_PATH`.

You can see the active mico CLI configuration via:

```
$ mico config --list
[mico] Global config:
ARM_PATH=C:\Program Files\ARM\armcc5.06
IAR_PATH=C:\Program Files\IAR Workbench 7.0\arm

[mico] Local config (D:\temp\mico-os-program):
No local configuration is set
```

More information about mico CLI configuration is available in the [configuration section](#mico-cli-configuration) of this document.

#### Through mico_settings.py

Edit `mico_settings.py` to set your toolchain:

* If you want to use the [ARM Compiler toolchain](https://developer.arm.com/products/software-development-tools/compilers/arm-compiler-5/downloads), set `ARM_PATH` to the *base* directory of your ARM Compiler installation (example: C:\Program Files\ARM\armcc5.06). The recommended version of the ARM Compiler toolchain is 5.06.
* If you want to use the [GCC ARM Emicoded toolchain](https://launchpad.net/gcc-arm-emicoded), set `GCC_ARM_PATH` to the *binary* directory of your GCC ARM installation (example: C:\Program Files\GNU Tools ARM Emicoded\4.9 2015q2\bin). Use versions 4.9 of GCC ARM Emicoded; version 5.0 or any version above may be incompatible with the tools.

As a rule, because `mico_settings.py` contains local settings (possibly relevant only to a single OS on a single machine), it should not be versioned. 

### Compiling your program

Use the `mico compile` command to compile your code:

```
$ mico compile -t ARM -m K64F
Building project mico-os-program (K64F, GCC_ARM)
Compile: aesni.c
Compile: blowfish.c
Compile: main.cpp
... [SNIP] ...
Compile: configuration_store.c
Link: mico-os-program
Elf2Bin: mico-os-program
+----------------------------+-------+-------+------+
| Module                     | .text | .data | .bss |
+----------------------------+-------+-------+------+
| Fill                       |   170 |     0 | 2294 |
| Misc                       | 36282 |  2220 | 2152 |
| core/hal                   | 15396 |    16 |  568 |
| core/rtos                  |  6751 |    24 | 2662 |
| features/FEATURE_IPV4      |    96 |     0 |   48 |
| frameworks/greentea-client |   912 |    28 |   44 |
| frameworks/utest           |  3079 |     0 |  732 |
| Subtotals                  | 62686 |  2288 | 8500 |
+----------------------------+-------+-------+------+
Allocated Heap: 65540 bytes
Allocated Stack: 32768 bytes
Total Static RAM memory (data + bss): 10788 bytes
Total RAM memory (data + bss + heap + stack): 109096 bytes
Total Flash memory (text + data + misc): 66014 bytes
Image: BUILD/K64F/GCC_ARM/mico-os-program.bin
```

The arguments for *compile* are:

* `-m <MCU>` to select a target. If `detect` or `auto` parameter is passed, then mico CLI will attempt to detect the connected target and compile against it.
* `-t <TOOLCHAIN>` to select a toolchain (of those defined in `mico_settings.py`, see above). The value can be `ARM` (ARM Compiler 5), `GCC_ARM` (GNU ARM Emicoded), or `IAR` (IAR Emicoded Workbench for ARM).
* `--source <SOURCE>` to select the source directory. The default is `.` (the current directory). You can specify multiple source locations, even outside the program tree.
* `--build <BUILD>` to select the build directory. Default: `BUILD/` inside your program.
* `--profile <PATH_TO_BUILD_PROFILE>` to select a path to a build profile configuration file. Example: mico-os/tools/profiles/debug.json.
* `--library` to compile the code as a [static .a/.ar library](#compiling-static-libraries).
* `--config` to inspect the runtime compile configuration (see below).
* `-S` or `--supported` shows a matrix of the supported targets and toolchains.
* `-c ` (optional) to build from scratch; a clean build or rebuild.
* `-j <jobs>` (optional) to control the compile threads on your machine. The default value is 0, which infers the number of threads from the number of cores on your machine. You can use `-j 1` to trigger a sequential compile of source code.
* `-v` or `--verbose` for verbose diagnostic output.
* `-vv` or `--very_verbose` for very verbose diagnostic output.

The compiled binary, ELF image, memory usage and link statistics can be found in the `build` subdirectory of your program.

For more information on build profiles see https://code.aliyun.com/mico/mico-os/blob/master/docs/Toolchain_Profiles.md .

### Compiling static libraries

You can build a static library of your code by adding the `--library` argument to `mico compile`. Static libraries are useful when you want to build multiple applications from the same mico-os codebase without having to recompile for every application. To achieve this:

1. Build a static library for mico-os.
2. Compile multiple applications or tests against the static library:

```
$ mico compile -t ARM -m K64F --library --no-archive --source=mico-os --build=../mico-os-build
Building library mico-os (K64F, ARM)
[...]
Completed in: (47.4)s

$ mico compile -t ARM -m K64F --source=mico-os/TESTS/integration/basic --source=../mico-os-build --build=../basic-out
Building project basic (K64F, ARM)
Compile: main.cpp
Link: basic
Elf2Bin: basic
Image: ../basic-out/basic.bin

$ mico compile -t ARM -m K64F --source=mico-os/TESTS/integration/threaded_blinky --source=../mico-os-build --build=..\/hreaded_blinky-out
Building project threaded_blinky (K64F, ARM)
Compile: main.cpp
Link: threaded_blinky
Elf2Bin: threaded_blinky
Image: ../threaded_blinky-out/threaded_blinky.bin
```

### Compile configuration system

The [compile configuration system](https://docs.mico.com/docs/mico-os-handbook/en/5.3/advanced/config_system/) provides a flexible mechanism for configuring the mico program, its libraries and the build target. Refer to the previous link for more details about the configuration system.

___Inspecting the configuration___

If the program uses the [compile configuration system](https://docs.mico.com/docs/mico-os-handbook/en/latest/advanced/config_system/), you can use `mico compile --config` to view the configuration:

```
$ mico compile --config -t GCC_ARM -m K64F
```

To display more verbose information about the configuration parameters, use `-v`:

```
$ mico compile --config -t GCC_ARM -m K64F -v
```

It's possible to filter the output of `mico compile --config` by specifying one or more prefixes for the configuration parameters that will be displayed. For example, to display only the configuration defined by the targets:

```
$ mico compile --config -t GCC_ARM -m K64F --prefix target
```

`--prefix` can be used more than once. To display only the configuration defined by the application and the targets, use two `--prefix` options:


```
$ mico compile --config -t GCC_ARM -m K64F --prefix target --prefix app
```

### Compile-time customizations

___Macros___

You can specify macros in your command-line using the -D option. For example:

```
$ mico compile -t GCC_ARM -m K64F -c -DUVISOR_PRESENT
```

___Compiling in debug mode___

To compile in debug mode (as opposed to the default *release* mode), use `--profile mico-os/tools/profiles/debug.json` in the compile command-line:

```
$ mico compile -t GCC_ARM -m K64F --profile mico-os/tools/profiles/debug.json
```

<span class="tips">**Tip:** If you have files that you want to compile only in release mode, put them in a directory called `TARGET_RELEASE` at any level of your tree. If you have files that you want to compile only in debug mode, put them in a directory called `TARGET_DEBUG` at any level of your tree (then use `--profile` as explained above).
</span>

### Automating toolchain and target selection

Using `mico target <target>` and `mico toolchain <toolchain>`, you can set the default target and toolchain for your program, meaning you won't have to specify these every time you compile or generate IDE project files.

You can also use ``mico target detect``, which will attempt to detect the connected target board and use it as parameter every time you compile or export.


## Exporting to desktop IDEs

If you need to debug your code, a good way to do that is to export your source tree to an IDE project file, so you can use the IDE's debugging facilities. Currently mico CLI supports exporting to Keil uVision, DS-5, IAR Workbench, Simplicity Studio and other IDEs.

For example, to export to uVision, run:

```
$ mico export -i uvision -m K64F
```

A `.uvproj` file is created in the projectfiles/uvision folder. You can open the project file with uVision.

## Testing

Use the `mico test` command to compile and run tests:

```
$ mico test -m K64F -t GCC_ARM
Building library mico-build (K64F, GCC_ARM)
Building project GCC_ARM to TESTS-unit-myclass (K64F, GCC_ARM)
Compile: main.cpp
Link: TESTS-unit-myclass
Elf2Bin: TESTS-unit-myclass
+-----------+-------+-------+------+
| Module    | .text | .data | .bss |
+-----------+-------+-------+------+
| Fill      |   74  |   0   | 2092 |
| Misc      | 47039 |  204  | 4272 |
| Subtotals | 47113 |  204  | 6364 |
+-----------+-------+-------+------+
Allocated Heap: 65540 bytes
Allocated Stack: 32768 bytes
Total Static RAM memory (data + bss): 6568 bytes
Total RAM memory (data + bss + heap + stack): 104876 bytes
Total Flash memory (text + data + misc): 48357 bytes
Image: build\tests\K64F\GCC_ARM\TESTS\micomicro-rtos-mico\mutex\TESTS-unit-myclass.bin
...[SNIP]...
micogt: test suite report:
+--------------+---------------+---------------------------------+--------+--------------------+-------------+
| target       | platform_name | test suite                      | result | elapsed_time (sec) | copy_method |
+--------------+---------------+---------------------------------+--------+--------------------+-------------+
| K64F-GCC_ARM | K64F          | TESTS-unit-myclass              | OK     | 21.09              |    shell    |
+--------------+---------------+---------------------------------+--------+--------------------+-------------+
micogt: test suite results: 1 OK
micogt: test case report:
+--------------+---------------+------------------------------------------+--------+--------+--------+--------------------+
| target       | platform_name | test suite         | test case           | passed | failed | result | elapsed_time (sec) |
+--------------+---------------+--------------------+---------------------+--------+--------+--------+--------------------+
| K64F-GCC_ARM | K64F          | TESTS-unit-myclass | TESTS-unit-myclass1 | 1      | 0      | OK     | 5.00               |
| K64F-GCC_ARM | K64F          | TESTS-unit-myclass | TESTS-unit-myclass2 | 1      | 0      | OK     | 5.00               |
| K64F-GCC_ARM | K64F          | TESTS-unit-myclass | TESTS-unit-myclass3 | 1      | 0      | OK     | 5.00               |
+--------------+---------------+--------------------+---------------------+--------+--------+--------+--------------------+
micogt: test case results: 3 OK
micogt: completed in 21.28 sec
```

The arguments to `test` are:
* `-m <MCU>` to select a target for the compilation. If `detect` or `auto` parameter is passed, then mico CLI will attempt to detect the connected target and compile against it.
* `-t <TOOLCHAIN>` to select a toolchain (of those defined in `mico_settings.py`, see above), where `toolchain` can be either `ARM` (ARM Compiler 5), `GCC_ARM` (GNU ARM Emicoded), or `IAR` (IAR Emicoded Workbench for ARM).
* `--compile-list` to list all the tests that can be built.
* `--run-list` to list all the tests that can be run (they must be built first).
* `--compile` to only compile the tests.
* `--run` to only run the tests.
* `-n <TESTS_BY_NAME>` to limit the tests built or run to a comma separated list (ex. test1,test2,test3).
* `--source <SOURCE>` to select the source directory. Default is `.` (the current directory). You can specify multiple source locations, even outside the program tree.
* `--build <BUILD>` to select the build directory. Default: `BUILD/` inside your program.
* `--profile <PATH_TO_BUILD_PROFILE>` to select a path to a build profile configuration file. Example: mico-os/tools/profiles/debug.json.
* `-c or --clean` to clean the build directory before compiling.
* `--test-spec <TEST_SPEC>` to set the path for the test spec file used when building and running tests (the default path is the build directory).
* `-v` or `--verbose` for verbose diagnostic output.
* `-vv` or `--very_verbose` for very verbose diagnostic output.

You can find the compiled binaries and test artifacts in the `BUILD/tests/<TARGET>/<TOOLCHAIN>` directory of your program.

#### Finding available tests

You can find the tests that are available for **building** by using the `--compile-list` option:

```
$ mico test --compile-list
Test Case:
    Name: TESTS-functional-test1
    Path: .\TESTS\functional\test1
Test Case:
    Name: TESTS-functional-test2
    Path: .\TESTS\functional\test2
Test Case:
    Name: TESTS-functional-test3
    Path: .\TESTS\functional\test3
```

You can find the tests that are available for **running** by using the `--run-list` option:

```
$ mico test --run-list
micogt: test specification file '.\build\tests\K64F\ARM\test_spec.json' (specified with --test-spec option)
micogt: using '.\build\tests\K64F\ARM\test_spec.json' from current directory!
micogt: available tests for built 'K64F-ARM', location '.\build\tests\K64F\ARM'
        test 'TESTS-functional-test1'
        test 'TESTS-functional-test2'
        test 'TESTS-functional-test3'
```

#### Compiling and running tests

You can specify to only **build** the tests by using the `--compile` option:

```
$ mico test -m K64F -t GCC_ARM --compile
```

You can specify to only **run** the tests by using the `--run` option:

```
$ mico test -m K64F -t GCC_ARM --run
```

If you don't specify any of these, `mico test` will first compile all available tests and then run them.

#### Limiting the test scope

You can limit the scope of the tests built and run by using the `-n` option. This takes a comma separated list of test names as an argument:

```
$ mico test -m K64F -t GCC_ARM -n TESTS-functional-test1,TESTS-functional-test2
```

You can use the wildcard character `*` to run a group of tests that share a common prefix without specifying each test individually. For instance, if you only want to run the three tests `TESTS-functional-test1`, `TESTS-functional-test2` and `TESTS-functional-test3`, but you have other tests in your project, you can run:

```
$ mico test -m NUCLEO_F429ZI -t GCC_ARM -n TESTS-functional*
```

**Note:** Some shells will try to expand the wildcard character `*` into file names that exist in your working directory. To prevent this behavior, please see your shell's documentation.


### Test directory structure

Test code exists in the following directory structure:

```
mico-os-program
 |- main.cpp            # Optional main.cpp with main() if it is an application module.
 |- pqr.lib             # Required libs
 |- xyz.lib
 |- mico-os
 |  |- frameworks        # Test dependencies
 |  |  `_greentea-client # Greentea client required by tests.
 |  |...
 |  `- TESTS              # Tests directory. Special name upper case TESTS is excluded during application build process
 |     |- TestGroup1      # Test Group directory
 |     |  `- TestCase1    # Test case source directory
 |     |      `- main.cpp # Test source
 |     |- TestGroup2
 |     |   `- TestCase2
 |     |      `- main.cpp
 |     `- host_tests      # Python host tests script directory
 |        |- host_test1.py
 |        `- host_test2.py
 `- build                 # Build directory
     |- <TARGET>          # Target directory
     | `- <TOOLCHAIN>     # Toolchain directory
     |   |- TestCase1.bin # Test binary
     |   `- TestCase2.bin
     | ....
```

As shown above, tests exist inside ```TESTS\testgroup\testcase\``` directories. Please note that `TESTS` is a special upper case directory that is excluded from module sources while compiling.

<span class="notes">**Note:** This feature does not work in applications that contain a  ```main``` function that is outside of a `TESTS` directory.</span>

## Publishing your changes

### Checking status

As you develop your program, you'll edit parts of it - either your own code or code in some of the libraries that it depends on. You can get the status of all the repositories in your program (recursively) by running `mico status`. If a repository has uncommitted changes, this command will display these changes. 

Here's an example:

```
[mico] Status for "mico-os-program":
 M main.cpp
 M mico-os.lib
?? gdb_log.txt
?? test_spec.json

[mico] Status for "mico-os":
 M tools/toolchains/arm.py
 M tools/toolchains/gcc.py

[mico] Status for "mico-client-classic":
 M source/m2mtimerpimpl.cpp

[mico] Status for "mico-mesh-api":
 M source/include/static_config.h
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

Let's assume that you make changes to `iot-client`. `publish` detects the change on the leaf `iot-client` dependency and asks you to commit it. Then it detects that `my-libs` depends on `iot-client`, updates the `my-libs` dependency on `iot-client` to its latest version (by updating the `iot-client.lib` file) and asks you to commit it. This propagates up to `my-libs` and finally to your program `my-mico-os-example`.

## Publishing a local program or library

When you create a new (local) source-control managed program or library, its revision history exists only locally; the repository is not associated with the remote one. To publish the local repository without losing its revision history, please follow these steps:

1. Create a new empty repository on the remote site. This can be based on a public repository hosting service (GitHub, Bitbucket, mico.org), your own service or even a different location on your system.
2. Copy the URL/location of the new repository in your clipboard and open command-line in the local repository directory (for example change directory to `mico-os-example/local-lib`).
3. To associate the local repository:
 * For Git - run `git remote add origin <url-or-paht-to-your-remote-repo>`.
 * For Mercurial - edit .hg/hgrc and add (or replace if exists):
 
            ```
            [paths]
            default = <url-or-paht-to-your-remote-repo>
            ```
4. Run `mico publish` to publish your changes.

In a scenario with nested local repositories, start with the leaf repositories first.

### Forking workflow

Git enables asymmetric workflow where the publish/push repository may be different than the original ("origin") one. This allows new revisions to land in a fork repository while maintaining an association with the original repository.

To achieve this, first import an mico OS program or mico OS itself and then associate the push remote with your fork. For example:

```
$ git remote set-url --push origin https://github.com/screamerbg/repo-fork
```

Each time you `git` commit and push, or use `mico publish`, the new revisions will be pushed against your fork. You can fetch from the original repository using `mico update` or `git pull`. If you explicitly want to fetch or pull from your fork, then you can use `git pull https://github.com/screamerbg/repo-fork [branch]`.

Through the workflow explained above, mico CLI will maintain association to the original repository (which you may want to send a pull request to) and will record references with the revision hashes that you push to your fork. Until your pull request (PR) is accepted, all recorded references will be invalid. Once the PR is accepted, all revision hashes from your fork will become part the original repository, so all references will become valid.

## Updating programs and libraries

You can update programs and libraries on your local machine so that they pull in changes from the remote sources (GitHub or Mercurial). 

There are two main scenarios when updating:

* Update to a *moving* revision, such as the tip of a branch.
* Update to a *specific* revision that is identified by a revision hash or tag name.

Each scenario has two cases:

* Update with local uncommitted changes - *dirty* update.
* Update without local uncommitted changes - *clean* update.

As with any mico CLI command, `mico update` uses the current directory as a working context, meaning that before calling `mico update`, you should change your working directory to the one you want to update. For example, if you're updating mico-os, use `cd mico-os` before you begin updating.

<span class="tips">**Tip: Synchronizing library references:** Before triggering an update, you may want to synchronize any changes that you've made to the program structure by running ``mico sync``, which will update the necessary library references and get rid of the invalid ones.</span>

### Protection against overwriting local changes

The update command will fail if there are changes in your program or library that `update` could overwrite. This is by design: mico CLI does not run operations that would result in overwriting local changes that are not yet committed. If you get an error, take care of your local changes (commit or use one of the options below), then rerun `update`.

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

To help understand what options you can use with mico CLI, check the examples below.

**Case 1: I want to update a program or a library to the latest version in a specific or current branch**

__I want to preserve my uncommitted changes__ 

Run `mico update [branch]`. You might have to commit or stash your changes if the source control tool (Git or Mercurial) throws an error that the update will overwrite local changes.

__I want a clean update (and discard uncommitted changes)__

Run `mico update [branch] --clean`

Specifying a branch to `mico update` will only check out that branch and won't automatically merge or fast-forward to the remote/upstream branch. You can run `mico update` to merge (fast-forward) your local branch with the latest remote branch. On Git you can do `git pull`.

<span class="warnings">**Warning**: The `--clean` option tells mico CLI to update that program or library and its dependencies and discard all local changes. This action cannot be undone; use with caution.</span>

**Case 2: I want to update a program or a library to a specific revision or a tag**
 
__I want to preserve my uncommitted changes__ 

Run `mico update <tag_name|revision>`. You might have to commit or stash your changes if they conflict with the latest revision.

__I want a clean update (discard changes)__

Run `mico update <tag_name|revision> --clean`

__When you have unpublished local libraries__

There are three additional options that modify how unpublished local libraries are handled:

* `mico update --clean-deps` - update the current program or library and its dependencies and discard all local unpublished repositories. Use this with caution because your local unpublished repositories cannot be restored unless you have a backup copy.

* `mico update --clean-files` - update the current program or library and its dependencies, discard local uncommitted changes and remove any untracked or ignored files. Use this with caution because your local unpublished repositories cannot be restored unless you have a backup copy.

* `mico update --ignore` - update the current program or library and its dependencies and ignore any local unpublished libraries (they won't be deleted or modified, just ignored).

__Combining update options__

You can combine the options above for the following scenarios:

* `mico update --clean --clean-deps --clean-files` - update the current program or library and its dependencies, remove all local unpublished libraries, discard local uncommitted changes and remove all untracked or ignored files. This wipes every single change that you made in the source tree and restores the stock layout.

* `mico update --clean --ignore` - update the current program or library and its dependencies, but ignore any local repositories. mico CLI will update whatever it can from the public repositories.

Use these with caution because your uncommitted changes and unpublished libraries cannot be restored.

## mico CLI configuration

You can streamline many options in mico CLI with global and local configuration.

The mico CLI configuration syntax is:
```
mico config [--global] <var> [value] [--unset]
```

* The **global** configuration (via `--global` option) defines the default behavior of mico CLI across programs unless overridden by *local* settings.
* The **local** configuration (without `--global`) is per mico program and allows overriding of global or default mico CLI settings within the scope of a program or library and its dependencies.
* If **no value** is specified then mico CLI will print the currently set value for this settings from either the local or global scope.
* The `--unset` option allows removing of a setting.
* The `--list` option allows you to list global and local configuration.

Here is a list of currently implemented configuration settings:

 * `target` - defines the default target for `compile`, `test` and `export`; an alias of `mico target`. Default: none.
 * `toolchain` - defines the default toolchain for `compile` and `test`; can be set through `mico toolchain`. Default: none.
 * `ARM_PATH`, `GCC_ARM_PATH`, `IAR_PATH` - defines the default path to ARM Compiler, GCC ARM and IAR Workbench toolchains. Default: none.
 * `protocol` - defines the default protocol used for importing or cloning of programs and libraries. The possible values are `https`, `http` and `ssh`. Use `ssh` if you have generated and registered SSH keys (Public Key Authentication) with a service such as GitHub, GitLab, Bitbucket, etc. Read more about SSH keys [here](https://help.github.com/articles/generating-an-ssh-key/). Default: `https`.
 * `depth` - defines the *clone* depth for importing or cloning and applies only to *Git* repositories. Note that though this option may improve cloning speed, it may also prevent you from correctly checking out a dependency tree when the reference revision hash is older than the clone depth. Read more about shallow clones [here](https://git-scm.com/docs/git-clone). Default: none.
 * `cache` - defines the local path that will be used to store minimalistic copies of the imported or cloned repositories, and attempts to use it to minimize traffic and speed up future imports of the same repositories. Use `on` or `enabled` to turn on caching in the system temp path. Default: none (disabled).
 
## Troubleshooting

#### Unable to import Mercurial based (mico.org) programs or libraries.
1. Check whether you have Mercurial installed in your system path by  running `hg` in command prompt. If you're receiving "command not found" or similar message, then you need to install Mercurial and add it to your system path.

2. Try to clone a Mercurial repository directly, e.g. `hg clone https://developer.mico.org/teams/mico/code/mico_blinky/`. If you're receiving error similar to `abort: error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.:590)`, then your system certificates are very old. You need to update your system certificates and possibly add the host certificate fingerprint of `mico.com` and `mico.org`. Read more about Mercurial's certificate management [here](https://www.mercurial-scm.org/wiki/CACertificates).

#### Various issues when running mico CLI in Cygwin environment
Currently mico CLI is not compatible with Cygwin environment and cannot be executed inside it (https://code.aliyun.com/mico/mico-cli/issues/299).
