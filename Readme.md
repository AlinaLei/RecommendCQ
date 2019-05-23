##
项目框架架构解释如下：
api  层级 里面存放 和前端交互的接口定义以及数据传输规范定义
---- core.py            定义路由
---- evaluatelist.py    定义接口和前端的交互规范

conf  层级
配置文件，存放一些比如数据库等的相关信息   注意涉及到密码等内容的文件，需要在忽略文件中写明
在后续提交到git上的时候需要忽略此类文件，只在本地留存
---- db_conf.py         数据库相关信息
---- main.py            主要的一些文件路径等存放定义

ModelFunction 层级
该层级主要是存放具体的方法实现，用来定义接口需要实现的功能方法
---- evaluate.py         推荐系统评估方法
---- model.py            推荐系统算法实现

public  层级
公用方法一般都放在此目录下，比如数据库调用方法等
---- common.py           公用方法
---- mysql_db.py         数据库公用方法

util 层级
是一个融合的多功能的工具包

.gitignore 文件用来定义哪些文件在git 中Push的时候需要忽略

requirements.txt 用来存放需要的配置包清单

run.py 运行主程序



