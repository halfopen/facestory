// pages/add_tag/add_tag.js
let app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        genders: ["男", "女"],
        gender_index: 0,

        gender: "男",
        name: "",
        birth: "1900-01-01"
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

    bindDateChange: function (e) {
        console.log('picker发送选择改变，携带值为', e.detail.value)
        this.setData({
            birth: e.detail.value
        })
    },

    bindPickerChange: function (e) {
        console.log('picker发送选择改变，携带值为', e.detail.value)
        this.setData({
            gender_index: e.detail.value,
            gender: this.data.genders[e.detail.value]
        })
    },

    tapAdd: function (e) {
        var _this = this;
        console.log("点击添加", e, this.data.gender, this.data.birth, this.data.name)
        wx.getStorage({
            key: 'openid',
            success: function (res) {
                let openid = res.data;
                wx.request({
                    url: app.config.FACE_STORY_TAG_API,
                    method: "POST",
                    data: {
                        name: _this.data.name,
                        birth: _this.data.birth,
                        gender: _this.data.gender,
                        openid: openid
                    },
                    success: function (res) {
                        console.log(res)
                        wx.showModal({
                            title: '添加成功',
                            content: '是否继续添加',
                            cancelText:"开始测试",
                            confirmText:"继续添加",
                            success:function(res){
                                if(res.confirm){

                                }
                            }
                        })
                    }
                })
            },
        })


    },

    inputName: function (e) {
        console.log(e);
        this.data.name = e.detail.value
    }
})