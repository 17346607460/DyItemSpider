//
//
//
var result;
function callDYFun(bArr) { //定义导出函数
    Java.perform(function () {
        console.log("bArr:",bArr);
        var Base64 = Java.use("android.util.Base64")
        var NativeLib = Java.use("com.yuanrenxue.challenge.two.NativeLib");
        var str = Java.use("java.lang.String");  // "java.lang.String"字符串  Java.use("java.lang.String")字符串对象， 可以使用字符串的第三方方法
        var res = Base64.encodeToString(str.$new(NativeLib.$new().encrypt(bArr, "1663319697357")));  // $new获取实例  OooO方法实例， ss类实例
        result = str.valueOf(res)  // 获取对象的值
        console.log("result:",result);
    });
    return result;//返回值给python
}
rpc.exports = {
    callsecretfunctionedy: callDYFun,
};

// function bin2String(array) {
//     return String.fromCharCode.apply(String, array);
// }
//
// var bit=[112,-83,53,82,31,-63,26,0,35,-9,19,14,80,-86,38,50,-113,-30,70,125,-15,35,81,89,-61,127,35,111,-85,77,-87,3,-7,-117,-95,-47,-12,116,64,70,96,53,37,-46,-35,-10,113];
// var tostring=bin2String(
//     ['112','-83','53','82','31','-63','26','0','35','-9','19','14','80','-86','38','50','-113','-30','70','125','-15','35','81','89','-61','127','35','111','-85','77','-87','3','-7','-117','-95','-47','-12','116','64','70','96','53','37','-46','-35','-10','113']
// ); // "hello word" co
//
// console.log(tostring)
//
// a = {
//     stringToBytes: function (str) {
//
//         var ch, st, re = [];
//         for (var i = 0; i < str.length; i++) {
//             ch = str.charCodeAt(i);  // get char
//             st = [];                 // set up "stack"
//
//             do {
//                 st.push(ch & 0xFF);  // push byte to stack
//                 ch = ch >> 8;          // shift value down by 1 byte
//             }
//
//             while (ch);
//             // add stack contents to result
//             // done because chars have "wrong" endianness
//             re = re.concat(st.reverse());
//         }
//         // return an array of bytes
//         return re;
//     }
// }
//
// var str   = '2:1663312708128'
// var bytes = []
//     bytes = a.stringToBytes(str)
//
// console.log(bytes)
