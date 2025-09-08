#include <iostream>
using namespace std;
int main() {
        int number;
    cin >> number;

    int years = number / 365;
    number %= 365;

    int months = number / 30;
    number %= 30;

    int days = number;

    cout << years << " years\n" << months << " months\n" << days << " days\n";

    return 0;
}