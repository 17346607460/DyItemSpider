var str = "page=11661224934856"
const utf8 = [];
for (let ii = 0; ii < str.length; ii++) {
    let charCode = str.charCodeAt(ii);
    if (charCode < 0x80) utf8.push(charCode);
    else if (charCode < 0x800) {
        utf8.push(0xc0 | (charCode >> 6), 0x80 | (charCode & 0x3f));
    } else if (charCode < 0xd800 || charCode >= 0xe000) {
        utf8.push(0xe0 | (charCode >> 12), 0x80 | ((charCode >> 6) & 0x3f), 0x80 | (charCode & 0x3f));
    } else {
        ii++;
        // Surrogate pair:
        // UTF-16 encodes 0x10000-0x10FFFF by subtracting 0x10000 and
        // splitting the 20 bits of 0x0-0xFFFFF into two halves
        charCode = 0x10000 + (((charCode & 0x3ff) << 10) | (str.charCodeAt(ii) & 0x3ff));
        utf8.push(
            0xf0 | (charCode >> 18),
            0x80 | ((charCode >> 12) & 0x3f),
            0x80 | ((charCode >> 6) & 0x3f),
            0x80 | (charCode & 0x3f),
        );
    }
}
//兼容汉字，ASCII码表最大的值为127，大于127的值为特殊字符
for (let jj = 0; jj < utf8.length; jj++) {
    var code = utf8[jj];
    if (code > 127) {
        utf8[jj] = code - 256;
    }
}

var length = utf8.length * 8;
// ArrayList<Integer> arrayList = new ArrayList<>();
// for (byte b : bArr) {
//     arrayList.add(Integer.valueOf(b));
// }
// arrayList.add(128);
// while (((arrayList.size() * 8) + 64) % 512 != 0) {
//     arrayList.add(0);
// }
// for (int i = 0; i < 8; i++) {
//     arrayList.add(Integer.valueOf((int) ((((long) length) >>> (i * 8)) & 255)));
// }
// return arrayList;


console.log(length)