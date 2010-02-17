#include <stdio.h>
#include <IL/il.h>
#include <IL/ilu.h>
#include <iostream>
#include <stdlib.h>
#include <stdarg.h>
#include "GridMap.h"
using namespace std;
int main(int argc,char ** argv)
{
GridMap * map;
map = new GridMap;
char filename[1024];
float x= atof(argv[1]);float y = atof(argv[2]);
sprintf(filename,"maps/%03u%02d%02d.map",1,(int)(32-x/SIZE_OF_GRIDS),(int)(32-y/SIZE_OF_GRIDS));
cout << "Loading " << filename << endl;
bool r = map->loadData(filename);
if (!r)
  cout << "Cannot load " << filename << " Replacing with blackmap" << endl;
else{
  printf("%f\n",map->getHeight(x,y));
  
    
  
  
  
}
}