# 到梦空间自动发现活动并抢活动

## 如何使用?
```
conda create -n dm python=3.8
conda activate dm
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

最后运行
```
python main.py
```


## 可配置项
```
like = ['分享活动']
timeSleep = 0.01
```


当``like``为空列表时则报名所有活动，否则按照关键词报名，``timeSleep``为延时时间



## 参考文献
fuck“盗”梦空间 https://github.com/kismetpro/fuck-daomengkongjian
