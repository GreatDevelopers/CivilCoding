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


#include<stdio.h>
#include<math.h>

int main()
{
    /* Declaring the pointer fp as a file  */
    FILE *fp;
    int i, j, k, Nc, Nu, N;
    float x,l,dx,p[10],ac[10], wu[10], au[10], lu[10], Vc[10], Mc[10], Vu[10];
    float Mu[10], V[10], M[10];

    /* Assigning output file cantbm.out */
    fp = fopen("cantbm.out","a");

    /* Printed on the screen to guide user to enter values */
    printf("Enter the values of Nc, Nu, l, N\n");
    
    /* Input of general information of beam */
    scanf("%d%d%f%d",&Nc,&Nu,&l,&N);
    
    /* Input is done when concentrated load is present */
    if (Nc>0)
    {
        printf("For each Concentrated Load Enter Intensity of Load and its position \n");
        for (i=1; i<=Nc; i++)
            /* Input of intensity of concentrated load and its position */
            scanf("%f%f",&p[i],&ac[i]);
    }

    /* Input is done when uniformaly distributed load is present */
    if (Nu>0)
    {
        printf("For each UDL Type Intensity of Load, its distance from free ");
        printf("end and length \n");
        for (i=1; i<=Nu;i++)
        {
            /* Input of intensity of uniformly distributed load its, position and its length */
            scanf("%f%f%f",&wu[i],&au[i],&lu[i]);
        }
    }
        /* Printing of the header of table */
        fprintf(fp," x      SF      BM\n");
        x=0;
        dx=l/N; 
        for (i=0;i<=N; i++) /* Initialization */
        {
            Vc[i]=0;
            Mc[i]=0;
            Vu[i]=0;
            Mu[i]=0;
            V[i]=0;
            M[i]=0;
        }
        for (i=0; i<=N;i++) /* Loop for computing SF and BM at equal Interval */
        {
            for (j=1;j<=Nc;j++) /* Loop for computing SF and BM due to concentrated load */
            {
                if (x>ac[j])
                {
                    Vc[i]=Vc[i]+p[j]; /* Computation of SF */
                    Mc[i]=Mc[i]-p[j]*(x-ac[j]); /* Computation of BM */
                }
            }

            for (k=1; k<=Nu; k++)   /* Loop for computing SF and BM due to uniformly distributed load */
            {
                if ((x>au[k]) && (x<=au[k]+lu[k]))/* Section on UDL */
                {
                    /* Computation of SF */
                    Vu[i]=Vu[i]+wu[k]*(x-au[k]);

                    /* Computation of BM */
                    Mu[i]=Mu[i]-wu[k]*(x-au[k])*(x-au[k])/2.0;
                }
                else if (x>(au[k]+lu[k]))
                {
                    /* Computation of SF */
                    Vu[i]=Vu[i]+wu[k]*lu[k];

                    /* Computation of BM */
                    Mu[i]=Mu[i]-wu[k]*lu[k]*(x-au[k]-lu[k]/2.0);
                }
            }
            V[i]=Vc[i]+Vu[i]; /* Computation of net Shear Force of Section */
            M[i]=Mc[i]+Mu[i];   /* Computation of net Bending moment of section */
            fprintf(fp, "%5.0f %10.3f %10.3f\n",x,V[i],M[i]);
            /* To check for the section to have any concetrated load */
            for(j=1; j<=Nc; j++)
                if (x==ac[j])
                    fprintf(fp, "%5.0f %10.3f %10.3f\n", x, V[i]+p[j],M[i]); /* Adds intensity of concentrated load to Sf at the section */
            x=x+dx;
        }
    
    return 0;
    }
