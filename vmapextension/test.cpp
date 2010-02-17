#include "VMapFactory.h"
#include <iostream>
#include <Vector3.h>
#include <IL/il.h>
#include <IL/ilu.h>
using namespace G3D;
using namespace VMAP;
#define MAX_NUMBER_OF_GRIDS      64
#define SIZE_OF_GRIDS            533.33333f
#define CENTER_GRID_OFFSET      (SIZE_OF_GRIDS/2)
#define CENTER_GRID_ID           (MAX_NUMBER_OF_GRIDS/2)
int getvmappos(float x)
{
  double x_offset = (double(x) - CENTER_GRID_OFFSET)/SIZE_OF_GRIDS;
  int x_val = int(x_offset+CENTER_GRID_ID + 0.5);
  return x_val;
}
class Image{
  public:
    ILuint image;
    int w;
    int h;
    int d;
    unsigned char * datapointer;
    Image()
    {
      ilGenImages(1,&image);
      
      
      
    }
    Image(char * filename)
    {
      ilGenImages(1,&image);
      ilBindImage(image);
      ilLoadImage(filename);
      ConvertToRGB();
      w = ilGetInteger(IL_IMAGE_WIDTH);
      h = ilGetInteger(IL_IMAGE_HEIGHT);
      d = ilGetInteger(IL_IMAGE_DEPTH);
      datapointer = ilGetData();
    }
    void Save(char * filename)
    {
      ilBindImage(image);
      ilSaveImage(filename);
    }
    void AllocateLUM(int x, int y,char * data=NULL)
    {
      ilBindImage(image);
      ilTexImage(x,y,1,1,IL_LUMINANCE,IL_UNSIGNED_BYTE,data);
      datapointer = ilGetData();
      w = ilGetInteger(IL_IMAGE_WIDTH);
      h = ilGetInteger(IL_IMAGE_HEIGHT);
      d = ilGetInteger(IL_IMAGE_DEPTH);
    }
    void AllocateRGB(int x, int y,char * data=NULL)
    {
      ilBindImage(image);
      ilTexImage(x,y,1,3,IL_RGB,IL_UNSIGNED_BYTE,data);
      datapointer = ilGetData();
      w = ilGetInteger(IL_IMAGE_WIDTH);
      h = ilGetInteger(IL_IMAGE_HEIGHT);
      d = ilGetInteger(IL_IMAGE_DEPTH);
    }
    void Rescale(int x , int y)
    {
      ilBindImage(image);
      iluScale(x,y,1);
      datapointer = ilGetData();
      w = ilGetInteger(IL_IMAGE_WIDTH);
      h = ilGetInteger(IL_IMAGE_HEIGHT);
      d = ilGetInteger(IL_IMAGE_DEPTH);
    }
    void GetPixelRGB(int x_,int y_,unsigned char * pix)
    {
      
      int x = x_ % w;
      int y = y_ % h;
      
      if ( datapointer )
      {
      pix[0] = datapointer[w*y*3+x*3];
      pix[1] = datapointer[w*y*3+x*3+1];
      pix[2] = datapointer[w*y*3+x*3+2];
      }else{
	printf("GetPixelRGB(%i,%i): datapointer is NULL\n",x_,y_);
      }
      //printf("%i %i %i\n",(int)pix[0],(int)pix[1],int(pix[2]));
    }
    void SetPixelRGB(int x_, int y_,char r, char g, char b)
    {
      int x = x_ % w;
      int y = y_ % h;
      datapointer[w*y*3+x*3] = r;
      datapointer[w*y*3+x*3+1] = g;
      datapointer[w*y*3+x*3+2] = b;
      
      
    }
    void SetPixelLUM(int x_, int y_, char val)
    {
      int x = x_ % w;
      int y = y_ % h;
      datapointer[y*w+x] = val;
      
      
    }
    void GetPixelLUM(int x_, int y_,unsigned char * p)
    {
      //printf("GetPixelLUM(%i,%i)\n",x_,y_);
      int x = x_ % w;
      int y = y_ % h;
      p[0] = datapointer[y*w+x];
      
    }
    void ConvertToLUM()
    {
      ilBindImage(image);
      ilConvertImage(IL_LUMINANCE,IL_UNSIGNED_BYTE);
      datapointer = ilGetData();
      iluFlipImage();
    }
    void ConvertToRGB()
    {
      ilBindImage(image);
      ilConvertImage(IL_RGB,IL_UNSIGNED_BYTE);
      datapointer = ilGetData();
    }
    ~Image()
    {
      ilDeleteImages(1,&image);
    }
};
int main(int argc,char ** argv)
{
  ilInit();
  Image * img = new Image();
  
  VMapFactory * f = new VMapFactory();
  f->createOrGetVMapManager()->setEnableHeightCalc(true);
  float xxx = -2250.634888;
  float yyy = -390.033691;
  int xx = 63-getvmappos(xxx);
  int yy = 63-getvmappos(yyy);
  switch(f->createOrGetVMapManager()->loadMap("/home/tiziano/WOWBot/vmap/vmaps",1,xx,yy))
  {
    case VMAP_LOAD_RESULT_OK:
      printf("Vmap loaded\n");
      break;
    case VMAP_LOAD_RESULT_ERROR:
      printf("Failed loading vmap\n");
      break;
    
    
  }
  float minx = xxx-SIZE_OF_GRIDS ;
  float maxx = xxx+SIZE_OF_GRIDS ;
  float miny = yyy-SIZE_OF_GRIDS ;
  float maxy = yyy+SIZE_OF_GRIDS ;



img->AllocateLUM(int(maxx-minx)+1,int(maxy-miny)+1);
for (float y = miny; y < maxy ;y+=1.0)
  {
    printf("%f/%f\n",y,maxy);
    for (float x = minx; x < maxx; x+=1.0)
    {
      for ( float h = -10; h < 70.0;h += 5.0)
      {
	float k = f->createOrGetVMapManager()->getHeight(1,x,y,h);
	if (k > 0.0)
	{
	  //printf("x=%f y=%f h=%f\n",x,y,k);
	  img->SetPixelLUM(int(x-minx),int(y-miny),int(k*3));

	  break;
	}
      }
 }
  }
  
  printf("%f %f -> %f %f\n",minx,miny,maxx,maxy);
  /*while (1)
  {
    
    printf("%f\n",f->createOrGetVMapManager()->getHeight(1,x,y,z));
  }*/
  img->Save("test1.png");
  
}