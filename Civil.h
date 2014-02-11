/**
 *       \file       Civil.h
 *
 *       \brief      This file contains the header of the Civil Program Functions
 *
 *       \version    0.1
 *       \date       01/27/2014 05:41:23 PM\n
 *       Compiler    g++
 *
 *       \author     H. S. RAI
 *       License     GNU General Public License
 *       \copyright  Copyright (c) 2014, GreatDevelopers
 *                   https://github.com/GreatDevelopers
 */

#define FILENAME_BM "cantsf.out"
#define FILENAME_SF "cantbm.out"

int cantBMInput(int, int, float, int);
int cantBMProcess(float[], float[], float[], float[], float[], FILE*, FILE*, float, int, int, int);
int cantBMOutput(float[], float[], float[], float[], FILE*, FILE*, float, int, int);
