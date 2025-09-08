#include <iostream>
using namespace std;

int main() {


    
    int a, b, c;
    cin >> a >> b >> c;

    int x = a, y = b, z = c;

   
    if (x > y) swap(x, y);
    if (x > z) swap(x, z);
    if (y > z) swap(y, z);

  
    cout << x << "\n" << y << "\n" << z << "\n\n";

    return 0;
    

}