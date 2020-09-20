public int findNumbers(int[] nums) {
    int evens = 0;
    for (int each:nums) {
        if ((int)(Math.log10(each)+1) % 2 ==0) {
            evens++;
        }
    }
    return evens;
}