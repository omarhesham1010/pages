#include<iostream>
#include<bits/stdc++.h>
using namespace std;
int main(){
     int a,b,c=0;
     cin>>a>>b;
     for(int i=a;i<=b;i++){
     bool t=0;
     int n=i;
     while(n!=0){
     int d=n%10;
     n/=10;
     if(d!=7&&d!=4){
     t=1;
     }
     }
     if(t==0){
     cout<<i<<" ";
     c++;
     }
     }
     if(c==0){
     cout <<"-1";
     }
    return 0;
    }
