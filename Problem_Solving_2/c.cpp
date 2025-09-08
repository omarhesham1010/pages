#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "How many numbers? ";
    cin >> n;

    int num;
    int count_positive = 0;
    int count_negative = 0;
    int count_even = 0;
    int count_odd = 0;

    for (int i = 1; i <= n; i++) {
        cout << "Enter number " << i << ": ";
        cin >> num;

        if (num > 0) count_positive++;
        else if (num < 0) count_negative++;

        if (num % 2 == 0) count_even++;
        else count_odd++;
    }

    cout << "\nPositive count = " << count_positive << endl;
    cout << "Negative count = " << count_negative << endl;
    cout << "Even count = " << count_even << endl;
    cout << "Odd count = " << count_odd << endl;

    return 0;
}
