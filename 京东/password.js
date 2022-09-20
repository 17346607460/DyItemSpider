var bY, bE = 28, a4 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

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

var g = [
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    null,
    null,
    null,
    null,
    null,
    null,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35
]

function aX(z, t) {
    var L = g[z.charCodeAt(t)];
    return (L == null) ? -1 : L
}

function bI(bZ, z) {
    var bW;
    if (z == 16) {
        bW = 4
    } else {
        if (z == 8) {
            bW = 3
        } else {
            if (z == 256) {
                bW = 8
            } else {
                if (z == 2) {
                    bW = 1
                } else {
                    if (z == 32) {
                        bW = 5
                    } else {
                        if (z == 4) {
                            bW = 2
                        } else {
                            this.fromRadix(bZ, z);
                            return
                        }
                    }
                }
            }
        }
    }
    this.t = 0;
    this.s = 0;
    var bY = bZ.length
      , L = false
      , bX = 0;
    while (--bY >= 0) {
        var t = (bW == 8) ? bZ[bY] & 255 : aX(bZ, bY);
        if (t < 0) {
            if (bZ.charAt(bY) == "-") {
                L = true
            }
            continue
        }
        L = false;
        if (bX == 0) {
            this[this.t++] = t
        } else {
            if (bX + bW > this.DB) {
                this[this.t - 1] |= (t & ((1 << (this.DB - bX)) - 1)) << bX;
                this[this.t++] = (t >> (this.DB - bX))
            } else {
                this[this.t - 1] |= t << bX
            }
        }
        bX += bW;
        if (bX >= this.DB) {
            bX -= this.DB
        }
    }
    if (bW == 8 && (bZ[0] & 128) != 0) {
        this.s = -1;
        if (bX > 0) {
            this[this.t - 1] |= ((1 << (this.DB - bX)) - 1) << bX
        }
    }
    this.clamp();
    if (L) {
        bf.ZERO.subTo(this, this)
    }
}

function bA() {
    var t = this.s & this.DM;
    while (this.t > 0 && this[this.t - 1] == t) {
        --this.t
    }
}

function bf(z, t, L) {
    if (z != null) {
        if ("number" == typeof z) {
            this.fromNumber(z, t, L)
        } else {
            if (t == null && "string" != typeof z) {
                this.fromString(z, 256)
            } else {
                this.fromString(z, t)
            }
        }
    }
}

function q(z) {
    var bW = 1, L;
    if ((L = z >>> 16) != 0) {
        z = L;
        bW += 16
    }
    if ((L = z >> 8) != 0) {
        z = L;
        bW += 8
    }
    if ((L = z >> 4) != 0) {
        z = L;
        bW += 4
    }
    if ((L = z >> 2) != 0) {
        z = L;
        bW += 2
    }
    if ((L = z >> 1) != 0) {
        z = L;
        bW += 1
    }
    return bW
}

function bt() {
    if (this.t <= 0) {
        return 0
    }
    return this.DB * (this.t - 1) + q(this[this.t - 1] ^ (this.s & this.DM))
}


function ad() {
    return ((this.t > 0) ? (this[0] & 1) : this.s) == 0
}

function K(t) {
    this.m = t;
    this.mp = t.invDigit();
    this.mpl = this.mp & 32767;
    this.mph = this.mp >> 15;
    this.um = (1 << (t.DB - 15)) - 1;
    this.mt2 = 2 * t.t
}

function by(t) {
    var z = bm();
    t.abs().dlShiftTo(this.m.t, z);
    z.divRemTo(this.m, null, z);
    if (t.s < 0 && z.compareTo(bf.ZERO) > 0) {
        this.m.subTo(z, z)
    }
    return z
}
function bl(t) {
    var z = bm();
    t.copyTo(z);
    this.reduce(z);
    return z
}
function bV(t) {
    while (t.t <= this.mt2) {
        t[t.t++] = 0
    }
    for (var L = 0; L < this.m.t; ++L) {
        var z = t[L] & 32767;
        var bW = (z * this.mpl + (((z * this.mph + (t[L] >> 15) * this.mpl) & this.um) << 15)) & t.DM;
        z = L + this.m.t;
        t[z] += this.m.am(0, bW, t, L, 0, this.m.t);
        while (t[z] >= t.DV) {
            t[z] -= t.DV;
            t[++z]++
        }
    }
    t.clamp();
    t.drShiftTo(this.m.t, t);
    if (t.compareTo(this.m) >= 0) {
        t.subTo(this.m, t)
    }
}
function ac(t, z) {
    t.squareTo(z);
    this.reduce(z)
}
function bz(t, L, z) {
    t.multiplyTo(L, z);
    this.reduce(z)
}

function ab() {
    if (this.t < 1) {
        return 0
    }
    var t = this[0];
    if ((t & 1) == 0) {
        return 0
    }
    var z = t & 3;
    z = (z * (2 - (t & 15) * z)) & 15;
    z = (z * (2 - (t & 255) * z)) & 255;
    z = (z * (2 - (((t & 65535) * z) & 65535))) & 65535;
    z = (z * (2 - t * z % this.DV)) % this.DV;
    return (z > 0) ? this.DV - z : -z
}
K.prototype.convert = by;
K.prototype.revert = bl;
K.prototype.reduce = bV;
K.prototype.mulTo = bz;
K.prototype.sqrTo = ac;

function bm() {
    return new bf(null)
}

function am(b0, b1) {
    if (b0 > 4294967295 || b0 < 1) {
        return bf.ONE
    }
    var bZ = bm()
      , L = bm()
      , bY = b1.convert(this)
      , bX = q(b0) - 1;
    bY.copyTo(bZ);
    while (--bX >= 0) {
        b1.sqrTo(bZ, L);
        if ((b0 & (1 << bX)) > 0) {
            b1.mulTo(L, bY, bZ)
        } else {
            var bW = bZ;
            bZ = L;
            L = bW
        }
    }
    return b1.revert(bZ)
}

function bB() {
    return (this.s < 0) ? this.negate() : this
}

function bv(L, z) {
    var t;
    for (t = this.t - 1; t >= 0; --t) {
        z[t + L] = this[t]
    }
    for (t = L - 1; t >= 0; --t) {
        z[t] = 0
    }
    z.t = this.t + L;
    z.s = this.s
}

function s(b0, bW) {
    var z = b0 % this.DB;
    var t = this.DB - z;
    var bY = (1 << t) - 1;
    var bX = Math.floor(b0 / this.DB), bZ = (this.s << z) & this.DM, L;
    for (L = this.t - 1; L >= 0; --L) {
        bW[L + bX + 1] = (this[L] >> t) | bZ;
        bZ = (this[L] & bY) << z
    }
    for (L = bX - 1; L >= 0; --L) {
        bW[L] = 0
    }
    bW[bX] = bZ;
    bW.t = this.t + bX + 1;
    bW.s = this.s;
    bW.clamp()
}

function a9(b3, b0, bZ) {
    var b9 = b3.abs();
    if (b9.t <= 0) {
        return
    }
    var b1 = this.abs();
    if (b1.t < b9.t) {
        if (b0 != null) {
            b0.fromInt(0)
        }
        if (bZ != null) {
            this.copyTo(bZ)
        }
        return
    }
    if (bZ == null) {
        bZ = bm()
    }
    var bX = bm()
      , z = this.s
      , b2 = b3.s;
    var b8 = this.DB - q(b9[b9.t - 1]);
    if (b8 > 0) {
        b9.lShiftTo(b8, bX);
        b1.lShiftTo(b8, bZ)
    } else {
        b9.copyTo(bX);
        b1.copyTo(bZ)
    }
    var b5 = bX.t;
    var L = bX[b5 - 1];
    if (L == 0) {
        return
    }
    var b4 = L * (1 << this.F1) + ((b5 > 1) ? bX[b5 - 2] >> this.F2 : 0);
    var cc = this.FV / b4
      , cb = (1 << this.F1) / b4
      , ca = 1 << this.F2;
    var b7 = bZ.t
      , b6 = b7 - b5
      , bY = (b0 == null) ? bm() : b0;
    bX.dlShiftTo(b6, bY);
    if (bZ.compareTo(bY) >= 0) {
        bZ[bZ.t++] = 1;
        bZ.subTo(bY, bZ)
    }
    bf.ONE.dlShiftTo(b5, bY);
    bY.subTo(bX, bX);
    while (bX.t < b5) {
        bX[bX.t++] = 0
    }
    while (--b6 >= 0) {
        var bW = (bZ[--b7] == L) ? this.DM : Math.floor(bZ[b7] * cc + (bZ[b7 - 1] + ca) * cb);
        if ((bZ[b7] += bX.am(0, bW, bZ, b6, 0, b5)) < bW) {
            bX.dlShiftTo(b6, bY);
            bZ.subTo(bY, bZ);
            while (bZ[b7] < --bW) {
                bZ.subTo(bY, bZ)
            }
        }
    }
    if (b0 != null) {
        bZ.drShiftTo(b5, b0);
        if (z != b2) {
            bf.ZERO.subTo(b0, b0)
        }
    }
    bZ.t = b5;
    bZ.clamp();
    if (b8 > 0) {
        bZ.rShiftTo(b8, bZ)
    }
    if (z < 0) {
        bf.ZERO.subTo(bZ, bZ)
    }
}
function bN(t) {
    var L = this.s - t.s;
    if (L != 0) {
        return L
    }
    var z = this.t;
    L = z - t.t;
    if (L != 0) {
        return (this.s < 0) ? -L : L
    }
    while (--z >= 0) {
        if ((L = this[z] - t[z]) != 0) {
            return L
        }
    }
    return 0
}

function bi(t) {
    var z = bm();
    z.fromInt(t);
    return z
}

function h(t) {
    this.t = 1;
    this.s = (t < 0) ? -1 : 0;
    if (t > 0) {
        this[0] = t
    } else {
        if (t < -1) {
            this[0] = t + this.DV
        } else {
            this.t = 0
        }
    }
}

function bs(z, bW) {
    var L = 0
      , bX = 0
      , t = Math.min(z.t, this.t);
    while (L < t) {
        bX += this[L] - z[L];
        bW[L++] = bX & this.DM;
        bX >>= this.DB
    }
    if (z.t < this.t) {
        bX -= z.s;
        while (L < this.t) {
            bX += this[L];
            bW[L++] = bX & this.DM;
            bX >>= this.DB
        }
        bX += this.s
    } else {
        bX += this.s;
        while (L < z.t) {
            bX -= z[L];
            bW[L++] = bX & this.DM;
            bX >>= this.DB
        }
        bX -= z.s
    }
    bW.s = (bX < 0) ? -1 : 0;
    if (bX < -1) {
        bW[L++] = this.DV + bX
    } else {
        if (bX > 0) {
            bW[L++] = bX
        }
    }
    bW.t = L;
    bW.clamp()
}

function a5(bX, b2, b3, bW, b0, t) {
    var bZ = b2 & 16383
      , b1 = b2 >> 14;
    while (--t >= 0) {
        var L = this[bX] & 16383;
        var bY = this[bX++] >> 14;
        var z = b1 * L + bY * bZ;
        L = bZ * L + ((z & 16383) << 14) + b3[bW] + b0;
        b0 = (L >> 28) + (z >> 14) + b1 * bY;
        b3[bW++] = L & 268435455
    }
    return b0
}

function d(z) {
    for (var t = this.t - 1; t >= 0; --t) {
        z[t] = this[t]
    }
    z.t = this.t;
    z.s = this.s
}

function a2(L, z) {
    for (var t = L; t < this.t; ++t) {
        z[t - L] = this[t]
    }
    z.t = Math.max(this.t - L, 0);
    z.s = this.s
}

function bT(bZ, bW) {
    bW.s = this.s;
    var bX = Math.floor(bZ / this.DB);
    if (bX >= this.t) {
        bW.t = 0;
        return
    }
    var z = bZ % this.DB;
    var t = this.DB - z;
    var bY = (1 << z) - 1;
    bW[0] = this[bX] >> z;
    for (var L = bX + 1; L < this.t; ++L) {
        bW[L - bX - 1] |= (this[L] & bY) << t;
        bW[L - bX] = this[L] >> z
    }
    if (z > 0) {
        bW[this.t - bX - 1] |= (this.s & bY) << t
    }
    bW.t = this.t - bX;
    bW.clamp()
}

function bJ(z, bW) {
    var t = this.abs()
      , bX = z.abs();
    var L = t.t;
    bW.t = L + bX.t;
    while (--L >= 0) {
        bW[L] = 0
    }
    for (L = 0; L < bX.t; ++L) {
        bW[L + t.t] = t.am(0, bX[L], bW, L, 0, t.t)
    }
    bW.s = 0;
    bW.clamp();
    if (this.s != z.s) {
        bf.ZERO.subTo(bW, bW)
    }
}

function au(L) {
    var t = this.abs();
    var z = L.t = 2 * t.t;
    while (--z >= 0) {
        L[z] = 0
    }
    for (z = 0; z < t.t - 1; ++z) {
        var bW = t.am(z, t[z], L, 2 * z, 0, 1);
        if ((L[z + t.t] += t.am(z + 1, 2 * t[z], L, 2 * z + 1, bW, t.t - z - 1)) >= t.DV) {
            L[z + t.t] -= t.DV;
            L[z + t.t + 1] = 1
        }
    }
    if (L.t > 0) {
        L[L.t - 1] += t.am(z, t[z], L, 2 * z, 0, 1)
    }
    L.s = 0;
    L.clamp()
}

function Y(t) {
    return a.charAt(t)
}

function u(z) {
    if (this.s < 0) {
        return "-" + this.negate().toString(z)
    }
    var L;
    if (z == 16) {
        L = 4
    } else {
        if (z == 8) {
            L = 3
        } else {
            if (z == 2) {
                L = 1
            } else {
                if (z == 32) {
                    L = 5
                } else {
                    if (z == 4) {
                        L = 2
                    } else {
                        return this.toRadix(z)
                    }
                }
            }
        }
    }
    var bX = (1 << L) - 1, b0, t = false, bY = "", bW = this.t;
    var bZ = this.DB - (bW * this.DB) % L;
    if (bW-- > 0) {
        if (bZ < this.DB && (b0 = this[bW] >> bZ) > 0) {
            t = true;
            bY = Y(b0)
        }
        while (bW >= 0) {
            if (bZ < L) {
                b0 = (this[bW] & ((1 << bZ) - 1)) << (L - bZ);
                b0 |= this[--bW] >> (bZ += this.DB - L)
            } else {
                b0 = (this[bW] >> (bZ -= L)) & bX;
                if (bZ <= 0) {
                    bZ += this.DB;
                    --bW
                }
            }
            if (b0 > 0) {
                t = true
            }
            if (t) {
                bY += Y(b0)
            }
        }
    }
    return t ? bY : "0"
}

function bC() {
    var t = bm();
    bf.ZERO.subTo(this, t);
    return t
}

function bh(t) {
    var z = bm();
    this.abs().divRemTo(t, null, z);
    if (this.s < 0 && z.compareTo(bf.ZERO) > 0) {
        t.subTo(z, z)
    }
    return z
}

bf.prototype.DB = bE;
bf.prototype.DM = ((1 << bE) - 1);
bf.prototype.DV = (1 << bE);
var bQ = 52;
bf.prototype.FV = Math.pow(2, bQ);
bf.prototype.F1 = bQ - bE;
bf.prototype.F2 = 2 * bE - bQ;
var a = "0123456789abcdefghijklmnopqrstuvwxyz";
//
bf.prototype.am = a5
bf.prototype.copyTo = d;
bf.prototype.fromInt = h;
bf.prototype.fromString = bI;
bf.prototype.clamp = bA;
bf.prototype.dlShiftTo = bv;
bf.prototype.drShiftTo = a2;
bf.prototype.lShiftTo = s;
bf.prototype.rShiftTo = bT;
bf.prototype.subTo = bs;
bf.prototype.multiplyTo = bJ;
bf.prototype.squareTo = au;
bf.prototype.divRemTo = a9;
bf.prototype.invDigit = ab;
bf.prototype.invDigit = ab;
bf.prototype.isEven = ad;
bf.prototype.exp = am;
bf.prototype.toString = u;
bf.prototype.negate = bC;
bf.prototype.abs = bB;
bf.prototype.compareTo = bN;
bf.prototype.bitLength = bt;
bf.prototype.mod = bh;
bf.prototype.modPowInt = aG;
bf.ZERO = bi(0);
bf.ONE = bi(1);

function w(z, t) {
    return new bf(z,t)
}

function bW(b2, b3, b1, bZ, b0) {
    this.stream = b2;
    this.header = b3;
    this.length = b1;
    this.tag = bZ;
    this.sub = b0
}
bW.prototype.typeName = function() {
    if (this.tag === bY) {
        return "unknown"
    }
    var b1 = this.tag >> 6
      , bZ = (this.tag >> 5) & 1
      , b0 = this.tag & 31;
    switch (b1) {
    case 0:
        switch (b0) {
        case 0:
            return "EOC";
        case 1:
            return "BOOLEAN";
        case 2:
            return "INTEGER";
        case 3:
            return "BIT_STRING";
        case 4:
            return "OCTET_STRING";
        case 5:
            return "NULL";
        case 6:
            return "OBJECT_IDENTIFIER";
        case 7:
            return "ObjectDescriptor";
        case 8:
            return "EXTERNAL";
        case 9:
            return "REAL";
        case 10:
            return "ENUMERATED";
        case 11:
            return "EMBEDDED_PDV";
        case 12:
            return "UTF8String";
        case 16:
            return "SEQUENCE";
        case 17:
            return "SET";
        case 18:
            return "NumericString";
        case 19:
            return "PrintableString";
        case 20:
            return "TeletexString";
        case 21:
            return "VideotexString";
        case 22:
            return "IA5String";
        case 23:
            return "UTCTime";
        case 24:
            return "GeneralizedTime";
        case 25:
            return "GraphicString";
        case 26:
            return "VisibleString";
        case 27:
            return "GeneralString";
        case 28:
            return "UniversalString";
        case 30:
            return "BMPString";
        default:
            return "Universal_" + b0.toString(16)
        }
    case 1:
        return "Application_" + b0.toString(16);
    case 2:
        return "[" + b0 + "]";
    case 3:
        return "Private_" + b0.toString(16)
    }
}
;
bW.prototype.reSeemsASCII = /^[ -~]+$/;
bW.prototype.content = function() {
    if (this.tag === bY) {
        return null
    }
    var b3 = this.tag >> 6
      , b0 = this.tag & 31
      , b2 = this.posContent()
      , bZ = Math.abs(this.length);
    if (b3 !== 0) {
        if (this.sub !== null) {
            return "(" + this.sub.length + " elem)"
        }
        var b1 = this.stream.parseStringISO(b2, b2 + Math.min(bZ, z));
        if (this.reSeemsASCII.test(b1)) {
            return b1.substring(0, 2 * z) + ((b1.length > 2 * z) ? t : "")
        } else {
            return this.stream.parseOctetString(b2, b2 + bZ)
        }
    }
    switch (b0) {
    case 1:
        return (this.stream.get(b2) === 0) ? "false" : "true";
    case 2:
        return this.stream.parseInteger(b2, b2 + bZ);
    case 3:
        return this.sub ? "(" + this.sub.length + " elem)" : this.stream.parseBitString(b2, b2 + bZ);
    case 4:
        return this.sub ? "(" + this.sub.length + " elem)" : this.stream.parseOctetString(b2, b2 + bZ);
    case 6:
        return this.stream.parseOID(b2, b2 + bZ);
    case 16:
    case 17:
        return "(" + this.sub.length + " elem)";
    case 12:
        return this.stream.parseStringUTF(b2, b2 + bZ);
    case 18:
    case 19:
    case 20:
    case 21:
    case 22:
    case 26:
        return this.stream.parseStringISO(b2, b2 + bZ);
    case 30:
        return this.stream.parseStringBMP(b2, b2 + bZ);
    case 23:
    case 24:
        return this.stream.parseTime(b2, b2 + bZ)
    }
    return null
}
;
bW.prototype.toString = function() {
    return this.typeName() + "@" + this.stream.pos + "[header:" + this.header + ",length:" + this.length + ",sub:" + ((this.sub === null) ? "null" : this.sub.length) + "]"
}
;
bW.prototype.print = function(b0) {
    if (b0 === bY) {
        b0 = ""
    }
    document.writeln(b0 + this);
    if (this.sub !== null) {
        b0 += "  ";
        for (var b1 = 0, bZ = this.sub.length; b1 < bZ; ++b1) {
            this.sub[b1].print(b0)
        }
    }
}
;
bW.prototype.toPrettyString = function(b0) {
    if (b0 === bY) {
        b0 = ""
    }
    var b2 = b0 + this.typeName() + " @" + this.stream.pos;
    if (this.length >= 0) {
        b2 += "+"
    }
    b2 += this.length;
    if (this.tag & 32) {
        b2 += " (constructed)"
    } else {
        if (((this.tag == 3) || (this.tag == 4)) && (this.sub !== null)) {
            b2 += " (encapsulates)"
        }
    }
    b2 += "\n";
    if (this.sub !== null) {
        b0 += "  ";
        for (var b1 = 0, bZ = this.sub.length; b1 < bZ; ++b1) {
            b2 += this.sub[b1].toPrettyString(b0)
        }
    }
    return b2
}
;
bW.prototype.toDOM = function() {
    var b0 = L.tag("div", "node");
    b0.asn1 = this;
    var b6 = L.tag("div", "head");
    var b8 = this.typeName().replace(/_/g, " ");
    b6.innerHTML = b8;
    var b4 = this.content();
    if (b4 !== null) {
        b4 = String(b4).replace(/</g, "&lt;");
        var b3 = L.tag("span", "preview");
        b3.appendChild(L.text(b4));
        b6.appendChild(b3)
    }
    b0.appendChild(b6);
    this.node = b0;
    this.head = b6;
    var b7 = L.tag("div", "value");
    b8 = "Offset: " + this.stream.pos + "<br/>";
    b8 += "Length: " + this.header + "+";
    if (this.length >= 0) {
        b8 += this.length
    } else {
        b8 += (-this.length) + " (undefined)"
    }
    if (this.tag & 32) {
        b8 += "<br/>(constructed)"
    } else {
        if (((this.tag == 3) || (this.tag == 4)) && (this.sub !== null)) {
            b8 += "<br/>(encapsulates)"
        }
    }
    if (b4 !== null) {
        b8 += "<br/>Value:<br/><b>" + b4 + "</b>";
        if ((typeof oids === "object") && (this.tag == 6)) {
            var b1 = oids[b4];
            if (b1) {
                if (b1.d) {
                    b8 += "<br/>" + b1.d
                }
                if (b1.c) {
                    b8 += "<br/>" + b1.c
                }
                if (b1.w) {
                    b8 += "<br/>(warning!)"
                }
            }
        }
    }
    b7.innerHTML = b8;
    b0.appendChild(b7);
    var bZ = L.tag("div", "sub");
    if (this.sub !== null) {
        for (var b2 = 0, b5 = this.sub.length; b2 < b5; ++b2) {
            bZ.appendChild(this.sub[b2].toDOM())
        }
    }
    b0.appendChild(bZ);
    b6.onclick = function() {
        b0.className = (b0.className == "node collapsed") ? "node" : "node collapsed"
    }
    ;
    return b0
}
;
bW.prototype.posStart = function() {
    return this.stream.pos
}
;
bW.prototype.posContent = function() {
    return this.stream.pos + this.header
}
;
bW.prototype.posEnd = function() {
    return this.stream.pos + this.header + Math.abs(this.length)
}
;
bW.prototype.fakeHover = function(bZ) {
    this.node.className += " hover";
    if (bZ) {
        this.head.className += " hover"
    }
}
;
bW.prototype.fakeOut = function(b0) {
    var bZ = / ?hover/;
    this.node.className = this.node.className.replace(bZ, "");
    if (b0) {
        this.head.className = this.head.className.replace(bZ, "")
    }
}
;
bW.prototype.toHexDOM_sub = function(b2, b1, b3, b4, bZ) {
    if (b4 >= bZ) {
        return
    }
    var b0 = L.tag("span", b1);
    b0.appendChild(L.text(b3.hexDump(b4, bZ)));
    b2.appendChild(b0)
}
;
bW.prototype.toHexDOM = function(b0) {
    var b3 = L.tag("span", "hex");
    if (b0 === bY) {
        b0 = b3
    }
    this.head.hexNode = b3;
    this.head.onmouseover = function() {
        this.hexNode.className = "hexCurrent"
    }
    ;
    this.head.onmouseout = function() {
        this.hexNode.className = "hex"
    }
    ;
    b3.asn1 = this;
    b3.onmouseover = function() {
        var b5 = !b0.selected;
        if (b5) {
            b0.selected = this.asn1;
            this.className = "hexCurrent"
        }
        this.asn1.fakeHover(b5)
    }
    ;
    b3.onmouseout = function() {
        var b5 = (b0.selected == this.asn1);
        this.asn1.fakeOut(b5);
        if (b5) {
            b0.selected = null;
            this.className = "hex"
        }
    }
    ;
    this.toHexDOM_sub(b3, "tag", this.stream, this.posStart(), this.posStart() + 1);
    this.toHexDOM_sub(b3, (this.length >= 0) ? "dlen" : "ulen", this.stream, this.posStart() + 1, this.posContent());
    if (this.sub === null) {
        b3.appendChild(L.text(this.stream.hexDump(this.posContent(), this.posEnd())))
    } else {
        if (this.sub.length > 0) {
            var b4 = this.sub[0];
            var b2 = this.sub[this.sub.length - 1];
            this.toHexDOM_sub(b3, "intro", this.stream, this.posContent(), b4.posStart());
            for (var b1 = 0, bZ = this.sub.length; b1 < bZ; ++b1) {
                b3.appendChild(this.sub[b1].toHexDOM(b0))
            }
            this.toHexDOM_sub(b3, "outro", this.stream, b2.posEnd(), this.posEnd())
        }
    }
    return b3
}
;
bW.prototype.toHexString = function(bZ) {
    return this.stream.hexDump(this.posStart(), this.posEnd(), true)
}
;
bW.decodeLength = function(b2) {
    var b0 = b2.get()
      , bZ = b0 & 127;
    if (bZ == b0) {
        return bZ
    }
    if (bZ > 3) {
        throw "Length over 24 bits not supported at position " + (b2.pos - 1)
    }
    if (bZ === 0) {
        return -1
    }
    b0 = 0;
    for (var b1 = 0; b1 < bZ; ++b1) {
        b0 = (b0 << 8) | b2.get()
    }
    return b0
}
;
bW.hasContent = function(b0, bZ, b5) {
    if (b0 & 32) {
        return true
    }
    if ((b0 < 3) || (b0 > 4)) {
        return false
    }
    var b4 = new bX(b5);
    if (b0 == 3) {
        b4.get()
    }
    var b3 = b4.get();
    if ((b3 >> 6) & 1) {
        return false
    }
    // try {
    var b2 = bW.decodeLength(b4);
    return ((b4.pos - b5.pos) + b2 == bZ)
    // } catch (b1) {
    //     return false
    // }
}
;
bW.decode = function(b6) {
    if (!(b6 instanceof bX)) {
        b6 = new bX(b6,0)
    }
    var b5 = new bX(b6)
      , b8 = b6.get()
      , b3 = bW.decodeLength(b6)
      , b2 = b6.pos - b5.pos
      , bZ = null;
    if (bW.hasContent(b8, b3, b6)) {
        var b0 = b6.pos;
        if (b8 == 3) {
            b6.get()
        }
        bZ = [];
        if (b3 >= 0) {
            var b1 = b0 + b3;
            while (b6.pos < b1) {
                bZ[bZ.length] = bW.decode(b6)
            }
            if (b6.pos != b1) {
                throw "Content size is not correct for container starting at offset " + b0
            }
        } else {
            try {
                for (; ; ) {
                    var b7 = bW.decode(b6);
                    if (b7.tag === 0) {
                        break
                    }
                    bZ[bZ.length] = b7
                }
                b3 = b0 - b6.pos
            } catch (b4) {
                throw "Exception while decoding undefined length content: " + b4
            }
        }
    } else {
        b6.pos += b3
    }
    return new bW(b5,b2,b3,b8,bZ)
}
;
bW.test = function() {
    var b4 = [{
        value: [39],
        expected: 39
    }, {
        value: [129, 201],
        expected: 201
    }, {
        value: [131, 254, 220, 186],
        expected: 16702650
    }];
    for (var b1 = 0, bZ = b4.length; b1 < bZ; ++b1) {
        var b3 = 0
          , b2 = new bX(b4[b1].value,0)
          , b0 = bW.decodeLength(b2);
        if (b0 != b4[b1].expected) {
            document.write("In test[" + b1 + "] expected " + b4[b1].expected + " got " + b0 + "\n")
        }
    }
}
;
ASN1 = bW

ASN1.prototype.getHexStringValue = function() {
    var t = this.toHexString();
    var L = this.header * 2;
    var z = this.length * 2;
    return t.substr(L, z)
}


function bX(bZ, b0) {
    if (bZ instanceof bX) {
        this.enc = bZ.enc;
        this.pos = bZ.pos
    } else {
        this.enc = bZ;
        this.pos = b0
    }
}
bX.prototype.get = function(bZ) {
    if (bZ === bY) {
        bZ = this.pos++
    }
    if (bZ >= this.enc.length) {
        throw "Requesting byte offset " + bZ + " on a stream of length " + this.enc.length
    }
    return this.enc[bZ]
}
;
bX.prototype.hexDigits = "0123456789ABCDEF";
bX.prototype.hexByte = function(bZ) {
    return this.hexDigits.charAt((bZ >> 4) & 15) + this.hexDigits.charAt(bZ & 15)
}
;
bX.prototype.hexDump = function(b3, bZ, b0) {
    var b2 = "";
    for (var b1 = b3; b1 < bZ; ++b1) {
        b2 += this.hexByte(this.get(b1));
        if (b0 !== true) {
            switch (b1 & 15) {
            case 7:
                b2 += "  ";
                break;
            case 15:
                b2 += "\n";
                break;
            default:
                b2 += " "
            }
        }
    }
    return b2
}
;
bX.prototype.parseStringISO = function(b2, bZ) {
    var b1 = "";
    for (var b0 = b2; b0 < bZ; ++b0) {
        b1 += String.fromCharCode(this.get(b0))
    }
    return b1
}
;
bX.prototype.parseStringUTF = function(b3, bZ) {
    var b1 = "";
    for (var b0 = b3; b0 < bZ; ) {
        var b2 = this.get(b0++);
        if (b2 < 128) {
            b1 += String.fromCharCode(b2)
        } else {
            if ((b2 > 191) && (b2 < 224)) {
                b1 += String.fromCharCode(((b2 & 31) << 6) | (this.get(b0++) & 63))
            } else {
                b1 += String.fromCharCode(((b2 & 15) << 12) | ((this.get(b0++) & 63) << 6) | (this.get(b0++) & 63))
            }
        }
    }
    return b1
}
;
bX.prototype.parseStringBMP = function(b4, b0) {
    var b3 = "";
    for (var b2 = b4; b2 < b0; b2 += 2) {
        var bZ = this.get(b2);
        var b1 = this.get(b2 + 1);
        b3 += String.fromCharCode((bZ << 8) + b1)
    }
    return b3
}
;
bX.prototype.reTime = /^((?:1[89]|2\d)?\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])([01]\d|2[0-3])(?:([0-5]\d)(?:([0-5]\d)(?:[.,](\d{1,3}))?)?)?(Z|[-+](?:[0]\d|1[0-2])([0-5]\d)?)?$/;
bX.prototype.parseTime = function(b2, b0) {
    var b1 = this.parseStringISO(b2, b0)
      , bZ = this.reTime.exec(b1);
    if (!bZ) {
        return "Unrecognized time: " + b1
    }
    b1 = bZ[1] + "-" + bZ[2] + "-" + bZ[3] + " " + bZ[4];
    if (bZ[5]) {
        b1 += ":" + bZ[5];
        if (bZ[6]) {
            b1 += ":" + bZ[6];
            if (bZ[7]) {
                b1 += "." + bZ[7]
            }
        }
    }
    if (bZ[8]) {
        b1 += " UTC";
        if (bZ[8] != "Z") {
            b1 += bZ[8];
            if (bZ[9]) {
                b1 += ":" + bZ[9]
            }
        }
    }
    return b1
}
;
bX.prototype.parseInteger = function(b4, b0) {
    var bZ = b0 - b4;
    if (bZ > 4) {
        bZ <<= 3;
        var b2 = this.get(b4);
        if (b2 === 0) {
            bZ -= 8
        } else {
            while (b2 < 128) {
                b2 <<= 1;
                --bZ
            }
        }
        return "(" + bZ + " bit)"
    }
    var b3 = 0;
    for (var b1 = b4; b1 < b0; ++b1) {
        b3 = (b3 << 8) | this.get(b1)
    }
    return b3
}
;
bX.prototype.parseBitString = function(bZ, b0) {
    var b4 = this.get(bZ)
      , b2 = ((b0 - bZ - 1) << 3) - b4
      , b7 = "(" + b2 + " bit)";
    if (b2 <= 20) {
        var b6 = b4;
        b7 += " ";
        for (var b3 = b0 - 1; b3 > bZ; --b3) {
            var b5 = this.get(b3);
            for (var b1 = b6; b1 < 8; ++b1) {
                b7 += (b5 >> b1) & 1 ? "1" : "0"
            }
            b6 = 0
        }
    }
    return b7
}
;
bX.prototype.parseOctetString = function(b3, b0) {
    var bZ = b0 - b3
      , b2 = "(" + bZ + " byte) ";
    if (bZ > z) {
        b0 = b3 + z
    }
    for (var b1 = b3; b1 < b0; ++b1) {
        b2 += this.hexByte(this.get(b1))
    }
    if (bZ > z) {
        b2 += t
    }
    return b2
}
;
bX.prototype.parseOID = function(b6, b0) {
    var b3 = ""
      , b5 = 0
      , b4 = 0;
    for (var b2 = b6; b2 < b0; ++b2) {
        var b1 = this.get(b2);
        b5 = (b5 << 7) | (b1 & 127);
        b4 += 7;
        if (!(b1 & 128)) {
            if (b3 === "") {
                var bZ = b5 < 80 ? b5 < 40 ? 0 : 1 : 2;
                b3 = bZ + "." + (b5 - bZ * 40)
            } else {
                b3 += "." + ((b4 >= 31) ? "bigint" : b5)
            }
            b5 = b4 = 0
        }
    }
    return b3
}


var t = {}, L, z;
t.decode = function(bW) {
    var bZ;
    if (L === z) {
        var bY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
          , b3 = "= \f\n\r\t\u00A0\u2028\u2029";
        L = [];
        for (bZ = 0; bZ < 64; ++bZ) {
            L[bY.charAt(bZ)] = bZ
        }
        for (bZ = 0; bZ < b3.length; ++bZ) {
            L[b3.charAt(bZ)] = -1
        }
    }
    var bX = [];
    var b0 = 0
      , b2 = 0;
    for (bZ = 0; bZ < bW.length; ++bZ) {
        var b1 = bW.charAt(bZ);
        if (b1 == "=") {
            break
        }
        b1 = L[b1];
        if (b1 == -1) {
            continue
        }
        if (b1 === z) {
            throw "Illegal character at offset " + bZ
        }
        b0 |= b1;
        if (++b2 >= 4) {
            bX[bX.length] = (b0 >> 16);
            bX[bX.length] = (b0 >> 8) & 255;
            bX[bX.length] = b0 & 255;
            b0 = 0;
            b2 = 0
        } else {
            b0 <<= 6
        }
    }
    switch (b2) {
    case 1:
        throw "Base64 encoding incomplete: at least 2 bits missing";
    case 2:
        bX[bX.length] = (b0 >> 10);
        break;
    case 3:
        bX[bX.length] = (b0 >> 16);
        bX[bX.length] = (b0 >> 8) & 255;
        break
    }
    return bX
}
t.re = /-----BEGIN [^-]+-----([A-Za-z0-9+\/=\s]+)-----END [^-]+-----|begin-base64[^\n]+\n([A-Za-z0-9+\/=\s]+)====/;
t.unarmor = function(bX) {
    var bW = t.re.exec(bX);
    if (bW) {
        if (bW[1]) {
            bX = bW[1]
        } else {
            if (bW[2]) {
                bX = bW[2]
            } else {
                throw "RegExp out of sync"
            }
        }
    }
    return t.decode(bX)
}
;
Base64 = t


function A() {
    this.n = null;
    this.e = 0;
    this.d = null;
    this.p = null;
    this.q = null;
    this.dmp1 = null;
    this.dmq1 = null;
    this.coeff = null
}

function aG(L, t) {
    var bW;
    if (L < 256 || t.isEven()) {
        bW = new aT(t)
    } else {
        bW = new K(t)
    }
    return this.exp(L, bW)
}

function an(z, t) {
    if (z != null && t != null && z.length > 0 && t.length > 0) {
        this.n = w(z, 16);
        this.e = parseInt(t, 16)
    } else {
        console.error("Invalid RSA public key")
    }
}
function bq(t) {
    return t.modPowInt(this.e, this.n)
}
function al(L) {
    var t = bD(L, (this.n.bitLength() + 7) >> 3);
    if (t == null) {
        return null
    }
    var bW = this.doPublic(t);
    if (bW == null) {
        return null
    }
    var z = bW.toString(16);
    if ((z.length & 1) == 0) {
        return z
    } else {
        return "0" + z
    }
}
A.prototype.doPublic = bq;
A.prototype.setPublic = an;
A.prototype.encrypt = al;
A.prototype.parseKey = function(b1) {
    // try {
    var b6 = 0;
    var bW = 0;
    var t = /^\s*(?:[0-9A-Fa-f][0-9A-Fa-f]\s*)+$/;
    var b5 = t.test(b1) ? Hex.decode(b1) : Base64.unarmor(b1);
    var bX = ASN1.decode(b5);
    if (bX.sub.length === 3) {
        bX = bX.sub[2].sub[0]
    }
    if (bX.sub.length === 9) {
        b6 = bX.sub[1].getHexStringValue();
        this.n = w(b6, 16);
        bW = bX.sub[2].getHexStringValue();
        this.e = parseInt(bW, 16);
        var z = bX.sub[3].getHexStringValue();
        this.d = w(z, 16);
        var b0 = bX.sub[4].getHexStringValue();
        this.p = w(b0, 16);
        var bZ = bX.sub[5].getHexStringValue();
        this.q = w(bZ, 16);
        var b3 = bX.sub[6].getHexStringValue();
        this.dmp1 = w(b3, 16);
        var b2 = bX.sub[7].getHexStringValue();
        this.dmq1 = w(b2, 16);
        var L = bX.sub[8].getHexStringValue();
        this.coeff = w(L, 16)
    } else {
        if (bX.sub.length === 2) {
            var b7 = bX.sub[1];
            var bY = b7.sub[0];
            b6 = bY.sub[0].getHexStringValue();
            this.n = w(b6, 16);
            bW = bY.sub[1].getHexStringValue();
            this.e = parseInt(bW, 16)
        } else {
            return false
        }
    }
    return true
    // } catch (b4) {
    //     return false
    // }
}
;
A.prototype.getPrivateBaseKey = function() {
    var z = {
        array: [new KJUR.asn1.DERInteger({
            "int": 0
        }), new KJUR.asn1.DERInteger({
            bigint: this.n
        }), new KJUR.asn1.DERInteger({
            "int": this.e
        }), new KJUR.asn1.DERInteger({
            bigint: this.d
        }), new KJUR.asn1.DERInteger({
            bigint: this.p
        }), new KJUR.asn1.DERInteger({
            bigint: this.q
        }), new KJUR.asn1.DERInteger({
            bigint: this.dmp1
        }), new KJUR.asn1.DERInteger({
            bigint: this.dmq1
        }), new KJUR.asn1.DERInteger({
            bigint: this.coeff
        })]
    };
    var t = new KJUR.asn1.DERSequence(z);
    return t.getEncodedHex()
}
;
A.prototype.getPrivateBaseKeyB64 = function() {
    return ae(this.getPrivateBaseKey())
}
;
A.prototype.getPublicBaseKey = function() {
    var L = {
        array: [new KJUR.asn1.DERObjectIdentifier({
            oid: "1.2.840.113549.1.1.1"
        }), new KJUR.asn1.DERNull()]
    };
    var t = new KJUR.asn1.DERSequence(L);
    L = {
        array: [new KJUR.asn1.DERInteger({
            bigint: this.n
        }), new KJUR.asn1.DERInteger({
            "int": this.e
        })]
    };
    var bX = new KJUR.asn1.DERSequence(L);
    L = {
        hex: "00" + bX.getEncodedHex()
    };
    var bW = new KJUR.asn1.DERBitString(L);
    L = {
        array: [t, bW]
    };
    var z = new KJUR.asn1.DERSequence(L);
    return z.getEncodedHex()
}
;
A.prototype.getPublicBaseKeyB64 = function() {
    return ae(this.getPublicBaseKey())
}
;
A.prototype.wordwrap = function(L, t) {
    t = t || 64;
    if (!L) {
        return L
    }
    var z = "(.{1," + t + "})( +|$\n?)|(.{1," + t + "})";
    return L.match(RegExp(z, "g")).join("\n")
}
;
A.prototype.getPrivateKey = function() {
    var t = "-----BEGIN RSA PRIVATE KEY-----\n";
    t += this.wordwrap(this.getPrivateBaseKeyB64()) + "\n";
    t += "-----END RSA PRIVATE KEY-----";
    return t
}
;
A.prototype.getPublicKey = function() {
    var t = "-----BEGIN PUBLIC KEY-----\n";
    t += this.wordwrap(this.getPublicBaseKeyB64()) + "\n";
    t += "-----END PUBLIC KEY-----";
    return t
}
;
A.prototype.hasPublicKeyProperty = function(t) {
    t = t || {};
    return (t.hasOwnProperty("n") && t.hasOwnProperty("e"))
}
;
A.prototype.hasPrivateKeyProperty = function(t) {
    t = t || {};
    return (t.hasOwnProperty("n") && t.hasOwnProperty("e") && t.hasOwnProperty("d") && t.hasOwnProperty("p") && t.hasOwnProperty("q") && t.hasOwnProperty("dmp1") && t.hasOwnProperty("dmq1") && t.hasOwnProperty("coeff"))
}
;
A.prototype.parsePropertiesFrom = function(t) {
    this.n = t.n;
    this.e = t.e;
    if (t.hasOwnProperty("d")) {
        this.d = t.d;
        this.p = t.p;
        this.q = t.q;
        this.dmp1 = t.dmp1;
        this.dmq1 = t.dmq1;
        this.coeff = t.coeff
    }
}

function G() {}
G.prototype.nextBytes = aY;

function aY(z) {
    var t;
    for (t = 0; t < z.length; ++t) {
        z[t] = bb()
    }
}


var j
function P() {
    return new bp()
}

function be() {
    var z;
    this.i = (this.i + 1) & 255;
    this.j = (this.j + this.S[this.i]) & 255;
    z = this.S[this.i];
    this.S[this.i] = this.S[this.j];
    this.S[this.j] = z;
    return this.S[(z + this.S[this.i]) & 255]
}

function bp() {
    this.i = 0;
    this.j = 0;
    this.S = new Array()
}

bp.prototype.init = af
bp.prototype.next = be

function af(bX) {
    var bW, z, L;
    for (bW = 0; bW < 256; ++bW) {
        this.S[bW] = bW
    }
    z = 0;
    for (bW = 0; bW < 256; ++bW) {
        z = (z + this.S[bW] + bX[bW % bX.length]) & 255;
        L = this.S[bW];
        this.S[bW] = this.S[z];
        this.S[z] = L
    }
    this.i = 0;
    this.j = 0
}

var C = 256,y = 256
l = new Array();
C = 0;
var ba;
var a8 = new Uint32Array(256);
getRandomValues(a8);
for (ba = 0; ba < a8.length; ++ba) {
    l[C++] = a8[ba] & 255
}


function bb() {
    if (j == null) {
        j = P();
        while (C < y) {
            var t = Math.floor(65536 * Math.random());
            l[C++] = t & 255
        }
        j.init(l);
        for (C = 0; C < l.length; ++C) {
            l[C] = 0
        }
        C = 0
    }
    return j.next()
}

function bD(bW, bZ) {

    if (bZ < bW.length + 11) {
        console.error("Message too long for RSA");
        return null
    }
    var bY = new Array();
    var L = bW.length - 1;
    while (L >= 0 && bZ > 0) {
        var bX = bW.charCodeAt(L--);
        if (bX < 128) {
            bY[--bZ] = bX
        } else {
            if ((bX > 127) && (bX < 2048)) {
                bY[--bZ] = (bX & 63) | 128;
                bY[--bZ] = (bX >> 6) | 192
            } else {
                bY[--bZ] = (bX & 63) | 128;
                bY[--bZ] = ((bX >> 6) & 63) | 128;
                bY[--bZ] = (bX >> 12) | 224
            }
        }
    }
    bY[--bZ] = 0;
    var z = new G();
    var t = new Array();
    while (bZ > 2) {
        t[0] = 0;
        while (t[0] == 0) {
            z.nextBytes(t)
        }
        bY[--bZ] = t[0]
    }
    bY[--bZ] = 2;
    bY[--bZ] = 0;
    return new bf(bY)
}


var bx = function(t) {
    A.call(this);
    if (t) {
        if (typeof t === "string") {
            this.parseKey(t)
        } else {
            if (this.hasPrivateKeyProperty(t) || this.hasPublicKeyProperty(t)) {
                this.parsePropertiesFrom(t)
            }
        }
    }
};
bx.prototype = new A();
bx.prototype.constructor = bx;




var a3 = function(t) {
    t = t || {};
    this.default_key_size = parseInt(t.default_key_size) || 1024;
    this.default_public_exponent = t.default_public_exponent || "010001";
    this.log = t.log || false;
    this.key = null
};
a3.prototype.setKey = function(t) {
    if (this.log && this.key) {
        console.warn("A key was already set, overriding existing.")
    }
    this.key = new bx(t)
}
;
a3.prototype.setPrivateKey = function(t) {
    this.setKey(t)
}
;
a3.prototype.setPublicKey = function(t) {
    this.setKey(t)
}
;
a3.prototype.decrypt = function(t) {
    // try {
    return this.getKey().decrypt(aW(t))
    // } catch (z) {
    //     return false
    // }
}
;
a3.prototype.encrypt = function(t) {
    // try {
    return ae(this.getKey().encrypt(t))
    // } catch (z) {
    //     return false
    // }
}
;
a3.prototype.getKey = function(t) {
    if (!this.key) {
        this.key = new bx();
        if (t && {}.toString.call(t) === "[object Function]") {
            this.key.generateAsync(this.default_key_size, this.default_public_exponent, t);
            return
        }
        this.key.generate(this.default_key_size, this.default_public_exponent)
    }
    return this.key
}
;
a3.prototype.getPrivateKey = function() {
    return this.getKey().getPrivateKey()
}
;
a3.prototype.getPrivateKeyB64 = function() {
    return this.getKey().getPrivateBaseKeyB64()
}
;
a3.prototype.getPublicKey = function() {
    return this.getKey().getPublicKey()
}
;
a3.prototype.getPublicKeyB64 = function() {
    return this.getKey().getPublicBaseKeyB64()
}
;
a3.version = "2.3.1";
JSEncrypt = a3


function ae(L) {
    var z;
    var bW;
    var t = "";
    for (z = 0; z + 3 <= L.length; z += 3) {
        bW = parseInt(L.substring(z, z + 3), 16);
        t += a4.charAt(bW >> 6) + a4.charAt(bW & 63)
    }
    if (z + 1 == L.length) {
        bW = parseInt(L.substring(z, z + 1), 16);
        t += a4.charAt(bW << 2)
    } else {
        if (z + 2 == L.length) {
            bW = parseInt(L.substring(z, z + 2), 16);
            t += a4.charAt(bW >> 2) + a4.charAt((bW & 3) << 4)
        }
    }
    while ((t.length & 3) > 0) {
        t += "="
    }
    return t
}


function getEntryptPwd(pwd, pubKey){
    // var pubKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5laljaN9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7PAzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQq+CA6agNkqly2H4j6wIDAQAB";
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(pubKey);
    return encrypt.encrypt(pwd);
}
// console.log(getEntryptPwd("Beidemei@2021."))