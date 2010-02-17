#include "VMapFactory.h"
#include <Vector3.h>
using namespace G3D;
using namespace VMAP;
MapTree * vm;
extern "C"{
 void initialize(char * path);
float getHeight(float x,float y,float z); 
  
}

void initialize(char * path)
{
  
  vm = new VMapFactory(path);
  vm->createOrGetVMapManager()->setEnableHeightCalc(true);
}
float getHeight(float x,float y,float z)
{
  Vector3 pos;
  pos.x =x;
  pos.y =y;
  pos.z =z;
  return vm->getHeight(pos);
  
  
  
}
