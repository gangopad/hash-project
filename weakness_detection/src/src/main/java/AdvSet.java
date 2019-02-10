import java.util.HashSet;
import java.util.Random;

public class AdvSet extends HashSet<byte[]> {

    int INPUT_BITE_SIZE = 1024;

    /*
     * @param number of items to seed set with
     * Adds random 1024 bit strings to set
     */
    public void randomlySeedSet(int size) {
        for (int i = 0; i < size; i++)
        {
            Random rand = new Random();
            byte[] ranBytes = new byte[INPUT_BITE_SIZE];
            rand.nextBytes(ranBytes);
            this.add(ranBytes);
        }
    }

    /*
     * @param Seed set
     * Adds specified elements to the set
     */
    public void seedSet(AdvSet seed) {
        this.addAll(seed);
    }
}