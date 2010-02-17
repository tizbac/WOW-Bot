#include <stdlib.h>
#include <stdio.h>
#include <iostream>
using namespace std;
typedef unsigned short uint16;
typedef unsigned int uint32;
typedef unsigned char uint8;
typedef int int32;
#define MAP_MAGIC             'SPAM'
#define MAP_VERSION_MAGIC     '5.0w'
#define MAP_AREA_MAGIC        'AERA'
#define MAP_HEIGHT_MAGIC      'TGHM'
#define MAP_LIQUID_MAGIC      'QILM'
#define MAX_HEIGHT            100000.0f                     // can be use for find ground height at surface
#define INVALID_HEIGHT       -100000.0f                     // for check, must be equal to VMAP_INVAL
#define MAP_RESOLUTION 128
#define SIZE_OF_GRIDS 533.333333
struct map_fileheader
{
    uint32 mapMagic;
    uint32 versionMagic;
    uint32 areaMapOffset;
    uint32 areaMapSize;
    uint32 heightMapOffset;
    uint32 heightMapSize;
    uint32 liquidMapOffset;
    uint32 liquidMapSize;
};

#define MAP_AREA_NO_AREA      0x0001

struct map_areaHeader
{
    uint32 fourcc;
    uint16 flags;
    uint16 gridArea;
};

#define MAP_HEIGHT_NO_HEIGHT  0x0001
#define MAP_HEIGHT_AS_INT16   0x0002
#define MAP_HEIGHT_AS_INT8    0x0004

struct map_heightHeader
{
    uint32 fourcc;
    uint32 flags;
    float  gridHeight;
    float  gridMaxHeight;
};

#define MAP_LIQUID_NO_TYPE    0x0001
#define MAP_LIQUID_NO_HEIGHT  0x0002

struct map_liquidHeader
{
    uint32 fourcc;
    uint16 flags;
    uint16 liquidType;
    uint8  offsetX;
    uint8  offsetY;
    uint8  width;
    uint8  height;
    float  liquidLevel;
};

enum ZLiquidStatus
{
    LIQUID_MAP_NO_WATER     = 0x00000000,
    LIQUID_MAP_ABOVE_WATER  = 0x00000001,
    LIQUID_MAP_WATER_WALK   = 0x00000002,
    LIQUID_MAP_IN_WATER     = 0x00000004,
    LIQUID_MAP_UNDER_WATER  = 0x00000008
};

#define MAP_LIQUID_TYPE_NO_WATER    0x00
#define MAP_LIQUID_TYPE_WATER       0x01
#define MAP_LIQUID_TYPE_OCEAN       0x02
#define MAP_LIQUID_TYPE_MAGMA       0x04
#define MAP_LIQUID_TYPE_SLIME       0x08

#define MAP_ALL_LIQUIDS   (MAP_LIQUID_TYPE_WATER | MAP_LIQUID_TYPE_OCEAN | MAP_LIQUID_TYPE_MAGMA | MAP_LIQUID_TYPE_SLIME)

#define MAP_LIQUID_TYPE_DARK_WATER  0x10
#define MAP_LIQUID_TYPE_WMO_WATER   0x20

struct LiquidData
{
    uint32 type;
    float  level;
    float  depth_level;
};

class GridMap
{
    uint32  m_flags;
    // Area data
    uint16  m_gridArea;
    uint16 *m_area_map;
    // Height level data
    float   m_gridHeight;
    float   m_gridIntHeightMultiplier;
    union{
        float  *m_V9;
        uint16 *m_uint16_V9;
        uint8  *m_uint8_V9;
    };
    union{
        float  *m_V8;
        uint16 *m_uint16_V8;
        uint8  *m_uint8_V8;
    };
    // Liquid data
    uint16  m_liquidType;
    uint8   m_liquid_offX;
    uint8   m_liquid_offY;
    uint8   m_liquid_width;
    uint8   m_liquid_height;
    float   m_liquidLevel;
    uint8  *m_liquid_type;
    float  *m_liquid_map;

    bool  loadAreaData(FILE *in, uint32 offset, uint32 size);
    bool  loadHeihgtData(FILE *in, uint32 offset, uint32 size);
    bool  loadLiquidData(FILE *in, uint32 offset, uint32 size);

    // Get height functions and pointers
    typedef float (GridMap::*pGetHeightPtr) (float x, float y) const;
    pGetHeightPtr m_gridGetHeight;
    float  getHeightFromFloat(float x, float y) const;
    float  getHeightFromUint16(float x, float y) const;
    float  getHeightFromUint8(float x, float y) const;
    float  getHeightFromFlat(float x, float y) const;

public:
    GridMap();
    ~GridMap();
    bool  loadData(char *filaname);
    void  unloadData();

    uint16 getArea(float x, float y);
    inline float getHeight(float x, float y) {return (this->*m_gridGetHeight)(x, y);}
    float  getLiquidLevel(float x, float y);
    uint8  getTerrainType(float x, float y);
    ZLiquidStatus getLiquidStatus(float x, float y, float z, uint8 ReqLiquidType, LiquidData *data = 0);
};