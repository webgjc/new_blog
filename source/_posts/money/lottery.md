---
article: false
title: 彩票随机生成器
catalog: true
date: 1996-09-25 19:31:43
subtitle: 随机个五百万
header-img:
---

# 大乐透

<form class="form-inline">
    <div class="form-group">
        <label for="gsize">组数: </label>
        <input type="number" class="form-control" value='5' id='gsize'>
    </div>
    <button type="button" class='btn btn-default' style='line-height: 0.7' id='generate'>生成</button>
</form>
<div id='dlt' style='font-size: 28px'></div>


<script type="text/javascript">
    function getRandom(min, max) {
        return Math.floor(Math.random()*(max-min+1)+min)
    }

    function getRandomList(num, min, max) {
        if(max - min + 1 < num) {
            return []
        }
        let tmp = []
        while(true) {
            if(tmp.length >= num) {
                break
            }
            let n = getRandom(min, max);
            if(tmp.indexOf(n) == -1) {
                tmp.push(n)
            }
            console.log(1)
        }
        tmp.sort((a, b) => a-b)
        return tmp
    }

    function formatNumList(numList, n) {
        return numList.map(i => (Array(n).join(0) + i).slice(-n));
    }

    function writeDaLeTouList(n) {
        let str = "";
        for(let i = 0;i < n;i++) {
            str += formatNumList(getRandomList(5, 1, 35), 2).join(" ") + " + " + formatNumList(getRandomList(2, 1, 12), 2).join(" ") + "<br />"
        }
        document.getElementById("dlt").innerHTML = str
    }

    let gbtn = document.getElementById("generate");
    let gsize = document.getElementById("gsize");
    gbtn.onclick = function(e) {
        e.preventDefault();
        writeDaLeTouList(parseInt(gsize.value));
    }
</script>