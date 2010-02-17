#include <Python.h>
#include "GridMap.h"
#include <iostream>
#include <vector>
#include <map>
#include "VMapFactory.h"
#include "Thread.h"
using namespace VMAP;
using namespace std;
GridMap * currmap;
bool deb = true;
int cgx,cgy;
bool vmaploaded = false;
int loadedmaps = 0;
int LoadVMap ( int id ,int gx,int gy )
{
    // x and y are swapped !!
    int vmapLoadResult = VMAP::VMapFactory::createOrGetVMapManager()->loadMap ( "./vmaps",  id, gx,gy );
    switch ( vmapLoadResult )
    {
    case VMAP::VMAP_LOAD_RESULT_OK:
        printf ( "VMAP loaded\n" );
        break;
    case VMAP::VMAP_LOAD_RESULT_ERROR:
        printf ( "Could not load VMAP\n" );
        break;
    case VMAP::VMAP_LOAD_RESULT_IGNORED:
        printf ( "Ignored VMAP\n" );
        break;
    }
	return vmapLoadResult;
}
class MapLoadInfo 
{
public:
    bool loaded;
	GridMap * map;
    MapLoadInfo ( int mapid_,int gx_,int gy_ )
    {
        gx = gx_;
        gy = gy_;
        mapid = mapid_;
        loaded = false;
		map = NULL;
    };
	void Load()
	{

	  char filename[1024];
	  if ( LoadVMap ( mapid,gx,gy ) != VMAP::VMAP_LOAD_RESULT_OK )
	  {
		printf("Cannot load vmap: Map %d , GridX %d, GridY %d\n",mapid,gx,gy);
		return;
	  }
	  sprintf ( filename,"maps/%03u%02d%02d.map",mapid, gx,gy);
	  map = new GridMap;
	  cout << "Loading " << filename << endl;
	  bool r = map->loadData ( filename );
	  if ( !r )
	  {
		cout << "Failed to load map " << filename << endl;
		delete map;
		VMAP::VMapFactory::createOrGetVMapManager()->unloadMap(mapid,gx,gy);
		map = NULL;
		return;
	  }
	  loaded = true;
	  loadedmaps++;

	}
	void Unload()
	{

	  VMAP::VMapFactory::createOrGetVMapManager()->unloadMap(mapid,gx,gy);
	  
	  if (map)
		delete map;
	  cout << "Map " << mapid << " Grid (" << gx << "," << gy << ") unloaded" << endl;
	  loaded = false;
	  loadedmaps--;

	}
	bool LOS(float x1,float y1,float z1,float x2,float y2,float z2)
	{

	  if ( !loaded )
	  {
		cout << "LOS on non loaded vmap" << endl;
		return false;
	  }
	  bool l = VMAP::VMapFactory::createOrGetVMapManager()->isInLineOfSight ( mapid, x1,y1,z1,x2,y2,z2 );

	  return l;
	  
	}
	float getheight(float x,float y,float z)
	{

	  //printf("getheight(%f,%f,%f) MAP %d\n",x,y,z,mapid);
	  if (!loaded )
	  {
		cout << "Getheight on non loaded vmap" << endl;
		return -50000;
	  }
	  float maph = map->getHeight ( x,y );
	  float vmaph = VMAP::VMapFactory::createOrGetVMapManager()->getHeight ( mapid, x, y, z + 5.0f );
	  maph = std::max ( maph,vmaph );

	  return maph;
	}
	~MapLoadInfo()
	{
	  Unload();
	  
	}
    int mapid;
    int gx;
    int gy;
};
typedef std::vector<MapLoadInfo*> gridvect;
typedef std::vector<gridvect> gridmatrix;

MapLoadInfo* maps[1024][64][64];

void initmaps()
{
  printf("**** INIT MAPS *****\n");
  for ( int i = 0; i < 1024; i++)
  {
	for ( int i2 = 0; i2 < 65; i2++)
	{
	  for ( int i3 = 0; i3 < 65; i3++)
	  {
		MapLoadInfo * inst;
		inst = new MapLoadInfo(i,i2,i3);
		maps[i][i2][i3] = inst;
	  }
	  
	}
	
	
  }
  
}
static PyObject * gridmap_los ( PyObject *self,PyObject*args )
{
    unsigned int id;
    float x1,y1,z1,x2,y2,z2;
    bool los = false;
    if ( !PyArg_ParseTuple ( args, "Iffffff", &id,&x1,&y1,&z1,&x2,&y2,&z2 ) )
    {
        return Py_BuildValue ( "" );
    }
	cgx = ( int ) ( 32-x1/SIZE_OF_GRIDS );
	cgy = ( int ) ( 32-y1/SIZE_OF_GRIDS );
	int cgx2 = ( int ) ( 32-x2/SIZE_OF_GRIDS );
	int cgy2 = ( int ) ( 32-y2/SIZE_OF_GRIDS );
	if ( ! maps[id][cgx2][cgy2]->loaded )
	  maps[id][cgx2][cgy2]->Load();
	if ( ! maps[id][cgx][cgy]->loaded )
	  maps[id][cgx][cgy]->Load();
    los = maps[id][cgx][cgy]->LOS(x1,y1,z1,x2,y2,z2);
    return Py_BuildValue ( "i", ( int ) los );




}
static PyObject * gridmap_getheight ( PyObject *self,PyObject*args )
{
    unsigned int id;
    float x,y,z;
    float maph = -200000.0;
    if ( !PyArg_ParseTuple ( args, "Ifff", &id,&x,&y,&z ) )
    {
        return Py_BuildValue ( "" );
    }
    
	cgx = ( int ) ( 32-x/SIZE_OF_GRIDS );
	cgy = ( int ) ( 32-y/SIZE_OF_GRIDS );
	if ( ! maps[id][cgx][cgy]->loaded )
	  maps[id][cgx][cgy]->Load();
	maph = maps[id][cgx][cgy]->getheight(x,y,z);
    return Py_BuildValue ( "f",maph );
}
static PyObject * gridmap_init ( PyObject *self,PyObject*args )
{
    currmap = NULL;
    cgx = -1;
    cgy = -1;

}
static PyMethodDef gridmapMethods[] =
{
    {"getheight",gridmap_getheight,METH_VARARGS,"Nodoc"},
    {"los",gridmap_los,METH_VARARGS,"Nodoc"},
    {NULL,NULL,0,NULL}
};
PyMODINIT_FUNC
initgridmap ( void )
{
	initmaps();
    ( void ) Py_InitModule ( "gridmap", gridmapMethods );
}
