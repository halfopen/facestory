const BASE_URL = "http://localhost:5000"
var config = {
    FACE_DETECT_API:  BASE_URL+"/detect",
    GET_OPENID_API: BASE_URL+"/get_openid",
    GET_MY_STORYS_API:BASE_URL+"/get_my_storys",
    GET_SQUARE_STORYS_API: BASE_URL + "/get_square_storys"
}

module.exports = config