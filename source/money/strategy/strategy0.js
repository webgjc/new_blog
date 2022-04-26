// 基于指数估值和持仓曲线的投资策略

/**
 * 用户设置一个对指数的高低位评估，
 * 持仓曲线为按百分比表示持仓，
 * 低位持仓0%，高位持仓100%，中间的比例可按函数设置
 */

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

// 获取数据
function get_data() {
    return fetch(`../funddata/${zhishu_code}.json`)
        .then((res) => res.json())
}


// 确定持仓曲线, 返回闲钱占比
function get_holder_percent(now) {
    let res = (1 / (zhishu_high - zhishu_low)) * (now - zhishu_low)
    return Math.min(Math.max(res, 0), 1)
}


// 买入判断
function buy_point(now) {
    let cangwei = get_holder_percent(now)
    let t = parseInt(ready_money - ((ready_money + hold_money) * cangwei))
    if(t > buy_min_money) {
        return t
    }else{
        return 0
    }
}


// 卖出判断
function sale_point(now) {
    let cangwei = get_holder_percent(now)
    let t = parseInt(ready_money - ((ready_money + hold_money) * cangwei))
    if(t < -sale_min_money) {
        return -t
    }else{
        return 0
    }
}


// 回跑
async function reRun() {
    let result = {}
    let source_data = await get_data()
    let data = []
    let date = []
    for(let i = 0; i < source_data.length; i++) {
        if(source_data[i].x >= run_start_date && source_data[i].x <= run_end_date) {
            data.push(source_data[i].y)
            date.push(source_data[i].x)
        }
    }
    result["data"] = data
    result["date"] = date
    result["total_money"] = [start_money]
    result["profit"] = []

    for(let i = 0; i < data.length; i++) {
        // console.log(`日期: ${date[i]}，指数: ${data[i]}`)
        if(i > 0) {
            tmp = 0
            for(let j = 0; j < hold_fund.length; j++) {
                hold_fund[j]["money"] = data[i] / data[hold_fund[j]["index"]] * hold_fund[j]["benjin"]
                tmp += hold_fund[j]["money"]
            }
            hold_money = tmp
        }

        // 买
        buy = buy_point(data[i])
        if(buy > 0) {
            buy_sale_data.push({
                "type": "buy",
                "money": buy,
                "index": i
            })
            // console.log("买入: " + buy)
            ready_money -= buy
            buy = buy * (1 - buy_charge_percent)
            hold_fund.push({
                "index": i,
                "benjin": buy,
                "money": buy
            })
            hold_money += buy
        }

        // 卖
        sale = sale_point(data[i])
        if(sale > 0) {
            let j = 0
            let k = 0
            let this_sale = 0
            let hold_fund_copy = hold_fund.concat()
            while(k < hold_fund_copy.length) {
                if(i - hold_fund_copy[j]["index"] <= sale_hold_days) {
                    break
                }
                if(hold_fund_copy[j]["money"] > sale) {
                    this_sale += sale
                } else {
                    this_sale += hold_fund_copy[k]["money"]
                    hold_fund_copy.splice(j, 1)
                    k -= 1
                }
                k += 1
            }
            if(this_sale >= sale_min_money) {
                this_sale = 0
                while(j < hold_fund.length) {
                    if(i - hold_fund[j]["index"] <= sale_hold_days) {
                        break
                    }
                    if(i - hold_fund[j]["index"] <= sale_hold_days) {
                        break
                    }
                    if(hold_fund[j]["money"] > sale) {
                        this_sale += sale
                        hold_fund[j]["benjin"] = (hold_fund[j]["money"] - sale) / hold_fund[j]["money"] * hold_fund[j][
                            "benjin"]
                        hold_fund[j]["money"] -= sale
                        hold_money -= sale
                        ready_money += sale * (1 - sale_charge_percent)
                        break
                    } else {
                        this_sale += hold_fund[j]["money"]
                        hold_money -= hold_fund[j]["money"]
                        ready_money += hold_fund[j]["money"] * (1 - sale_charge_percent)
                        sale -= hold_fund[j]["money"]
                        hold_fund.splice(j, 1)
                        j -= 1
                    }
                    j += 1
                }
    
                if(this_sale > 0) {
                    buy_sale_data.push({
                        "type": "sale",
                        "money": parseFloat(this_sale.toFixed(2)),
                        "index": i
                    })
                    // console.log("卖出: " + this_sale)
                }
            }
        }

        console.log(ready_money)
        ready_money = parseFloat(ready_money.toFixed(4))
        hold_money = parseFloat(hold_money.toFixed(4))
        result["total_money"].push(parseFloat((ready_money + hold_money).toFixed(2)))
        result["profit"].push(parseFloat(((ready_money + hold_money - start_money) / start_money * 100).toFixed(2)))
        // console.log(`闲钱：${ready_money}, 持有价值：${hold_money}，总钱：${hold_money + ready_money}`)
    }

    result["trace_data"] = buy_sale_data
    console.log(result)

    if(hold_money + ready_money > start_money) {
        console.log(`本次回跑赚: ${hold_money + ready_money - start_money}, 比例: ${((hold_money + ready_money - start_money) / start_money * 100).toFixed(2)}%`)
    } else {
        console.log(`本次回跑亏: ${start_money - hold_money - ready_money}, 比例: ${((start_money - hold_money - ready_money) / start_money * 100).toFixed(2)}%`)
    }
    if(data[data.length-1] > data[0]) {
        console.log(`指数上涨: ${data[data.length-1] - data[0]}, 比例: ${((data[data.length-1] - data[0]) / data[0] * 100).toFixed(2)}%`)
    } else {
        console.log(`指数下降: ${data[0] - data[data.length-1]}, 比例: ${((data[0] - data[data.length-1]) / data[0] * 100).toFixed(2)}%`)
    }

    return result
}


function getParam() {
    return [
        {
            name: "start_money",
            alias: "开始钱数",
            default: 10000,
            type: "number"
        },
        {
            name: "sale_hold_days",
            alias: "最小持有天数",
            default: 30,
            type: "number"
        },
        {
            name: "buy_min_money",
            alias: "最小买入钱数",
            default: 1000,
            type: "number"
        },
        {
            name: "sale_min_money",
            alias: "最小卖出钱数",
            default: 1000,
            type: "number"
        },
        {
            name: "zhishu_low",
            alias: "指数低估点位",
            default: 2600,
            type: "number"
        },
        {
            name: "zhishu_high",
            alias: "指数高估点位",
            default: 3500,
            type: "number"
        },
        {
            name: "buy_charge_percent",
            alias: "买入手续费",
            default: 0.001,
            type: "number"
        },
        {
            name: "sale_charge_percent",
            alias: "卖出手续费",
            default: 0.005,
            type: "number"
        },
        {
            name: "run_start_date",
            alias: "回跑开始时间",
            default: "2020-05-20",
            type: "date"
        },
        {
            name: "run_end_date",
            alias: "回跑结束时间",
            default: "2021-05-20",
            type: "date"
        },
        {
            name: "zhishu_code",
            alias: "指数代码",
            default: "000001",
            type: "string"
        }   
    ]
}

function setParam(data) {
    getParam().map(item => {
        if(item.type == "number") {
            eval(`${item.name} = ${data[item.name]}`)
        } else {
            eval(`${item.name} = "${data[item.name]}"`)
        }
    })
    buy_sale_data = []
    ready_money = start_money
    hold_money = 0
    hold_fund = []

}