[TOC]



##### django-models .py

###### 字段类型

1. AutoField：映射到数据库为int类型，具有自增的特性，需要设置primary_kwy=True;
2. TextField：文本类型
3. DateTimeField：时间类型
4. CharField：字符串类型



1. primary_key：主键；
2. autoincrement：自动自增；
3. null：是否允许为空；
4. db_index：建立索引；
5. default：设置默认值；
6. auto_now_add：无论是你添加还是修改对象，时间为你添加或者修改的时间；
7. auto_row：无论是你添加还是修改对象，时间为你添加或者修改的时间；
8. max_length：限制字段的最大长度；