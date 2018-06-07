// pages/top/top.js
let config = require("../../config.js");

var update_top_storys = function(_this, is_first){
    console.log("update")
    wx.request({
        url: config.TOP_STORYS_API,
        success: function(res){
            console.log(res);
            _this.setData({
                top_storys: res.data.reverse()
            });
            if (!is_first){
                wx.showToast({
                    title: '刷新成功',
                })
            }
        },
        complete:function(e){
            wx.stopPullDownRefresh();
        }
    })
};

Page({

  /**
   * 页面的初始数据
   */
  data: {
    storys:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    update_top_storys(this, true);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
      console.log("pulldown");
    update_top_storys(this, false);
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
  
  }
})