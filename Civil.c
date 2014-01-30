#include<stdio.h>
#include<math.h>
#include"Civil.h"

/*
 * Program for analysis of cantilever beam developed by Dr.G.S.Suresh and Dr. 
 * M.N.Shesha Prakash
 * spanBeam = Span of the beam(l)
 * conLoadInten[] = Intensity of concentrated load(p)
 * conLoadA[] = Position of concentrated load measured from free end A(ac)
 * uniIntensity[]=  Intensity of uniformly distributed load (udl)(wu)
 * udlStartPos[] = Position of starting point of udl measured from free end A(au)
 * lenUDL[] = Length of udl(lu)
 * x = Position of section where SF and BM are computed, measured from free end A(x)
 * dx = Length of segment computed as total length divided by number of segments (dx)
 * noConLoad = Number of concentrated loads(Nc)
 * noUniLoad = Number of uniformly distributed loads(Nu)
 * N = Number of segments
 * conLoadShearForce[] = Shear force at a section due to concentrated loads(Vc)
 * uniLoadShearForce[] = Shear force at a section due to uniformly distributed loads(Vu)
 * conLoadBendMoment[] = Bending moment at a section due to concentrated loads(Mc)
 * uniLoadBendMoment[] = Bending moment at a section due to uniformly distributed loads(Mu)
 * netShearForce[] =  Net shear force at a section due to concentrated loads and uniformly distributed 
 * loads(V)
 * netBendMoment[] =  Net bending moment at a section due to concentrated loads and uniformly 
 * distributed loads(M)
 * i,j,k  are integer variables used as index in for loops
 * */
#define FILENAME "cantbm.out"

const int size = 10;

int cantBMOutput(float netShearForce[10], float netBendMoment[10], float conLoadA[10], float conLoadInten[10], FILE *fp, float spanBeam, int noSeg, int noConLoad)
{
    float x = 0, dx = spanBeam / noSeg;
    for (int i = 0; i <= noSeg; i++)
    {
            fprintf(fp, "%5.0f %10.3f %10.3f\n", x, netShearForce[i], netBendMoment[i]);
            for(int j = 1; j <= noConLoad; j++)
            {
                if (x == conLoadA[j])
                {
                    fprintf(fp, "%5.0f %10.3f %10.3f\n", x, netShearForce[i] + conLoadInten[j], netBendMoment[i]);
                }
            }
            x += dx;
    }

    return 0;

}

int cantBMProcess(float conLoadInten[10], float conLoadA[10], float uniIntensity[10], float udlStartPos[10], float lenUDL[10], FILE* fp, float spanBeam, int noSeg, int noConLoad, int noUniLoad)
{
        fprintf(fp, " x      SF      BM\n");
        float x = 0, conLoadShearForce[10], conLoadBendMoment[10], uniLoadShearForce[10], uniLoadBendMoment[10], netShearForce[10], netBendMoment[10];
        float dx = spanBeam / noSeg;
        for (int i = 0; i <= noSeg; i++)
        {
            conLoadShearForce[i] = 0;
            conLoadBendMoment[i] = 0;
            uniLoadShearForce[i] = 0;
            uniLoadBendMoment[i] = 0;
            netShearForce[i] = 0;
            netBendMoment[i] = 0;
        }

        //Output section kind of starts from here
        for (int i = 0; i <= noSeg; i++)
        {
            for (int j = 1;j <= noConLoad; j++)
            {
                if (x > conLoadA[j])
                {
                    conLoadShearForce[i] = conLoadShearForce[i] + conLoadInten[j];
                    conLoadBendMoment[i] = conLoadBendMoment[i] - conLoadInten[j] * (x - conLoadA[j]);
                }
            }

            for (int k = 1; k <= noUniLoad; k++)
            {
                if ((x > udlStartPos[k]) && (x <= udlStartPos[k] + lenUDL[k]))
                {
                    uniLoadShearForce[i] = uniLoadShearForce[i] + uniIntensity[k] * (x - udlStartPos[k]);
                    uniLoadBendMoment[i] = uniLoadBendMoment[i] - uniIntensity[k] * (x - udlStartPos[k]) * (x - udlStartPos[k]) / 2.0;
                }
                else if (x > (udlStartPos[k] + lenUDL[k]))
                {
                    uniLoadShearForce[i] = uniLoadShearForce[i] + uniIntensity[k] * lenUDL[k];
                    uniLoadBendMoment[i] = uniLoadBendMoment[i] - uniIntensity[k] * lenUDL[k] * (x - udlStartPos[k] - lenUDL[k] / 2.0);
                }
            }
            netShearForce[i] = conLoadShearForce[i] + uniLoadShearForce[i];
            netBendMoment[i] = conLoadBendMoment[i] + uniLoadBendMoment[i];
            x = x + dx;
        }

        cantBMOutput(netShearForce, netBendMoment, conLoadA, conLoadInten, fp, spanBeam, noSeg, noConLoad);
    return 0;
}




int cantBMInput(int noConLoad, int noUniLoad, float spanBeam, int noSeg)
{
    FILE *fp;
    int i, j, k;
    float conLoadInten[10], conLoadA[10], uniIntensity[10], udlStartPos[10], lenUDL[10];
    fp = fopen(FILENAME, "a");
    
    if (noConLoad > 0)
    {
        printf("For each Concentrated Load Enter Intensity of Load and its position \n");
        for (i = 1; i <= noConLoad; i++)
        {
            scanf("%f%f", &conLoadInten[i], &conLoadA[i]);
        }
    }
    if (noUniLoad > 0)
    {
        printf("For each UDL Type Intensity of Load, its distance from free ");
        printf("end and length \n");
        for ( i = 1; i <= noUniLoad; i++)
        {
            scanf("%f%f%f", &uniIntensity[i], &udlStartPos[i], &lenUDL[i]);
        }
    }

    cantBMProcess(conLoadInten, conLoadA, uniIntensity, udlStartPos, lenUDL, fp, spanBeam, noSeg, noConLoad, noUniLoad);      // Calling the process function

    return 0;

}

