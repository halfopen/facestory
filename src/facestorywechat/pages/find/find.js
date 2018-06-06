// pages/find/find.js
let config = require("../../config.js");
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    shared_storys:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      var _this = this;
      wx.request({
          url: config.GET_SQUARE_STORYS_API,
          success: function (res) {
              console.log(res.data);
              _this.setData({
                  shared_storys: res.data
              })
          }
      })
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
      let story = this.data.shared_storys[id];
      console.log(this.data.shared_storys);
      wx.navigateTo({
          url: '/pages/selfie_result/selfie_result?result=' + encodeURIComponent(JSON.stringify(story.story_json)),
      })
      console.log(this.data.shared_storys[id])
  },
  clickTopStory: function(e){
      wx.showToast({
          title: '排名功能暂无',
      })
  }
})