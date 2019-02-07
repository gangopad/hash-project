import com.sun.deploy.util.ArrayUtil;
import com.sun.tools.javac.util.ArrayUtils;

import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class md5Test {

    static int NUM_EXAMPLES = 2000000;

    public static void main(String [] args) {
        AdvSet set = new AdvSet();
        MD5 md5 = new MD5();
        Random rand = new Random();

        String hash1 = "212a6799fc002b7537a72b4b51e7df5170340b7e7effa11854841e03bcbb0612552d3406021e946097b2727d14d312140a8568a4f2cc7bfd966b6c18abfae3fb33b1803e9eba3ae31083f143179e11c3f576e8357b17c83ce8c82de7ccea9cfeadbf7b03469547e63a8b5d0aa2341afeeb740edb6ea13bbeb0beda787ac1a8f3";
        String hash2 = "212a6799fc002b7537a72b4b51e7df5170340bfe7effa11854841e03bcbb0612552d3406021e946097b2727d145313140a8568a4f2cc7bfd966b6c98abfae3fb33b1803e9eba3ae31083f143179e11c3f576e8b57b17c83ce8c82de7ccea9cfeadbf7b03469547e63a8b5d0aa2b419feeb740edb6ea13bbeb0bedaf87ac1a8f3";

        byte[] array1 = new BigInteger(hash1, 16).toByteArray();
        byte[] array2 = new BigInteger(hash2, 16).toByteArray();

        byte[] prefix = Arrays.copyOfRange(array1, 0, array1.length/2);

        //set.seedSetByteArray(array1);
        //set.seedSetByteArray(array2);

        byte[] suffix = new byte[64];

        for (byte[] e : set) {
            md5.toHexString(md5.computeMD5(e));
        }

        //Instant start = Instant.now();

        for (int i = 0; i < NUM_EXAMPLES; i++) {
            rand.nextBytes(suffix);
            md5.toHexString(md5.computeMD5(appendByteArrays(prefix, suffix)));
        }

        //Instant end = Instant.now();

        //long timeElapsed = Duration.between(start, end).toMillis();
        //System.out.println(timeElapsed);
    }

    public static byte[] appendByteArrays(byte[] prefix, byte[] suffix) {
        byte[] combined = new byte[prefix.length + suffix.length];
        for (int i = 0; i < prefix.length; i++) {
            combined[i] = prefix[i];
        }
        for (int j = prefix.length; j < combined.length; j++) {
            combined[j] = suffix[j - prefix.length];
        }
        return combined;
    }
}
