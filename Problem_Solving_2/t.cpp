#include<iostream>
#include<bits/stdc++.h>
using namespace std;
int main(){
     int n;
     cin >>n;
     for(int i=1;i<=n;i++){
     int z=n-i;
     for(int s=0;s<z;s++){
     cout <<" ";
     }
     int x=(i*2)-1;
     for(int j=1;j<=x;j++){
     cout <<"*";
     }
     cout <<"\n";
     }
    return 0;
    }
