#include <iostream>
#include <IL/il.h>
#include <stdlib.h>
#include <stdarg.h>
int main(int argc,char ** argv)
{
  char * data;
  
  FILE * f;
  ilInit();
  ILuint img;
  ilGenImages(1,&img);
  ilBindImage(img);
  ilTexImage(atoi(argv[1]),atoi(argv[2]),1,3,IL_RGB,IL_UNSIGNED_BYTE,NULL);
  f = fopen(argv[3],"rb");
  fseek(f,0,SEEK_END);
  int filesize = ftell(f);
  printf("%i\n",filesize);
  data = (char*)ilGetData();
  fseek(f,0,SEEK_SET);
  fread(data,filesize,1,f);
  fclose(f);
  
  printf("%i,%i\n",ilGetInteger(IL_IMAGE_WIDTH),ilGetInteger(IL_IMAGE_HEIGHT));
  ilSaveImage("out.bmp");
  return 0;
  
  
}