#include<bits/stdc++.h>
using namespace std;
int getf(int n)
{
    int get = 0;
    while(n != 0)
    {
        get = get + (n % 10);
        n = n / 10;

    }
    //cout<<"get = "<<get<<endl;
    return get;
}

int main()
{
    char str[10000];
    int t,sum,arr[10000],k,z=1;
    cin>>t;
    while(t--)
    {
        int l;
        k = 0;
        scanf("%s",str);
        l = strlen(str);
        sum = 0;
        for(int i=0; i<l; ++i)
        {
            if(str[i] >= 48 && str[i] <= 57)
                arr[++k] = (str[i] - '0') ;
            else if(str[i] >= 65 && str[i] <= 90)
                arr[++k] = (str[i] - 'A') + 1;
            else
                arr[++k] = (str[i] - 'a') + 1;
            //cout<<arr[k]<<endl;
        }
       // cout<<"k = "<<k<<endl;
        for(int i=1; i<=k ; ++i)
        {
            int m;
            m = arr[i];
            while(m != 0)
            {
                sum = sum + (m%10);
                m = m / 10;
            }
        }
        xy :

        //cout<<sum<<endl;
        if(sum < 10)
        {
            if(sum == 9)
                printf("Case %d: YES\n",z);
            else
                printf("Case %d: NO\n",z);
        }
        else{
            sum = getf(sum);
            //cout<<sum<<endl;
            goto xy;
        }
        z++;

    }
    return 0;
}