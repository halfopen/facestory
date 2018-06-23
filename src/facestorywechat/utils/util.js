let config = require("../config.js");
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

var sendLog = function(opContent, opType){
    wx.getStorage({
        key: 'openid',
        success: function(res) {
            var openid = res.data;
            wx.request({
                url: config.LOG_API,
                method:"POST",
                data:{
                    "openid":openid,
                    "op_content":opContent,
                    "op_type":opType,
                }, 
                header:{
                    "Content-Type":"application/json"
                }
            })
        },
    })
}

var logger = {
    error: function(opContent){
        sendLog(opContent, config.ERROR_CODE);
    },
    log:function(opContent){
        sendLog(opContent, config.LOG_CODE);
    },
    info:function(opContent){
        sendLog(opContent, config.INFO_CODE);
    }
}

module.exports = {
  formatTime: formatTime,
  json2Form: json2Form,
  logger: logger,
}
