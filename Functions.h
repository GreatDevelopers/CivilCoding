/**
 *       \file       Functions.h
 *
 *       \brief      This contains all the common functions used in the prohect
 *
 *       \version    0.1
 *       \date       02/02/2014 01:02:45 AM\n
 *       Compiler    g++
 *
 *       \author     Piyush Parkash, achyutapiyush@gmail.com
 *       License     GNU General Public License
 *       \copyright  Copyright (c) 2014, GreatDevelopers
 *                   https://github.com/GreatDevelopers
 */


#define HTML_DIR "html/"


int header()
{
    printf("Content-type:text/html\r\n\r\n");
    return 0;
}

int displayFile(const char *fileName)
{
    //Open the file
    FILE* file;

    file = fopen(fileName, "r");

    if (file == NULL)
    {
        return false;
    }

    char ch;
    while ( (ch = fgetc(file)) != EOF)
    {
        printf("%c", ch);
    }

    fclose(file);

    return 0;

}

