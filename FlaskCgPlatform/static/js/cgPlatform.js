//获取用户信息
function getUserInfo() {
    $.ajax({
        type: "GET",//使用get方法访问后台
        dataType: "json",//返回json格式的数据
        url: "/user/api/userinfo",//要访问的后台地址
        cache : false,
        error:function(){
            alert("无法连接服务器");
        },
        success: function (get) {
            var success = get["success"];
            if(success === 'no'){
                alert(get["msg"]);
            }
            else if(success === 'yes'){
                document.getElementById('user-name').innerHTML = get["user_name"];
                document.getElementById('company-id').innerHTML = get["company_id"];
                document.getElementById('company-name').innerHTML = get["company_name"];
                document.getElementById('company-name2').innerHTML = get["company_name"];
            }
        }
    });
}

// 退出登录
function userLogout(){
			    $.ajax({
					type: "GET",//使用get方法访问后台
					dataType: "json",//返回json格式的数据
					url: "/user/api/logout",//要访问的后台地址
					cache : false,
					error:function(){
						alert("无法连接服务器");
					},
					success: function (get) {
						var success = get["success"];
						if(success === 'no'){
							alert(get["msg"]);
						}
						else if(success === 'yes'){
							location.href = get["url"]
						}
					}
				});
            }