public class md5Test {
    public static void main(String [] args) {
        AdvSet set = new AdvSet();
        MD5 md5 = new MD5();

        set.randomlySeedSet(10);

        for (byte[] e : set) {
            System.out.println(md5.toHexString(md5.computeMD5(e)));
        }
    }
}
