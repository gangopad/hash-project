import java.time.Duration;
import java.time.Instant;

public class md5Test {
    public static void main(String [] args) {
        AdvSet set = new AdvSet();
        MD5 md5 = new MD5();

        set.randomlySeedSet(1000000);

//        for (byte[] e : set) {
//            System.out.println(md5.toHexString(md5.computeMD5(e)));
//        }

        Instant start = Instant.now();
        //md5.computeTransxAndMD5(set);
        md5.computeMD5(set);
        Instant end = Instant.now();

        long timeElapsed = Duration.between(start, end).toMillis();
        System.out.println(timeElapsed);
    }
}
