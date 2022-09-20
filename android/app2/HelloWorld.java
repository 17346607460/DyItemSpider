public class NativeLib {
    static {
        System.loadLibrary("two");
    }

    public static native byte[] encrypt(byte[] bArr, long j);

    public native String stringFromJNI();
}

public class HelloWorld{
	public static void main (String[] args){
            System.out.println(NativeLib.encrypt("1:1663312708128", "1663312708128"));
	}
}