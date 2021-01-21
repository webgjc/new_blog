
---
title: 宽客初探---策略之旅
catalog: true
date: 2018-1-31 18:46:21
---

既然已经接触了股票类金融，便也尝试一下宽客的滋味，至少python编程还是在的，在聚宽创了个号，了解基本的几个股票概念，便开始实践。<!--more-->

看了很多知乎，雪球大v的文章，了解到<strong>量化</strong>大多也是条充满荆棘的道路，然而这种路走多了好像也习惯了，（绝望多了也享受绝望的感觉了）&lt;-这种feeling很奇妙。不试试咋么知道呢，反正还没到头脑发热的程度，大不了重头再来呗。

家里人谈股色变，但好像我没咋受影响，自己的路自己走，也没有太多包袱。

可能我注定不会是一个专精的程序员，从web前端到后台，再到机器学习神经网络；从js到php，再到python，然后到现在写写量化策略。是种历练吧。

开始说第一个策略把，策略叫聪明钱，注解还是在代码里展示：
<pre># 导入函数库
import jqdata
import numpy as np
import random
import datetime

# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 输出内容到日志 log.info()
    # 过滤掉order系列API产生的比error级别低的log
    log.set_level('order', 'error')
    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    #运行，这里按天回测
    run_daily(trade, "every_bar")

#下面三个是过滤器，过滤停牌，摘牌，st的股票
def paused_filter(security_list):
    current_data=get_current_data()
    security_list=[stock for  stock in security_list if not current_data[stock].paused]
    return security_list
    
def delisted_filter(security_list):
    current_data=get_current_data()
    security_list=[stock for stock in security_list if not '退' in current_data[stock].name]
    return security_list

def st_filter(security_list):
    current_data=get_current_data()
    security_list=[stock for stock in security_list if not current_data[stock].is_st]
    return security_list

#主要交易
def trade(context):
    #选择股票，并用一些财务数据简单过滤，挑中100个
    stock_to_choose=get_fundamentals(query(
        valuation.code,valuation.pe_ratio,
        valuation.pb_ratio,valuation.market_cap,
        indicator.eps,indicator.inc_net_profit_annual
    ).filter(
        valuation.pe_ratio&lt;400,
        valuation.pe_ratio&gt;0,
        indicator.eps&gt;0.1,
        indicator.inc_net_profit_annual&gt;0.2,
        indicator.roe&gt;2
    ).order_by(
        valuation.pb_ratio.asc()
    ).limit(
        100
    ), date=None)
    #过滤股票
    stockpool=list(stock_to_choose['code'])
    stockpool=paused_filter(stockpool)
    stockpool=delisted_filter(stockpool)
    stockpool=st_filter(stockpool)
    #选择在每周周五交易
    if context.current_dt.weekday()==4:
        
        all_q={"stock":[],"q":[]}
        #遍历股票池
        for stock in stockpool:
            #按分钟获取20天的历史数据---收盘价，成交量，成交额
            df=attribute_history(stock,240*20,'1m',['close','volume','money'])
            #计算单笔的平均价格
            vwap_all = df['money'].sum()/df['volume'].sum()
            #计算涨跌幅，定义聪明因子s=涨跌幅除以根号成交量
            data_return=df['close'].pct_change()
            df["smart"]=np.abs(data_return)/np.sqrt(df['volume'])
            #过滤
            df = df[(df['smart']&gt;0) &amp; (df['smart']&lt;np.inf)]
            #按聪明因子s排序
            df=df.sort("smart",ascending=False)
            #计算成交量累积和
            df["accumvol"]=df['volume'].cumsum()
            if len(df["accumvol"].values)==0:
                continue
            #获取总和的前百分之20
            high_acc=df["accumvol"].values[-1]*0.2
            tmp = df[df['accumvol'] &lt;= high_acc]
            
            if tmp['volume'].sum()==0:
                continue
            #截取的单笔的均价
            vwap_smart = tmp['money'].sum()/tmp['volume'].sum()
            #均价相比较
            all_q['stock'].append(stock)
            all_q['q'].append(vwap_smart/vwap_all)
        #获取前百分之2
        tmp_q=pd.DataFrame(all_q)
        q_min=tmp_q["q"].quantile(0)
        q_max=tmp_q["q"].quantile(0.02)
        my_q=tmp_q[tmp_q["q"]&gt;=q_min][tmp_q["q"]&lt;q_max]
        my_stk=my_q['stock'].values
        #获取持仓的股票代码
        slist=list(context.portfolio.positions.keys())
        #不符合的卖出
        for stk in slist:
            if stk not in my_stk:
                order_target_value(stk, 0)
        #符合的买进
        buy_list=[]
        for stock in my_stk:
            if stock not in slist:
                buy_list.append(stock)
        if len(buy_list)==0:
            Cash=context.portfolio.available_cash
        else:
            Cash=context.portfolio.available_cash/len(buy_list)
            for  stock in buy_list:
                order_target_value(stock,Cash)</pre>
回测结果：

<a href="/img/uploads/2018/01/微信图片_20180131184240.png"><img class="alignnone wp-image-528 size-full" src="/img/uploads/2018/01/微信图片_20180131184240.png" alt="" width="1019" height="401" /></a>

这个策略在16年的时候还是可以的，但在17年回测的时候就不太行了。也了解了策略必须要经常更替，一个策略不可能长时间保持高收益。

策略来源：<a href="https://uqer.io/community/share/578f04e0228e5b3b9b5f1ab7">https://uqer.io/community/share/578f04e0228e5b3b9b5f1ab7</a>
