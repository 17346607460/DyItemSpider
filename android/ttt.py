import codecs
import frida
import os

def adbforward():
    os.system("adb forward tcp:27042 tcp:27042")
    os.system("adb forward tcp:27043 tcp:27043")

hook_code = '''
rpc.exports = {
    // 函数名gethello
    gethello: function(str){
        send('heelo');
        Java.perform(function(){

            //拿到context上下文
            var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
            var context = currentApplication.getApplicationContext();

            // use 加载的类路径
            var AuthUtils = Java.use('com.coolapk.market.util.AuthUtils');
            //f = tt.$new();
            var sig = AuthUtils.getAS(context, str);  // context，str组要自己组装
            send(sig);
        }
    )
    }
};
'''

def on_message(message, data):
    if message['type'] == 'send':
        print(message['payload'])
    elif message['type'] == 'error':
        print(message['stack'])

process = frida.get_usb_device().attach('com.coolapk.market')
script = process.create_script(hook_code)
script.on('message', on_message)
script.load()

script.exports.gethello('edc38cb9-c72d-3bc4-8e82-6fd9212d77a0')

