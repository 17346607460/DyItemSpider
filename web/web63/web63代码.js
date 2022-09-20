var window = global;

function randoms(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

function getRandomValues(buf) {
    var min = 0,
        max = 255;
    if (buf.length > 65536) {
        var e = new Error();
        e.code = 22;
        e.message = 'Failed to execute \'getRandomValues\' : The ' + 'ArrayBufferView\'s byte length (' + buf.length + ') exceeds the ' + 'number of bytes of entropy available via this API (65536).';
        e.name = 'QuotaExceededError';
        throw e;
    }
    if (buf instanceof Uint16Array) {
        max = 65535;
    } else if (buf instanceof Uint32Array) {
        max = 4294967295;
    }
    for (var element in buf) {
        buf[element] = randoms(min, max);
    }
    return buf;
}

window.crypto = {}
window.crypto.getRandomValues = getRandomValues

lzaCv = function (O, K) {
    return O + K;
}

MYXEs = function (O, K) {
    return O * K;
}

cRGWF = function (O, K) {
    return O < K;
}

lzaCv = function (O, K) {
    return O + K;
}

function j(y) {
    let O = ''
        , K = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM';
    for (let z = -0x17 * -0x195 + -0x5 * -0x6c7 + 0x202 * -0x23; cRGWF(z, y); z++) {
        const o = new Uint32Array(0x186a + -0xf76 * 0x1 + -0x8f3);
        window['crypto']['getRandomValues'](o);
        let d0 = o[-0xa0 * 0x1 + 0x220 + -0x180] / (-0x102ce1257 * -0x1 + 0x32a7 * 0x8c8e5 + -0x1bfc5d9bb * 0x1 + (-0x145 * -0x17 + 0x234 * 0x11 + -0x42a6));
        O += K[Math['floor'](MYXEs(d0, 0x35b + -0x2e * -0x9c + 0x1f2f * -0x1))];
    }
    return lzaCv(O, 'f');
}

qromH = function (y, O) {
    return y(O);
}

function s(y) {
    var O = "0|1|3|4|2"['split']('|')
        , K = -0xf18 + -0x11c2 + 0x20da;
    while (!![]) {
        switch (O[K++]) {
            case '0':
                var z = require('crypto-js');
                continue;
            case '1':
                var o = "12345678912345678912345678912345";
                continue;
            case '2':
                return d1['toString']();
            case '3':
                var d0 = z['enc']['Utf8']['parse'](o);
                continue;
            case '4':
                var d1 = z['RC4']['encrypt'](y, d0, {});
                continue;
        }
        break;
    }
}

function N(y) {
    var O = new Uint8Array(y['length']);
    for (var K = 0x53 + -0x1be6 + 0x1b93 * 0x1; K < y['length']; K++) {
        O[K] = y['charCodeAt'](K);
    }
    return O['buffer'];
}

function get_data(y) {
    a = N(s(lzaCv(qromH(j, -0xb31 + 0x53 * -0x42 + 0x4b1 * 0x7), y['toString']())))
    return a
}

console.log(get_data(1))