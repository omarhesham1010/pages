#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "How many numbers? ";
    cin >> n;

    int num, max;
    cout << "Enter number 1: ";
    cin >> num;
    max = num; 
    for (int i = 2; i <= n; i++) {
        cout << "Enter number " << i << ": ";
        cin >> num;
        if (num > max) {
            max = num; 
        }
    }

    cout << "Max num = " << max << endl;

    return 0;
}
