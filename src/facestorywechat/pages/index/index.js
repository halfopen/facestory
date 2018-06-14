//index.js
//获取应用实例
const app = getApp()
let util = require('../../utils/util.js');
let config = require('../../config.js');

/****页面****/
var clickSelfie = function (e) {
    var _this = this;
    util.logger.log("点击自拍按钮");
    wx.chooseImage({
        count: 1,
        success: choose_photo_callback,
        fail: choose_photo_fail_callback,
        sizeType: ['compressed'],
        sourceType: ['camera'],
    })
}
var clickGallery = function (e) {
    util.logger.log("点击从相册选择");
    wx.chooseImage({
        count: 1,
        success: choose_photo_callback,
        fail: choose_photo_fail_callback,
        sizeType: ['compressed'],
        sourceType: ['album'],
    })
}
/*----------------------*/


var choose_photo_callback = function (res) {
    console.log("choose success", res);

    var image_path = res.tempFilePaths[0];
    wx.showLoading({
        title: '加载中',
        mask: true
    })
    wx.getStorage({
        key: 'openid',
        success: function(res) {
            var openid = res.data;
            wx.uploadFile({
                url: config.FACE_DETECT_API + "?openid=" + openid,
                filePath: image_path,
                name: 'photo',
                success: upload_photo_callback,
                fail: upload_photo_fail_callback,
                complete: upload_photo_complete_callback
            })
        },
    })

}

var choose_photo_fail_callback = function (e) {
    console.log("choose fail", e);
}


/*************上传图片回调函数**************/
var upload_photo_callback = function (res) {
    console.log("upload success", res);
    var result = JSON.parse(res.data);
    if(result.code==-1){
        wx.showModal({
            title: '识别图片错误',
            content: result.message,
            showCancel:false
        })
        return;
    }
    if (result.face_size <= 0) {
        wx.showModal({
            title: '请重试',
            content: '未检测到人脸',
            showCancel: false
        });
        return;
    }
    var story = res.data;
    wx.navigateTo({
        url: '/pages/selfie_result/selfie_result?story=' + encodeURIComponent(story),
    })
}

var upload_photo_fail_callback = function (e) {
    console.log("upload fail", e);
    wx.hideLoading();
    wx.showModal({
        title: '请求服务器出错',
        content: e.errMsg,
        showCancel: false
    })
}

var upload_photo_complete_callback = function (e) {
    console.log("upload complete", e);
    // 防止没有关闭
    wx.hideLoading();
}
/*-------------------------------------*/


Page({
    data: {
        canIUse: wx.canIUse('button.open-type.getUserInfo')
    },
    //事件处理函数
    bindViewTap: function () {

    },
    onLoad: function () {
        console.log(app.globalData.userInfo);


    },
    onShow: function(){
        util.logger.log("进入拍照首页");
    },
    onHide: function(){
        util.logger.log("离开拍照首页");
    },

    // 点击自拍按钮
    clickSelfie: clickSelfie,

    // 点击从相册选择
    clickGallery: clickGallery
})