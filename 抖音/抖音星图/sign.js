const y = "e39539b8836fb99e1538974d3ac1fe98";
r = {
    stringToBytes: function(e) {
        for (var t = [], n = 0; n < e.length; n++)
            t.push(255 & e.charCodeAt(n));
        return t
    },
    bytesToString: function(e) {
        return decodeURIComponent(escape(t.bin.bytesToString(e)))
    }
}
n = {
    rotl: function(e, t) {
        return e << t | e >>> 32 - t
    },
    rotr: function(e, t) {
        return e << 32 - t | e >>> t
    },
    endian: function(e) {
        if (e.constructor == Number)
            return 16711935 & n.rotl(e, 8) | 4278255360 & n.rotl(e, 24);
        for (var t = 0; t < e.length; t++)
            e[t] = n.endian(e[t]);
        return e
    },
    randomBytes: function(e) {
        for (var t = []; e > 0; e--)
            t.push(Math.floor(256 * Math.random()));
        return t
    },
    bytesToWords: function(e) {
        for (var t = [], n = 0, r = 0; n < e.length; n++,
        r += 8)
            t[r >>> 5] |= e[n] << 24 - r % 32;
        return t
    },
    wordsToBytes: function(e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8)
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
        return t
    },
    bytesToHex: function(e) {
        for (var t = [], n = 0; n < e.length; n++)
            t.push((e[n] >>> 4).toString(16)),
            t.push((15 & e[n]).toString(16));
        return t.join("")
    },
    hexToBytes: function(e) {
        for (var t = [], n = 0; n < e.length; n += 2)
            t.push(parseInt(e.substr(n, 2), 16));
        return t
    },
    bytesToBase64: function(e) {
        for (var n = [], r = 0; r < e.length; r += 3)
            for (var i = e[r] << 16 | e[r + 1] << 8 | e[r + 2], o = 0; o < 4; o++)
                8 * r + 6 * o <= 8 * e.length ? n.push(t.charAt(i >>> 6 * (3 - o) & 63)) : n.push("=");
        return n.join("")
    },
    base64ToBytes: function(e) {
        e = e.replace(/[^A-Z0-9+\/]/gi, "");
        for (var n = [], r = 0, i = 0; r < e.length; i = ++r % 4)
            0 != i && n.push((t.indexOf(e.charAt(r - 1)) & Math.pow(2, -2 * i + 8) - 1) << 2 * i | t.indexOf(e.charAt(r)) >>> 6 - 2 * i);
        return n
    }
}
t = {
    rotl: function(e, t) {
        return e << t | e >>> 32 - t
    },
    rotr: function(e, t) {
        return e << 32 - t | e >>> t
    },
    endian: function(e) {
        if (e.constructor == Number)
            return 16711935 & n.rotl(e, 8) | 4278255360 & n.rotl(e, 24);
        for (var t = 0; t < e.length; t++)
            e[t] = n.endian(e[t]);
        return e
    },
    randomBytes: function(e) {
        for (var t = []; e > 0; e--)
            t.push(Math.floor(256 * Math.random()));
        return t
    },
    bytesToWords: function(e) {
        for (var t = [], n = 0, r = 0; n < e.length; n++,
        r += 8)
            t[r >>> 5] |= e[n] << 24 - r % 32;
        return t
    },
    wordsToBytes: function(e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8)
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
        return t
    },
    bytesToHex: function(e) {
        for (var t = [], n = 0; n < e.length; n++)
            t.push((e[n] >>> 4).toString(16)),
            t.push((15 & e[n]).toString(16));
        return t.join("")
    },
    hexToBytes: function(e) {
        for (var t = [], n = 0; n < e.length; n += 2)
            t.push(parseInt(e.substr(n, 2), 16));
        return t
    },
    bytesToBase64: function(e) {
        for (var n = [], r = 0; r < e.length; r += 3)
            for (var i = e[r] << 16 | e[r + 1] << 8 | e[r + 2], o = 0; o < 4; o++)
                8 * r + 6 * o <= 8 * e.length ? n.push(t.charAt(i >>> 6 * (3 - o) & 63)) : n.push("=");
        return n.join("")
    },
    base64ToBytes: function(e) {
        e = e.replace(/[^A-Z0-9+\/]/gi, "");
        for (var n = [], r = 0, i = 0; r < e.length; i = ++r % 4)
            0 != i && n.push((t.indexOf(e.charAt(r - 1)) & Math.pow(2, -2 * i + 8) - 1) << 2 * i | t.indexOf(e.charAt(r)) >>> 6 - 2 * i);
        return n
    }
}
function A(e) {
    return void 0 === e || null === e
}
function b(e) {
    return ["string", "number"].includes(typeof e)
}
v = function(e, n) {
    if (void 0 === e || null === e)
        throw new Error("Illegal argument " + e);
    var r = wordsToBytes(a(e, n));
    return n && n.asBytes ? r : n && n.asString ? o.bytesToString(r) : t.bytesToHex(r)
}
wordsToBytes = function(e) {
    for (var t = [], n = 0; n < 32 * e.length; n += 8)
        t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
    return t
}
a = function(e, n) {
    e.constructor == String ? e = n && "binary" === n.encoding ? o.stringToBytes(e) : r.stringToBytes(e) : i(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || e.constructor === Uint8Array || (e = e.toString());
    for (var s = t.bytesToWords(e), l = 8 * e.length, u = 1732584193, c = -271733879, d = -1732584194, f = 271733878, h = 0; h < s.length; h++)
        s[h] = 16711935 & (s[h] << 8 | s[h] >>> 24) | 4278255360 & (s[h] << 24 | s[h] >>> 8);
    s[l >>> 5] |= 128 << l % 32,
    s[14 + (l + 64 >>> 9 << 4)] = l;
    var p = a._ff
      , g = a._gg
      , m = a._hh
      , v = a._ii;
    for (h = 0; h < s.length; h += 16) {
        var y = u
          , A = c
          , b = d
          , _ = f;
        u = p(u, c, d, f, s[h + 0], 7, -680876936),
        f = p(f, u, c, d, s[h + 1], 12, -389564586),
        d = p(d, f, u, c, s[h + 2], 17, 606105819),
        c = p(c, d, f, u, s[h + 3], 22, -1044525330),
        u = p(u, c, d, f, s[h + 4], 7, -176418897),
        f = p(f, u, c, d, s[h + 5], 12, 1200080426),
        d = p(d, f, u, c, s[h + 6], 17, -1473231341),
        c = p(c, d, f, u, s[h + 7], 22, -45705983),
        u = p(u, c, d, f, s[h + 8], 7, 1770035416),
        f = p(f, u, c, d, s[h + 9], 12, -1958414417),
        d = p(d, f, u, c, s[h + 10], 17, -42063),
        c = p(c, d, f, u, s[h + 11], 22, -1990404162),
        u = p(u, c, d, f, s[h + 12], 7, 1804603682),
        f = p(f, u, c, d, s[h + 13], 12, -40341101),
        d = p(d, f, u, c, s[h + 14], 17, -1502002290),
        c = p(c, d, f, u, s[h + 15], 22, 1236535329),
        u = g(u, c, d, f, s[h + 1], 5, -165796510),
        f = g(f, u, c, d, s[h + 6], 9, -1069501632),
        d = g(d, f, u, c, s[h + 11], 14, 643717713),
        c = g(c, d, f, u, s[h + 0], 20, -373897302),
        u = g(u, c, d, f, s[h + 5], 5, -701558691),
        f = g(f, u, c, d, s[h + 10], 9, 38016083),
        d = g(d, f, u, c, s[h + 15], 14, -660478335),
        c = g(c, d, f, u, s[h + 4], 20, -405537848),
        u = g(u, c, d, f, s[h + 9], 5, 568446438),
        f = g(f, u, c, d, s[h + 14], 9, -1019803690),
        d = g(d, f, u, c, s[h + 3], 14, -187363961),
        c = g(c, d, f, u, s[h + 8], 20, 1163531501),
        u = g(u, c, d, f, s[h + 13], 5, -1444681467),
        f = g(f, u, c, d, s[h + 2], 9, -51403784),
        d = g(d, f, u, c, s[h + 7], 14, 1735328473),
        c = g(c, d, f, u, s[h + 12], 20, -1926607734),
        u = m(u, c, d, f, s[h + 5], 4, -378558),
        f = m(f, u, c, d, s[h + 8], 11, -2022574463),
        d = m(d, f, u, c, s[h + 11], 16, 1839030562),
        c = m(c, d, f, u, s[h + 14], 23, -35309556),
        u = m(u, c, d, f, s[h + 1], 4, -1530992060),
        f = m(f, u, c, d, s[h + 4], 11, 1272893353),
        d = m(d, f, u, c, s[h + 7], 16, -155497632),
        c = m(c, d, f, u, s[h + 10], 23, -1094730640),
        u = m(u, c, d, f, s[h + 13], 4, 681279174),
        f = m(f, u, c, d, s[h + 0], 11, -358537222),
        d = m(d, f, u, c, s[h + 3], 16, -722521979),
        c = m(c, d, f, u, s[h + 6], 23, 76029189),
        u = m(u, c, d, f, s[h + 9], 4, -640364487),
        f = m(f, u, c, d, s[h + 12], 11, -421815835),
        d = m(d, f, u, c, s[h + 15], 16, 530742520),
        c = m(c, d, f, u, s[h + 2], 23, -995338651),
        u = v(u, c, d, f, s[h + 0], 6, -198630844),
        f = v(f, u, c, d, s[h + 7], 10, 1126891415),
        d = v(d, f, u, c, s[h + 14], 15, -1416354905),
        c = v(c, d, f, u, s[h + 5], 21, -57434055),
        u = v(u, c, d, f, s[h + 12], 6, 1700485571),
        f = v(f, u, c, d, s[h + 3], 10, -1894986606),
        d = v(d, f, u, c, s[h + 10], 15, -1051523),
        c = v(c, d, f, u, s[h + 1], 21, -2054922799),
        u = v(u, c, d, f, s[h + 8], 6, 1873313359),
        f = v(f, u, c, d, s[h + 15], 10, -30611744),
        d = v(d, f, u, c, s[h + 6], 15, -1560198380),
        c = v(c, d, f, u, s[h + 13], 21, 1309151649),
        u = v(u, c, d, f, s[h + 4], 6, -145523070),
        f = v(f, u, c, d, s[h + 11], 10, -1120210379),
        d = v(d, f, u, c, s[h + 2], 15, 718787259),
        c = v(c, d, f, u, s[h + 9], 21, -343485551),
        u = u + y >>> 0,
        c = c + A >>> 0,
        d = d + b >>> 0,
        f = f + _ >>> 0
    }
    return t.endian([u, c, d, f])
}
a._ff = function(e, t, n, r, i, o, a) {
    var s = e + (t & n | ~t & r) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
,
a._gg = function(e, t, n, r, i, o, a) {
    var s = e + (t & r | n & ~r) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
,
a._hh = function(e, t, n, r, i, o, a) {
    var s = e + (t ^ n ^ r) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
,
a._ii = function(e, t, n, r, i, o, a) {
    var s = e + (n ^ (t | ~r)) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
,
a._blocksize = 16,
a._digestsize = 16
function w(e, t, n) {
    const {include: r, enforceWithKeys: i=[]} = null !== t && void 0 !== t ? t : {};
    let o = Object.keys(e);
    if (n && r) {
        const e = r.concat(["service_name", "service_method", "sign_strict"]);
        o = o.filter((t=>e.includes(t)))
    }
    const a = o.sort().map((t=>{
        const n = e[t];
        return A(n) ? "" : t + (!i.includes(t) && b(n) ? n : t)
    }
    )).join("");
    return v(a + y)
    // return v("attribute_filterattribute_filterauthor_pack_filterauthor_pack_filterdisplay_scene1limit20order_byscorepage1platform_source1regular_filterregular_filtersearch_scene1service_methodSearchForStarAuthorsservice_namego_search.AdStarGoSearchServicesign_strict1sort_type2e39539b8836fb99e1538974d3ac1fe98")
}


function get_sign(page) {
    return w(
        {
            "platform_source": 1,
            "order_by": "score",
            "sort_type": 2,
            "search_scene": 1,
            "display_scene": 1,
            "limit": 20,
            "page": page,
            "regular_filter": {
                "current_tab": 3,
                "marketing_target": 2,
                "task_category": 1
            },
            "attribute_filter": {
                "tag": "[55]"
            },
            "author_pack_filter": {},
            "service_name": "go_search.AdStarGoSearchService",
            "service_method": "SearchForStarAuthors",
            "sign_strict": 1
        },
        {
            "include": [
                "platform_source",
                "search_scene",
                "display_scene",
                "page",
                "limit",
                "sort_type",
                "order_by",
                "key",
                "regular_filter",
                "attribute_filter",
                "author_pack_filter",
                "non_standard_filter",
                "author_list_id",
                "is_download",
                "filter_str"
            ]
        },
        true
    )
}

// e = {
//     "platform_source": 1,
//     "order_by": "score",
//     "sort_type": 2,
//     "search_scene": 1,
//     "display_scene": 1,
//     "limit": 20,
//     "page": 21,
//     "regular_filter": {
//         "current_tab": 3,
//         "marketing_target": 2,
//         "task_category": 1
//     },
//     "attribute_filter": {
//         "tag": "[55]"
//     },
//     "author_pack_filter": {},
//     "service_name": "go_search.AdStarGoSearchService",
//     "service_method": "SearchForStarAuthors",
//     "sign_strict": 1
// }