// chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile" 控制当前浏览器

call = function(num) {
    var list = {
        "page": String(num),
        "token": window.token,
    };
    $.ajax({
        url: url,
        dataType: "json",
        async: true,
        data: list,
        type: "POST",
        beforeSend: function(request) {
            (function() {
                var httpRequest = new XMLHttpRequest();
                var url = '/cityjson';
                httpRequest.open('POST', url, false);
                httpRequest.send()
            })()
        },
        success: function(data) {
            window[data.k['k'].split('|')[0]]=parseInt(data.k['k'].split('|')[1]);
            var s = '<tr class="odd">';
            datas = data.data;
            window.datas = datas
            $.each(datas, function(index, val) {
                var html = '<td class="info">' + val.value + '</td>';
                s += html
            });
            $('.data').text('').append(s + '</tr>')
        },
        complete: function() {
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
            alert('加载失败败')
            location.reload()
        }
    })
};