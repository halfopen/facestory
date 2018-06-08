//app.js
let config = require('./config.js');

var upload_user_info = function(app){
    var user_info_data = app.globalData.userInfo;
    console.log(app);
    user_info_data.openid = app.globalData.openid;
    console.log(user_info_data);
    wx.request({
        url: config.USER_INFO_API,
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data: user_info_data,
        success: function (res) {
            console.log(res);
        }
    })
}

App({
  onLaunch: function () {
    var _this = this;
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        console.log(res);

        //调用request请求api转换登录凭证  
        wx.request({
            url: config.GET_OPENID_API+"?code="+res.code,
            header: {
                'content-type': 'application/json'
            },
            success: function (res) {
                console.log(res) //获取openid  
                _this.globalData.openid = res.data.openid
                console.log("globaldata",_this.globalData)
                // 上传用户信息
                upload_user_info(_this);
            }
        })  
      }
    })

    // 获取用户信息
    wx.getSetting({
      success: res => {
          console.log("get auth setting", res);
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
                console.log("userinfo",res);
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }else{
            // 如果没有授权，跳转到授权页面
            wx.redirectTo({
                url: '/pages/getuserinfo/getuserinfo',
            })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    openid:null
  }
})