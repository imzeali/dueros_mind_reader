# 小冰读心术智能音箱版

这个项目可将小冰读心术网页版变成百度智能音响语音交互技能，目前如果提交到百度CFC的正式线上环境小冰的接口是被微软封禁了，但自建服务器和模拟测试还是可以的，详细使用说明还需要时间编写，有问题可提issues，看到我会回复

配置完百度CFC就可以在技能管理后台测试了。
#### 配置百度云秘钥
	$ vi config.py 
```
AK = 'xxxxxxxxx'
SK = 'xxxxxxxxxx'
FUNCTION_NAME = 'xxxxxxxx'
```
#### 打包并上传技能
	$ python package.py
## 其他
[获取百度云秘钥](https://cloud.baidu.com/doc/Reference/GetAKSK.html#.E5.A6.82.E4.BD.95.E8.8E.B7.E5.8F.96AK.20.2F.20SK)
[百度CFC配置教程](https://cloud.baidu.com/doc/CFC/BestPractise.html#.E4.BB.8E.E5.A4.B4.E5.88.9B.E5.BB.BA.E5.87.BD.E6.95.B0)
