const BASE_URL = "https://facestory.cn:5000"
var config = {
    FACE_DETECT_API:  BASE_URL+"/detect",
    GET_OPENID_API: BASE_URL+"/get_openid",
    USER_INFO_API: BASE_URL+"/user_info",
    SHARE_TO_SQUARE_API: BASE_URL+"/share_to_square",
    FACESTORYS_API: BASE_URL +"/facestory",
    LOG_API: BASE_URL+"/log",
    STORY_API:BASE_URL+"/story",
    FACE_STORY_TAG_API:BASE_URL+"/facestory_tag",

    INFO_CODE:1,
    ERROR_CODE:-1,
    LOG_CODE:0
}

module.exports = config