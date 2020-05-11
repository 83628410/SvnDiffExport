# 导出版本差异文件

MacOs 中的svn 软件没有一个好用的，导出版本差异文件都没有目录结构，只能自己写一个了.
简单介绍一下自己的思路，先用diff命令获得版本差异文件列表，再循环这个文件列表逐个导出文件。

```shell script
svn svn地址 log  -v -r svn版本号 --xml
```

## 使用方法

```shell script
python3 main.py svn地址 svn版本号,可以用 :
```