setTimeout(function(){ajaxRefresh();}, 200);
setInterval("ajaxRefresh()", 1000*60*3);
function ajaxRefresh(){
    $.ajax({
        url: "/main/live",
        type: "GET",
        data: {},
        dataType: "json",
        cache: false,
        async: false,
        success: void{ }
    });
}