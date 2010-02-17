#include <Python.h>
#include "GridMap.h"
#include <iostream>
#include "VMapFactory.h"
using namespace VMAP;
using namespace std;
GridMap * currmap;
int cgx,cgy;
bool vmaploaded = false;
void LoadVMap(int id ,int gx,int gy)
{
                                                            // x and y are swapped !!
    int vmapLoadResult = VMAP::VMapFactory::createOrGetVMapManager()->loadMap("./vmaps",  id, gx,gy);
    switch(vmapLoadResult)
    {
        case VMAP::VMAP_LOAD_RESULT_OK:
            printf("VMAP loaded");
            break;
        case VMAP::VMAP_LOAD_RESULT_ERROR:
            printf("Could not load VMAP");
            break;
        case VMAP::VMAP_LOAD_RESULT_IGNORED:
            printf("Ignored VMAP");
            break;
    }
}
static PyObject * gridmap_los(PyObject *self,PyObject*args)
{
  unsigned int id;
  float x1,y1,z1,x2,y2,z2;
  bool los = false;
  if (!PyArg_ParseTuple(args, "Iffffff", &id,&x1,&y1,&z1,&x2,&y2,&z2))
  {
  return Py_BuildValue("");
  }
  if ( not ((int)(32-x1/SIZE_OF_GRIDS) == cgx and (int)(32-y1/SIZE_OF_GRIDS) == cgy) )
  {
    cgx = (int)(32-x1/SIZE_OF_GRIDS);
    cgy = (int)(32-y1/SIZE_OF_GRIDS);
    LoadVMap(id,cgx,cgy);
    los = VMAP::VMapFactory::createOrGetVMapManager()->isInLineOfSight(id, x1,y1,z1,x2,y2,z2);
    
  }else{
    
    printf("\n");
    los = VMAP::VMapFactory::createOrGetVMapManager()->isInLineOfSight(id, x1,y1,z1,x2,y2,z2);
  }
  return Py_BuildValue("i",(int)los);
  
  
  
  
}
static PyObject * gridmap_getheight(PyObject *self,PyObject*args)
{
  unsigned int id;
  float x,y,z;
  float maph = -200000.0;
  if (!PyArg_ParseTuple(args, "Ifff", &id,&x,&y,&z))
  {
  return Py_BuildValue("");
  }
  if ( not currmap )
  {
    char filename[1024];
    cgx = (int)(32-x/SIZE_OF_GRIDS);
    cgy = (int)(32-y/SIZE_OF_GRIDS);
    LoadVMap(id,cgx,cgy);
    vmaploaded = true;
    sprintf(filename,"maps/%03u%02d%02d.map",id,(int)(32-x/SIZE_OF_GRIDS),(int)(32-y/SIZE_OF_GRIDS));
    currmap = new GridMap;
    cout << "Loading " << filename << endl;
    bool r = currmap->loadData(filename);
    if (!r)
      return Py_BuildValue("");
    maph = currmap->getHeight(x,y);
    float vmaph = VMAP::VMapFactory::createOrGetVMapManager()->getHeight(id, x, y, z + 5.0f);
    maph = std::max(maph,vmaph);
  }else if( (int)(32-x/SIZE_OF_GRIDS) == cgx and (int)(32-y/SIZE_OF_GRIDS) == cgy)
  {
    maph = currmap->getHeight(x,y);
    float vmaph = VMAP::VMapFactory::createOrGetVMapManager()->getHeight(id, x, y, z + 5.0f);
    maph = std::max(maph,vmaph);
  }else{
    cout << "Unloading map " << cgx << "," << cgy << endl;
    delete currmap;
    char filename[1024];
    cgx = (int)(32-x/SIZE_OF_GRIDS);
    cgy = (int)(32-y/SIZE_OF_GRIDS);
    sprintf(filename,"maps/%03u%02d%02d.map",id,(int)(32-x/SIZE_OF_GRIDS),(int)(32-y/SIZE_OF_GRIDS));
    currmap = new GridMap;
    cout << "Loading " << filename << endl;
    LoadVMap(id,cgx,cgy);
    
    
    
    bool r = currmap->loadData(filename);
    if (!r)
      maph = currmap->getHeight(x,y);
    float vmaph = VMAP::VMapFactory::createOrGetVMapManager()->getHeight(id, x, y, z + 5.0f);
    maph = std::max(maph,vmaph);
  }
  return Py_BuildValue("f",maph);
}
static PyObject * gridmap_init(PyObject *self,PyObject*args)
{
  currmap = NULL;
  cgx = -1;
  cgy = -1;
  
}
static PyMethodDef gridmapMethods[] = {
  {"getheight",gridmap_getheight,METH_VARARGS,"Nodoc"},
  {"los",gridmap_los,METH_VARARGS,"Nodoc"},
  {NULL,NULL,0,NULL}
};
PyMODINIT_FUNC
initgridmap(void)
{
  (void) Py_InitModule("gridmap", gridmapMethods);
}
  
