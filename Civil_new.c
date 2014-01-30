#include <stdio.h>
#include <math.h>
#include "Civil_new.h"

#define FILENAME "cantbm.out"

const int size = 10;

int cantbm_output(float V[10], float M[10], float ac[10], float p[10], FILE *fp, float l, int N, int Nc)
{
    float x = 0, dx = l / N;
    for (int i = 0; i <= N; i++)
    {
            fprintf(fp, "%5.0f %10.3f %10.3f\n", x, V[i], M[i]);
            for(int j = 1; j <= Nc; j++)
            {
                if (x == ac[j])
                {
                    fprintf(fp, "%5.0f %10.3f %10.3f\n", x, V[i] + p[j], M[i]);
                }
            }
            x += dx;
    }

    return 0;

}

int cantbm_process(float p[10], float ac[10], float wu[10], float au[10], float lu[10], FILE* fp, float l, int N, int Nc, int Nu)
{
        fprintf(fp, " x      SF      BM\n");
        float x = 0, Vc[10], Mc[10], Vu[10], Mu[10], V[10], M[10];
        float dx = l / N;
        for (int i = 0; i <= N; i++)
        {
            Vc[i] = 0;
            Mc[i] = 0;
            Vu[i] = 0;
            Mu[i] = 0;
            V[i] = 0;
            M[i] = 0;
        }

        //Output section kind of starts from here
        for (int i = 0; i <= N; i++)
        {
            for (int j = 1;j <= Nc; j++)
            {
                if (x > ac[j])
                {
                    Vc[i] = Vc[i] + p[j];
                    Mc[i] = Mc[i] - p[j] * (x - ac[j]);
                }
            }

            for (int k = 1; k <= Nu; k++)
            {
                if ((x > au[k]) && (x <= au[k] + lu[k]))
                {
                    Vu[i] = Vu[i] + wu[k] * (x - au[k]);
                    Mu[i] = Mu[i] - wu[k] * (x - au[k]) * (x - au[k]) / 2.0;
                }
                else if (x > (au[k] + lu[k]))
                {
                    Vu[i] = Vu[i] + wu[k] * lu[k];
                    Mu[i] = Mu[i] - wu[k] * lu[k] * (x - au[k] - lu[k] / 2.0);
                }
            }
            V[i] = Vc[i] + Vu[i];
            M[i] = Mc[i] + Mu[i];
            x = x + dx;
        }

        cantbm_output(*V, *M, *ac, *p, fp, l, N, Nc);
    return 0;
}




int cantbm_input(int Nc, int Nu, float l, int N)
{
    FILE *fp;
    int i, j, k;
    float p[10], ac[10], wu[10], au[10], lu[10];
    fp = fopen(FILENAME, "a");
    
    if (Nc > 0)
    {
        printf("For each Concentrated Load Enter Intensity of Load and its position \n");
        for (i = 1; i <= Nc; i++)
        {
            scanf("%f%f", &p[i], &ac[i]);
        }
    }
    if (Nu > 0)
    {
        printf("For each UDL Type Intensity of Load, its distance from free ");
        printf("end and length \n");
        for ( i = 1; i <= Nu; i++)
        {
            scanf("%f%f%f", &wu[i], &au[i], &lu[i]);
        }
    }

    cantbm_process(*p, *ac, *wu, *au, *lu, fp, l, N, Nc, Nu);      // Calling the process function

    return 0;

}



