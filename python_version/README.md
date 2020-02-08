# Python 版本抢课说明

> Update on 2020-2-8
> Python版本修改自GitHub用户[YoungWilliamZ](https://github.com/YoungWilliamZ)的[SUSTC-Qiangke](https://github.com/YoungWilliamZ/SUSTC-Qiangke)项目
> 
> 本脚本需要输入CAS账号密码使用，但未以任何形式上传CAS账号密码 

## 运行环境

* Windows (.exe文件)
* Python3 (.py文件) (暂只验证Python 3.7)

## 运行过程

脚本运行最初要求提供CAS账号密码，输入密码时，不在屏幕上显示输入以防密码泄露。

脚本要求提供待抢课程信息，会优先检测目录下是否有名为`captureClassList.json`的文件，若有，则读取文件内课表信息。`captureClassList.json`不存在时，也可通过命令行输入课程信息，输入完成后，还可选择是否保存课程信息，若保存，则课程信息会保存在目录下名为`captureClassList.json`的文件中。

脚本支持设定抢课间隔时间，以毫秒为单位输入。

脚本运行前先判断时间，如果当日启动时间在`12:55`之前会先待机等待。

脚本运行中，先访问CAS登陆界面和教务系统界面获取必要的登录信息，然后通过直接访问选课系统“选课”按钮链接来达到快速抢课效果。

### 附：如何查看课程 id ？

1. 进入选课系统
2. 右键 `选课` 按钮，检查
3. 右侧或左侧出现 id , 如下

![查找 id](https://i.imgur.com/aPU8Yki.png)
