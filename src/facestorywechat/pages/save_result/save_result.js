// pages/save_result/save_result.js
let app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    tags:[],
    selected:0,
    story_id:0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("options",options)
    this.data.story_id = options.story_id;
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
      var _this = this;
      wx.getStorage({
          key: 'openid',
          success: function(res) {
              let openid = res.data;
              wx.request({
                  url: app.config.FACE_STORY_TAG_API+"?openid="+openid,
                  success:function(res){
                      console.log(res);
                      _this.setData({
                          tags:res.data
                      });
                  }
              })
          },
      })

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

  /**
   * 点击选择用户
   */
  tapTag: function(e){
      let index = e.currentTarget.dataset.index;
      this.setData({
          selected:index
      });
  },

/**
 * 点击保存结果
 */
  tapSaveResult:function(e){
      let facestory_tag_id = this.data.tags[this.data.selected].id;
      let facestory_id = this.data.story_id;
      console.log(facestory_tag_id, facestory_id);

      wx.showLoading({
          title: '保存成功',
      })
      setTimeout(function(){

            wx.navigateBack({

            })
      }, 1000);

  }
})