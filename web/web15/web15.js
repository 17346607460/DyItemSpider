call = function(num) {
	window.sign = '';
    $("#loadingDiv").show();
    $('.sign').remove();
    $('.now').remove();
    $('body').append($("<script>").attr({
                class:"now",
                type:"text/javascript",
                src:"/cityjson"
    }));
    $('.page-box').hide();
    $.getScript("/api/challenge15/js?_t=" + returnCitySN["timestamp"], function () {
    if (window.sign){
        var sign = window.sign
	}
	else {
        var sign = $.cookie('sign');

    }
        var list = {
        "page": String(num),
        "sign": sign
    };
    $.ajax({
        url: url,
        dataType: "json",
        async: true,
        data: list,
        type: "POST",
        beforeSend: function(request) {
        },
        success: function(data) {

            var s = '<tr class="odd">';
            datas = data.data;
            window.datas=datas
            $.each(datas, function(index, val) {
                var html = '<td class="info fonteditor">' + val.value + '</td>';
                s += html
            });
            $('.data').text('').append(s + '</tr>');

            $("#loadingDiv").hide();
            $('.page-box').show();
        },

        complete: function() {
            $.removeCookie('sign', { path: '/' });
            $("#page").paging({
                nowPage: num,
                pageNum: 100,
                buttonNum: 7,
                canJump: 1,
                showOne: 1,
                callback: function(num) {
                    call(num)
                },
            })
        },
        error: function() {
            location.reload()
        }
    })









    });





}