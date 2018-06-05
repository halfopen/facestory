// pages/selfie_result/selfie_result.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    head_pic:null,
    face_reading:[],
    emotion:null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    var _this = this;
    wx.getStorage({
      key: 'photo_result',
      success: function(res) {
        console.log(res.data);
        var selfie_result = JSON.parse(res.data);
        console.log(selfie_result);
        var face_reading = [];
        for(var key in selfie_result.face_reading){
          face_reading.push(selfie_result.face_reading[key]);
        }
        console.log(face_reading);
        _this.setData({
          head_pic:selfie_result.image_url,
          face_reading: face_reading,
          emotion:selfie_result.emotion
        })
      },
    })
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
  onShareAppMessage: function (res) {
      return {
          title: 'face story',
          path: '/pages/index/index',
          imageUrl:'/images/baidu/timg_2.jpeg'
      }
  }
})