#include<stdio.h>
#include<math.h>
#include"Civil.h"

/*
 * Program for analysis of cantilever beam developed by Dr.G.S.Suresh and Dr. 
 * M.N.Shesha Prakash
 * l = Span of the beam
 * p[] = Intensity of concentrated load
 * ac[] = Position of concentrated load measured from free end A
 * wu[]=  Intensity of uniformly distributed load (udl)
 * au[] = Position of starting point of udl measured from free end A
 * lu[] = Length of udl
 * x = Position of section where SF and BM are computed, measured from free end A
 * dx = Length of segment computed as total length divided by number of segments 
 * Nc = Number of concentrated loads
 * Nu = Number of uniformly distributed loads
 * N = Number of segments
 * Vc[] = Shear force at a section due to concentrated loads
 * Vu[] = Shear force at a section due to uniformly distributed loads
 * Mc[] = Bending moment at a section due to concentrated loads
 * Mu[] = Bending moment at a section due to uniformly distributed loads
 * V[] =  Net shear force at a section due to concentrated loads and uniformly distributed 
 * loads
 * M[] =  Net bending moment at a section due to concentrated loads and uniformly 
 * distributed loads
 * i,j,k  are integer variables used as index in for loops
 * */
int cantbm(int Nc, int Nu, float l, int N)
{
    FILE *fp;
    int i, j, k;
    float x,dx,wu[10], au[10], lu[10], Vc[10], Mc[10], Vu[10];
    float Mu[10], V[10], M[10], p[10], ac[10];

    fp = fopen("cantbm.out","a");
    
    if (Nc>0)
    {
        printf("For each Concentrated Load Enter Intensity of Load and its position \n");
        for (i=1; i<=Nc; i++)
            scanf("%f%f",&p[i],&ac[i]);
    }
    if (Nu>0)
    {
        printf("For each UDL Type Intensity of Load, its distance from free ");
        printf("end and length \n");
        for (i=1; i<=Nu;i++)
        {
            scanf("%f%f%f",&wu[i],&au[i],&lu[i]);
        }
    }
        fprintf(fp," x      SF      BM\n");
        x=0;
        dx=l/N;
        for (i=0;i<=N; i++)
        {
            Vc[i]=0;
            Mc[i]=0;
            Vu[i]=0;
            Mu[i]=0;
            V[i]=0;
            M[i]=0;
        }
        for (i=0; i<=N;i++)
        {
            for (j=1;j<=Nc;j++)
            {
                if (x>ac[j])
                {
                    Vc[i]=Vc[i]+p[j];
                    Mc[i]=Mc[i]-p[j]*(x-ac[j]);
                }
            }

            for (k=1; k<=Nu; k++)
            {
                if ((x>au[k]) && (x<=au[k]+lu[k]))
                {
                    Vu[i]=Vu[i]+wu[k]*(x-au[k]);
                    Mu[i]=Mu[i]-wu[k]*(x-au[k])*(x-au[k])/2.0;
                }
                else if (x>(au[k]+lu[k]))
                {
                    Vu[i]=Vu[i]+wu[k]*lu[k];
                    Mu[i]=Mu[i]-wu[k]*lu[k]*(x-au[k]-lu[k]/2.0);
                }
            }
            V[i]=Vc[i]+Vu[i];
            M[i]=Mc[i]+Mu[i];
            fprintf(fp, "%5.0f %10.3f %10.3f\n",x,V[i],M[i]);
            for(j=1; j<=Nc; j++)
                if (x==ac[j])
                    fprintf(fp, "%5.0f %10.3f %10.3f\n", x, V[i]+p[j],M[i]);
            x=x+dx;
        }
    
    return 0;

}
