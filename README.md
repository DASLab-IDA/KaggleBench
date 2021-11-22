# KaggleBench

#### 介绍
这是一个用于评价可视化推荐效果的公开benchmark。其数据来源是数据分析网站Kaggle上的数据集及其对应的数据可视化结果。我们利用收集的数据集及其对应的来自不同用户的可视化结果，以及不同用户对每个可视化结果的投票，构造了一系列有序的可视化，作为每个数据集的期望结果。Benchmark总共包含18个数据集，每个数据集对应一个有序的可视化结果。同时，我们也将收集的原始的来自不同用户的可视化结果记录并公开vengeji/vizrec_bench: benchmark dataset for visualization recommendation (github.com)。


#### 目录结构
 
对每个数据集，它包含以下部分内容：

1.原始数据文件，airplane_crashes_drop_unused_cols.csv，但由于文件大小限制，我们将其保存到了别处https://stuscueducn-my.sharepoint.com/:f:/g/personal/vengeji_stu_scu_edu_cn/ErvLbAEpd7BOl99haBYrsXMBLMgBKxEQ_6wIJt-M8ZdKFw?e=Kejp6x。

2.  从Kaggle上收集的数据分析记录，位于目录/notebooks下

3.  收集的数据分析记录中提取的可视化结果，位于目录/raw_json下

4.  合并后的有序的可视化结果，保存于airplane_crashes.json中

5.  数据表的列名以及对应的列类型（对应于pandas的数据类型）
![目录结构](https://images.gitee.com/uploads/images/2021/0617/211722_0fd772d2_9100839.png "fig1.png")


#### benchmark_manager 
benchmark_manager中包含对benchmark的处理代码。主要有对数据文件的清洗，可视化的过滤与合并，以及一系列评估指标。manage.py可直接执行并查看在benchmark上的评估结果。


#### 执行方式

1.  进入benchmark_manager目录，执行命令python manage.py

2.  待所有benchmark中18个数据集处理完成后即可看到结果(处理需要依赖VizGrank的代码)

![输入图片说明](https://images.gitee.com/uploads/images/2021/0617/213437_a669e5ce_9100839.png "fig4.png")
