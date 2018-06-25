// pages/my/my.js
let config = require("../../config.js");
let util = require("../../utils/util.js");
const app = getApp();

/**
 * 更新我的拍照记录
 */
var update_storys = function(_this, is_first){
    wx.request({
        url: config.FACE_STORY_TAG_API + "?openid=" + app.globalData.openid,
        success: function (res) {
            console.log(res);
            if(res.statusCode==200){
            _this.setData({
                my_storys: res.data
            });
            if(!is_first){
                // wx.showToast({
                //     title: '更新成功',
                // });
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
      my_storys:[],
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
    util.logger.log("进入我的")
    update_storys(this, false);
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    console.log("onhide")
    util.logger.log("离开我的")
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
  /**
   * 点击查看详情
   */
  clickStory: function (e) {
      let id = e.target.dataset.id;
      let tagIndex = e.currentTarget.dataset.tagIndex;
      console.log(e, e.target.dataset.storyId);
      console.log(id, tagIndex);
      let story = this.data.my_storys[tagIndex].face_storys[id];
      console.log(this.data.my_storys);
      wx.navigateTo({
          url: '/pages/selfie_result/selfie_result?story=' + encodeURIComponent(JSON.stringify(story)),
      })
      console.log(this.data.my_storys[id])
  },
  /**
   * 长按删除
   */
  longTapStory: function(e){
      let storyId = e.currentTarget.dataset.storyId;
      
      let _this = this;
      console.log(storyId)
      wx.showModal({
          title: '是否删除',
          content: '',
          success:function(e){
              console.log(e, e.confirm)
              if(e.confirm==true){
                  wx.request({
                      url: config.STORY_API+"?id="+storyId,
                      method:"DELETE",
                      complete: function(e){
                          console.log(e)
                          update_storys(_this, false)
                      }
                  })
              }
          }
      })
  },

  /**
   * 点击添加家人和朋友
   */
  tapAddTag: function(e){
      wx.navigateTo({
          url: '/pages/add_tag/add_tag',
      })
  }
})