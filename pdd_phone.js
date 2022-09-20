function m(e) {
    var t = e.ciphertext
      , n = e.secret
      , r = {
        "=": 0
    };
    d.forEach((function(e, t) {
        r[e] = t
    }
    ));
    var a = "";
    t.split("").map((function(e) {
        var t = r[e];
        a += (0,
        l.default)(t.toString(2), 6, "0")
    }
    ));
    for (var o = "", c = a.length - 8; c >= 0; c -= 8) {
        var s = parseInt(a.slice(c, c + 8), 2);
        0 === s && 0 === o.length || (o = String.fromCharCode(s) + o)
    }
    for (var f = n.split(""), p = (0,
    i.default)(f, 2), h = p[0], m = p[1], g = function(e) {
        var t = parseInt(e, 16);
        return (t >= m ? t - m : t + 16 - m).toString(16)
    }, v = [], b = 0; b < o.length; b += 4) {
        var y = o.slice(b, b + 4);
        v.push(y.slice(0, h) + g(y[h]) + y.slice(+h + 1))
    }
    return (0,
    u.utf8ToChar)(v.map((function(e) {
        return parseInt(e, 16)
    }
    )))
}



function get_phone_number(e){
    t = e.data
    n = e.web_spider_rule
    r = n.slice(34, 35)
    i = n.slice(100).split("|");
    switch (r) {
    case "1":
        a = n.slice(35, 99)
        o = f
        break
    case "2":
        a = n.slice(35, 99)
        o = p
        break
    case "3":
        a = n.slice(35, 36)
        o = h
        break
    case "4":
        a = n.slice(35, 37)
        o = m
    }
    console.log(o({
        ciphertext: t,
        secret: a
    }))
}
data = {
    can_virtual_extend: false,
    cannot_extend_reason_type: 1,
    ext_number: "2455",
    has_report: false,
    mobile_from_order_print: false,
    order_sn: "220606-542292110791211",
    show_export_popup: false,
    show_virtual_report_button: true,
    show_virtual_risk_tip: false,
    show_virtual_tip_after_mobile: true,
    virtual_expired_timestamp: 1665560649,
    virtual_extend_expired_timestamp: 1665560649,
    virtual_mobile: "MDMzMTAzMzgwMzM0MDMzNjAzMzYwMzM4MDMzNDAzMzIwMzMzMDMzNTAzMzI=",
    web_spider_rule: "4120f3f4b6524e61943b0ae7f9e7d3ae4v413eHotyzWwBtzREtwNH4CTh7B9/CCTzMMaQB/Zo3+MbN0OXHbPUwiEnYvyKeQ4AZ|$.contact_mobile|$.virtual_mobile|$.mobile"
}
get_phone_number(data)
// console.log("83af5f30635d47168aae5195f2073d95sv1^kb5P*af4g9xDx0PBDt0b7789&uiCszsbba15e09c7843264b53c08e4ad2971d5|$.contact_mobile|$.virtual_mobile|$.mobile".slice(35, 99))