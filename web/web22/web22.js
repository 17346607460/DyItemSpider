document = {}
var url = "/api/challenge22";
call = function(num) {
    function randomString(len) {
        len = len || 32;
        var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz123456789=+-';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
        var maxPos = $chars.length;
        var pwd = '';
        for (i = 0; i < len; i++) {
            pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
        }
        return pwd;
    }
    seed=randomString(32);
    document.cookie = '"Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1663047488; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1663139345; __yr_token__=b301cDCpkLCc/Bihhd3ZefksbJHALBiJSLXUNFzdVPH5qL0dzT1cSTShddANzZiEeYG1YJzIeWCsnG0dPUTIxfnpzaB8bG0MnLR50OVA6XQkZRAAVUnQwMA83WAZYF3ZrXAZPABUMG3kJWQNBYRY="'
    var list = {
        "page": String(num),
    };
    $.ajax({
        url: url,
        dataType: "json",
        async: true,
        data: list,
        type: "POST",
        beforeSend: function(request) {
            (function() {})()
        },
        success: function(data) {
            var s = '<tr class="odd">';
            datas = data.data;
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
            alert('风控检测到您的数据异常，请关闭抓包工具并使用谷歌浏览器重试');
            location.reload()
        }
    })
}
call(1)