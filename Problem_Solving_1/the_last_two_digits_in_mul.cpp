#include <iostream>
using namespace std;
int main() {
    int A, B, C, D;
        cin >> A >> B >> C >> D;

        int result = 1;
        result = (result * A) % 100;
        result = (result * B) % 100;
        result = (result * C) % 100;
        result = (result * D) % 100;

        if (result < 10) cout << "0" << result << "\n";
        else cout << result << "\n";
}