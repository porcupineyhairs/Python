setTimeout(function(){keepAlive();}, 200);
setInterval("keepAlive()", 1000*60*3);
function keepAlive(){
    $.ajax({
        url: "/main/keepAlive",
        type: "GET",
        data: {},
        dataType: "json",
        cache: false,
        async: false,
        success: void{ }
    });
}