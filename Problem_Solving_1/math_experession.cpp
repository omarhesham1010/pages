 #include<iostream>
 using namespace std;
    int main() {
 int num1, num2, res;
 char op1, op2;

 cin >> num1 >> op1 >> num2 >> op2 >> res;

 if (op1 == '+') {
     if (num1 + num2 == res) cout << "Yes\n";
     else cout << num1 + num2 << '\n';
 }
 else if (op1 == '-') {
     if (num1 - num2 == res) cout << "Yes\n";
     else cout << num1 - num2 << '\n';
 }
 else if (op1 == '*') {
     if (num1 * num2 == res) cout << "Yes\n";
     else cout << num1 * num2 << '\n';
 }

 return 0;
}