let config = require("../config.js")

const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

function json2Form(json) {
    var str = [];
    for (var p in json) {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(json[p]));
    }
    return str.join("&");
} 

// 发出请求保存log
var sendLog = function (opContent, opType = 0) {
    console.log("send log"+opContent+ opType);
    wx.getStorage({
        key: 'openid',
        success: function (res) {
            console.log("get openid", res);
            let openid = res.data;

            wx.request({
                url: config.LOG_API,
                data: {
                    "data": {
                        "type": "logs",
                        "attributes": {
                            "op_content": opContent,
                            "openid": openid,
                            "op_type": opType
                        }
                    }
                },
                header: {
                    "Accept": "application/vnd.api+json",
                    "Content-Type": "application/vnd.api+json"
                },
                method: "POST",
                success: function (res) {
                    console.log(res)
                }
            })
        },
    });
}

// log 方法
var logger = {
    log:function(opContent){
        sendLog(opContent, config.LOG_CODE)
    },
    info: function(opContent){
        sendLog(opContent, config.INFO_CODE);
    },
    error: function(opContent){
        sendLog(opContent, config.ERROR_CODE);
    }
}

module.exports = {
  formatTime: formatTime,
  json2Form: json2Form,
  logger:logger
}
