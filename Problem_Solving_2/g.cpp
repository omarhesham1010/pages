#include<iostream>
using namespace std;

int main()
{
     long long N,num,x; 
     cin>>N;
     for(int i=1;i<=N;i++){
     cin>>num;
      x=1;
     for(int j=1;j<=num;j++){
     x*=j;
     }
     cout<<x<<'\n';
     }
    return 0;
}
