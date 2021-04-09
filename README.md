# [CCF2020-滴滴-路况状态时空预测](https://www.datafountain.cn/competitions/466)

---

## 赛题介绍

### 背景

移动互联网时代的到来让所有移动设备的持有者都可以成为道路通行能力的描绘者, 滴滴平台收集了海量的高质量司乘轨迹数据, 可以对实时道路拥堵状况有良好的建模能力。 如果可以基于实时和历史的路况信息, 对未来的路况状态有较精准的预估, 无疑对出行决策, 缓解城市拥堵等场景有至关重要的作用。

 然而, 未来的路况预估仍然是十分困难的, 未来路况会受到时间周期, 道路通行能力, 路网上下游拓扑, 导航流量以及道路突然状况等多种因素的影响。此次竞赛诚邀参赛者基于滴滴提供的实时与历史路况状态信息以及道路属性等信息, 精准预估未来某时间段内的路况状态, 助力城市规划与智能出行方案。
 
### 任务（回归预测/多分类）

根据滴滴提供的道路小段的实时和历史路况状态特征, 道路基本属性以及路网拓扑关系图, 预测未来一段时间内道路小段的路况状态(即畅通, 缓行和拥堵几类状态）

---

## 赛题数据

本次比赛提供滴滴平台2019年7月1日至2019年7月30日西安的实时和历史路况信息, 以及西安市的道路属性和路网拓扑信息.

术语解释：
1. link: 对完整道路按照拓扑切分后得到的小段, 由唯一id标识。
2. 路况状态：根据道路的平均车速, 道路等级等信息对道路通行状态的描述, 分为畅通, 缓行, 拥堵三种状态, 分别对应滴滴地图展示的绿色, 黄色, 红色。
3. 时间片：对时间的离散化描述。一般以2分钟为一个单位，2分钟内认为道路的路况状态是统一的。

历史与实时路况文件：
1. link_id：车道ID
2. cur_slice_id：当前时间片
2. pred_slice_id：待预测时间片
3. label：待预测时间片的路况状态
4. speed_with_light_list：近n个时间片的路况速度（n=5）
5. speed_without_light_list：近n个时间片的ETA速度
6. status_list：近n个时间片的路况状态
7. car_count_list：近n个时间片参与路况计算的车辆数
4. his_speed_with_light_list：历史m个星期同期n个时间片的路况速度（m=4, -28 -12 -14 -7)
5. his_speed_without_light_list：历史m个星期同期n个时间片的ETA速度
6. his_status_list：历史m个星期同期n个时间片的路况状态
7. car_count_list：历史m个星期同期n个时间片参与路况计算的车辆数

道路属性文件：
1. link_id：category：车道ID
2. length：numeric：车道长度（米）
3. direction：category：车道通行方向
4. path_class：category：车道的功能等级
5. speed_class：category：车道的限速等级
6. lane_num：categroy：车道数目
7. speed_limit：numeric：车道限速（m/s）
8. level：categroy：车道的等级
9. width：numeric：车道的宽度（米）

路网拓扑文件：

link id -> 下游link id1, 下游link id2, 下游link id3, …

---

## 评测

评测指标: 加权 F1, 畅通权重0.2, 缓行权重0.2, 拥堵权重0.6。

---

## 参考

[Traffic Network GNN papers](https://github.com/thunlp/GNNPapers#traffic-network)

[CCF-2020路况状态时空预测Baseline](https://mp.weixin.qq.com/s/gxWr4CkEPjUwZdKa9Qls6g)

[路况状态时空预测首日基线](http://jiangliclub.com/article?article_id=75)

[2020ccf滴滴时空预测比赛lstm版本baseline](https://mp.weixin.qq.com/s?__biz=MzkxODEzODI2Mg==&mid=2247483746&idx=1&sn=c6f50c39e26019b0b79ac3225009e056&chksm=c1b4bd9bf6c3348dc68bf07c9880e48b071393cd439d42af2189eb2030a6242864c3d3e67c39&mpshare=1&scene=23&srcid=1022rEQo31uhsJkhvuI6nFZl&sharer_sharetime=1603339734792&sharer_shareid=87d503e69458fd3111dde727291f12d6#rd)