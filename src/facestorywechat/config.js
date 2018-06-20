const BASE_URL = "https://facestory.cn:5000"
var config = {
    FACE_DETECT_API:  BASE_URL+"/detect",
    GET_OPENID_API: BASE_URL+"/get_openid",
    GET_MY_STORYS_API:BASE_URL+"/get_my_storys",
    GET_SQUARE_STORYS_API: BASE_URL + "/get_square_storys",
    USER_INFO_API: BASE_URL+"/user_info",
    SHARE_TO_SQUARE_API: BASE_URL+"/share_to_square",
    TOP_STORYS_API: BASE_URL +"/top_storys",
    LOG_API: BASE_URL+"/api/log",
    STORY_API:BASE_URL+"/story",
    INFO_CODE:1,
    ERROR_CODE:-1,
    LOG_CODE:0
}

module.exports = config