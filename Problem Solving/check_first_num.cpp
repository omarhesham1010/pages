#include <iostream>
using namespace std;
int main() {
 string input;
 cin >> input;

 int num = input[0] - '0';
 if (num % 2 == 0) {
     cout << "EVEN" << '\n';
 }
 else {
     cout << "ODD" << '\n';
 }

 return 0;
}