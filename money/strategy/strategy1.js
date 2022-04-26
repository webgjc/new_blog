// 超10%补仓止盈策略
// 多基金混合策略
// 前段时间高低点买卖策略

let start_money = 10000  // 开始钱数
let sale_hold_days = 30  // 持有多少个交易日可以卖出
let buy_min_money = 1000  // 最小买入限制
let sale_min_money = 1000  // 最小卖出限制

let zhishu_low = 2600  // 指数低值, 低于低值将满仓
let zhishu_high = 3500  // 指数高值，高于高值将空仓
let buy_charge_percent = 0.001  // 买入手续费
let sale_charge_percent = 0.005  // 卖出手续费
let run_start_date = "2020-05-20" // 回跑开始天数
let run_end_date = "2021-05-20" // 回跑结束天数
let today_value = undefined  // 当天指数
let zhishu_code = "000001"  // 上证: 1.000001 成指: 0.399001 创业板: 0.399006

let ready_money = start_money  // 手上剩余钱数
let buy_sale_data = [] // 买卖数据
let hold_money = 0  // 指数持有价值
let hold_fund = []  // 持有指数钱列表


function getParam() {
    return []
}

function setParam(data) {

}

async function reRun() {
    return {
        data: [],
        date: [],
        profit: [],
        total_money: [],
        trace_data: []
    }
}


