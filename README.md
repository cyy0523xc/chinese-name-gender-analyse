# 中文姓名与性别的相关性分析

原始数据：`./data/`

基本字段：

- 姓名：`name`
- 性别：`gender`
- 省份：`province`
- 民族：`nation`

省份和民族字段不一定都有。可以扩展用于研究不同省份和民族的名字特征。


数据格式化

```sh
grep ",女" data/chinese_name_gender_0*.csv|cut -d, -f1|cut -d: -f2|sort|uniq > data/female.txt

grep ",男" data/chinese_name_gender_0*.csv|cut -d, -f1|cut -d: -f2|sort|uniq > data/male.txt
```

## 测试

```sh
python test.py
```
