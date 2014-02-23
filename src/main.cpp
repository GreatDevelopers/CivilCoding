#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cstring>
#include "Civil.h"
#include "Functions.h"
#include <rude/cgi.h>
#include <iostream>


using namespace std;
using namespace rude;
int main()
{

    //The CGI Parser
    CGI cgi;

    //check here for posted information

    
    if (cgi.exists("initialparameter"))
    {
      
        //we have posted information. Lets first fetch the information

        //Firstly the very basic information
        int nc, nu, noseg;
        float spanbeam;
          nc=         atoi(cgi.value("nc"));
          nu=         atoi(cgi.value("nu"));
          spanbeam =  atof(cgi.value("spanbeam"));
          noseg =     atoi(cgi.value("noseg"));
          //cout<<nc<<endl<<nu<<endl<<spanbeam<<endl<<noseg;

        //Now the dependent information
        float conLoadInten[10], conLoadA[10], uniIntensity[10], udlStartPos[10], lenUDL[10];
        if (nc>0)
        {
            for (int i=1; i<=nc; i++)
            {
                conLoadInten[i] = atof(cgi.value("p",i-1));
                conLoadA[i] = atof(cgi.value("ac", i-1));
                //cout<<conLoadA[i]<<endl<<conLoadInten[i]<<endl;
            }
        }

        if (nu>0)
        {
            for (int i=1; i<=nu; i++)
            {
                uniIntensity[i] = atof(cgi.value("wu",i-1));
                udlStartPos[i] = atof(cgi.value("au", i-1));
                lenUDL[i] = atof(cgi.value("lu", i-1));
                //cout<<uniIntensity[i]<<endl<<udlStartPos[i]<<endl<<lenUDL[i]<<endl;
            }
        }
        
        //Create a file for the output
        FILE* fbm;
        FILE* fsf;

        fbm = fopen(FILENAME_SF, "w");
        fsf = fopen(FILENAME_BM, "w");  
        
        //Now do the processing and output we have skipped the input part
        cantBMProcess(conLoadInten, conLoadA, uniIntensity, udlStartPos, lenUDL, fbm, fsf, spanbeam, noseg, nc, nu);
        printf("Location: index.sh\n\n");
    }
    header();

    //displaying the html header
    displayFile("header.html");

    if (cgi.exists("secondaryparameter"))
    {
        displayFile("output.html");
        displayFile("footer.html");
        return 0;
    }

    //displaying the main form
    displayFile("form.html");
    
    //Display the footer file
    displayFile("footer.html");
    return 0;

}
