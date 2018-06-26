// pages/selfie_result/selfie_result.js
let app = getApp();
let config = require("../../config.js");
let util = require("../../utils/util.js");
var is_my_story = false;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    story_id:0, 
    head_pic:"/images/baidu/timg_3.jpeg",
    results:[{
        item_title:{content:"暂无数据"},
        item_detail:{
            contents:[{
                type:"text",
                content:"..."
            }]
        }
    }],
    in_square:false,
    like:0,
    is_my_story:false,
    story:null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      if('undefined'!=typeof(options.story)){
            var _this = this;
            var story = JSON.parse( decodeURIComponent(options.story));
            console.log(story, app.globalData.openid == story.openid, app.globalData.openid , story.openid);
            if(app.globalData.openid== story.openid){
                is_my_story = true;
            }
            _this.setData({
                story_id:story.id,
                head_pic: story.story_json.image_url,
                results: story.story_json.results,
                is_my_story:is_my_story,
                in_square: story.in_square+0,
                story:story,
                tag:story.tag
            })
      }
      
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
    util.logger.log("进入拍照结果")
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
      util.logger.log("离开拍照结果");
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    console.log("onUnload selfieresult");
    // 拍照结果一般是点左上角返回按钮
    util.logger.log("离开拍照结果");
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
      console.log("share", res);
      return {
          title: '面部分析结果',
          path: '/pages/selfie_result/selfie_result?share=1&story='+encodeURIComponent(JSON.stringify(this.data.story)),
          imageUrl:this.data.head_pic,
          success:function(res){

          }
      }
  },

  // 点击分享按钮
  clickShareStory:function(e){
      wx.showLoading({
          title: '请求中',
      })
      var _this = this;
      console.log(e, e.target.dataset.inSquare);
      var inSquare = e.target.dataset.inSquare;
      var tips = "成功从广场撤回";
      var story_id = e.target.dataset.storyId;
      if(inSquare==0){
          tips = "成功分享到广场";
      }
    wx.request({
        url: config.SHARE_TO_SQUARE_API,
        data:{
            id:story_id,
            in_square:!inSquare+0
        },
        success:function(res){
            console.log(res);
            _this.setData({
                in_square:!inSquare+0
            });
            wx.showToast({
                title: tips,
            });

        },
        complete:function(e){
            wx.hideLoading();
        }
    })
  },
  
  // 点击保存按钮
  clickSave: function(e){
      wx.navigateTo({
          url: '/pages/save_result/save_result?story_id='+this.data.story_id+"&tag_id="+this.data.tag.id,
      })
  }
})