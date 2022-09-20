var result;
function callDYFun(bArr) { //定义导出函数
    Java.perform(function () {
        console.log("bArr:",bArr);
        var ss = Java.use('OooO0o.OooOO0O.OooO00o.OooOo0.OooO00o');  // 类的对象
        var str = Java.use("java.lang.String");  // "java.lang.String"字符串  Java.use("java.lang.String")字符串对象， 可以使用字符串的第三方方法
        var res = str.$new(ss.$new().OooO(bArr));  // $new获取实例  OooO方法实例， ss类实例
        result = str.valueOf(res)  // 获取对象的值
        console.log("result:",result);
    });
    return result;//返回值给python
}
rpc.exports = {
    callsecretfunctionedy: callDYFun,
};