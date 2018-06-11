const BASE_URL = "http://localhost:5000"
var config = {
    FACE_DETECT_API:  BASE_URL+"/detect",
    GET_OPENID_API: BASE_URL+"/get_openid",
    GET_MY_STORYS_API:BASE_URL+"/get_my_storys",
    GET_SQUARE_STORYS_API: BASE_URL + "/get_square_storys",
    USER_INFO_API: BASE_URL+"/user_info",
    SHARE_TO_SQUARE_API: BASE_URL+"/share_to_square",
    TOP_STORYS_API: BASE_URL +"/top_storys",
    STORY_API:BASE_URL+"/story"
}

module.exports = config