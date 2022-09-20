import frida, sys


# hook 一般函数

def on_message(message, data):
    if message['type'] == 'send':
        print("[* ] {0}".format(message['payload']))
    else:
        print(message)

# NativeLib.encrypt(String.format(getResources().getString(R$string.challenge_two_data_format), Integer.valueOf(this.f2036OooO0oo), Long.valueOf(currentTimeMillis)).getBytes(StandardCharsets.UTF_8), currentTimeMillis);

jscode_hook = '''
Java.perform(
    function(){
        console.log("1、start hook");
        var Base64 = Java.use("android.util.Base64")
        var ChallengeTwoFragment = Java.use("com.yuanrenxue.challenge.fragment.challenge.ChallengeTwoFragment");
        var NativeLib = Java.use("com.yuanrenxue.challenge.two.NativeLib");
        console.log("2、find class");
        NativeLib.encrypt.implementation = function (a, b){
            var ch, st, re = [], str = '1:1663319697357';
            for (var i = 0; i < str.length; i++) {
                ch = str.charCodeAt(i);  // get char
                st = [];                 // set up "stack"
    
                do {
                    st.push(ch & 0xFF);  // push byte to stack
                    ch = ch >> 8;          // shift value down by 1 byte
                }
    
                while (ch);
                // add stack contents to result
                // done because chars have "wrong" endianness
                re = re.concat(st.reverse());
            }
            // return an array of bytes
            console.log("计算参数a:" + re);
            console.log("计算参数a:" + b);
            var res = this.encrypt(re, b);
            console.log(Base64.encodeToString(res, 10))
            return res
        }
    }
)'''

process = frida.get_usb_device(timeout=1000).attach('com.yuanrenxue.challenge')
script = process.create_script(jscode_hook)
script.on('message', on_message)
print('[* ] Hook Start Running')
script.load()
sys.stdin.read()