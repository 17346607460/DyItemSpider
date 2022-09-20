prefixInteger = function(a, b) {
    return (Array(b).join(0) + a).slice(-b)
}

string10to64 = function(d) {
    var c = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~".split("")
      , b = c.length
      , e = +d
      , a = [];
    do {
        mod = e % b;
        e = (e - mod) / b;
        a.unshift(c[mod])
    } while (e);
    return a.join("")
}

pretreatment = function(d, c, b) {
    var f = this;
    var e = string10to64(Math.abs(d));
    var a = "";
    if (!b) {
        a += (d > 0 ? "1" : "0")
    }
    a += prefixInteger(e, c);
    return a
}

function getCoordinate(c) {
    var b = new Array();
    for (var e = 0; e < c.length; e++) {
        if (e == 0) {
            b.push(pretreatment(c[e][0] < 262143 ? c[e][0] : 262143, 3, true));
            b.push(pretreatment(c[e][1] < 16777215 ? c[e][1] : 16777215, 4, true));
            b.push(pretreatment(c[e][2] < 4398046511103 ? c[e][2] : 4398046511103, 7, true))
        } else {
            var a = c[e][0] - c[e - 1][0];
            var f = c[e][1] - c[e - 1][1];
            var d = c[e][2] - c[e - 1][2];
            b.push(pretreatment(a < 4095 ? a : 4095, 2, false));
            b.push(pretreatment(f < 4095 ? f : 4095, 2, false));
            b.push(pretreatment(d < 16777215 ? d : 16777215, 4, true))
        }
    }
    return b.join("")
}

function get_c() {
    a = {
        "version": "1.0",
        "bizId": "passport_jd_com_login_pc",
        "elementId": "0",
        "seq": "focus",
        "sessionId": "3288145627089396536",
        "sp": 23,
        "eid": "QIA4VKJLEBK7HKLL45XNANJUBXCJI26WLREC3OYB5BO33SGYTSOE4O2VVR3FDTBV74CYZBBCBNY7PA5KMTAZT4M7ZE",
        "val": "1",
        "ctime": new Date().getTime()
    }

    C = function (a) {
        if (void 0 == a || null == a)
            return null;
        var b = "{", e;
        for (e in a)
            b += "'" + e + "':",
                b = "string" == typeof a[e] ? b + ("'" + a[e] + "'") : b + a[e],
                b += ",";
        b = b.substring(0, b.length - 1);
        return E(b + "}")
    }

    E = function (a) {
        this.tdmovebit = function () {
            var a = 10
                , b = 20
                , c = 30;
            ++a;
            a++;
            a = ++a + ++b + c++ + a++;
            return d + a - 76
        }
        ;
        var b = "23IL";
        a = encodeURIComponent(a);
        var e = ""
            , c = "";
        b += "<N01c7KvwZO56RSTAfghiFyzWJqVabGH4PQdopUrsCuX*xeBjkltDEmn89.-";
        var d = 0;
        var g = "";
        do {
            var h = a.charCodeAt(d);
            d = this.tdmovebit(d);
            var f = a.charCodeAt(d);
            d = this.tdmovebit(d);
            e = a.charCodeAt(d);
            d = this.tdmovebit(d);
            var k = h >> Math.round(((19 << 43) / 90 ^ 34) / 214);
            h = (h & 3) << 4 | f >> 4;
            var l = (f & 15) << 2 | e >> 6;
            c = e & Math.round(((19 << 43) / 90 ^ 34) / 6) - 4;
            isNaN(f) ? l = c = Math.round(((19 << 43) / 90 ^ 34) / 6) - 3 : isNaN(e) && (c = Math.round(((19 << 43) / 90 ^ 34) / 6) - 3);
            g = g + b.charAt(k) + b.charAt(h) + b.charAt(l) + b.charAt(c);
            k = h = l = c = h = f = e = ""
        } while (d <= a.length);
        return g + "/"
    }
    return C(a)
}