// pages/my/my.js
let config = require("../../config.js");
let utils = require("../../utils/util.js");
const app = getApp();

/**
 * 更新我的拍照记录
 */
var update_storys = function(_this, is_first){
    wx.request({
        url: config.GET_MY_STORYS_API + "?openid=" + app.globalData.openid,
        success: function (res) {
            console.log(res);
            if(res.statusCode==200){
            _this.setData({
                my_storys: res.data.reverse()
            });
            if(!is_first){
                wx.showToast({
                    title: '更新成功',
                });
                wx.stopPullDownRefresh();
            }
            }
        }
    });
}

Page({

  /**
   * 页面的初始数据
   */
  data: {
      my_storys:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("onload");
    var _this = this;
    update_storys(_this, true);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    console.log("onready")
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    console.log('onshow')
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    console.log("onhide")
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    console.log("onunload")
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    update_storys(this, false);
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }, 
  

  clickStory: function (e) {
      let id = e.target.dataset.id;
      console.log(e, e.target.dataset.storyId);
      let story = this.data.my_storys[id];
      console.log(this.data.my_storys);
      wx.navigateTo({
          url: '/pages/selfie_result/selfie_result?story=' + encodeURIComponent(JSON.stringify(story)),
      })
      console.log(this.data.my_storys[id])
  }
})