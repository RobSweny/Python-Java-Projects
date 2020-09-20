public void reverseString(char[] s) {
    char holder = 'a';
    for (int i = 0; i < s.length/2; i++) {
        holder = s[i];
        s[i] = s[s.length-(1+i)];
        s[s.length-(1+i)] = holder;
    }
}