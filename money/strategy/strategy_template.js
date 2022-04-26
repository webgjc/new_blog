
/**
 * 获取可配置参数列表
 * @returns [{
        name: "start_money",
        alias: "开始钱数",
        default: 10000,
        type: "number"
    }]
 */
function getParam() {
    return []
}

/**
 * 设置传入的参数
 * @param {*} data 
 */
function setParam(data) {

}

/**
 * 运行回测，返回报告
 * @returns 
 */
async function reRun() {
    return {
        data: [],
        date: [],
        profit: [],
        total_money: [],
        trace_data: []
    }
}


