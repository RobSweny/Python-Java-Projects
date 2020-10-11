/*
https://leetcode.com/problems/split-a-string-in-balanced-strings/
Balanced strings are those who have equal quantity of 'L' and 'R' characters.
Given a balanced string s split it in the maximum amount of balanced strings.
Return the maximum amount of splitted balanced strings.

Example 1:
Input: s = "RLRRLLRLRL"
Output: 4
Explanation: s can be split into "RL", "RRLL", "RL", "RL", each substring contains same number of 'L' and 'R'.
*/
class SplitBalancedString {
    public int balancedStringSplit(String s) {
        int counter = 0, ans = 0;
        for (char ch : s.toCharArray()){
            if(ch == 'R') ans += 1;
            else ans -= 1;
            if(ans == 0) counter += 1;
        }
        return counter;
    }
}