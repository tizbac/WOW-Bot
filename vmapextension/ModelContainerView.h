#ifndef _MODELCONTAINERVIEW_H
#define _MODELCONTAINERVIEW_H

#include <G3D/G3DAll.h>
#include <G3D/System.h>
#include "ModelContainer.h"
#include "DebugCmdLogger.h"
#include "VMapManager.h"
#include "AABox.h"
#include "CollisionDetection.h"  
#include "debug.h"
#include "GCamera.h"  
#include "Plane.h" 
#include "Ray.h"           
#include "stringutils.h"  
#include "Triangle.h "     
#include "Vector3.h"
#include "Array.h"  
#include "CoordinateFrame.h"     
#include "format.h"   
#include "Line.h"     
#include "platform.h" 
#include "RegistryUtil.h" 
#include "System.h"  
#include "Vector2.h"   
#include "Vector3int16.h"
#include "Box.h"    
#include "Crypto.h"              
#include "g3dmath.h"  
#include "Matrix3.h" 
#include "Quat.h"      
#include "Sphere.h"       
#include "Table.h"      
#include "Vector2int16.h"
#include "Vector4.h"




namespace VMAP
{
	//==========================================


	//==========================================

	class ModelContainerView : 
		public G3D::GApp
	{
	private:
        SkyRef              iSky;
        LightingRef         iLighting;
        SkyParameters       iSkyParameters;

		VARAreaRef iVARAreaRef;
		Table<std::string , VAR*> iTriVarTable;
		Table<std::string , Array<int> > iTriIndexTable;

		VARAreaRef iVARAreaRef2;
        VAR iTriDebugVar;
        Array<Vector3> iVTriDebugArray;
        Array<int> iTriDebugArray;

        //Array<int> iLineIndexArray;

		GApp* i_App;
		CommandFileRW iCommandFileRW;
		Array<Command> iCmdArray;
		int iCurrCmdIndex;

		VMapManager* iVMapManager;

		Vector3 iPos1;
		Vector3 iPos2;
		Color3 iColor;
		bool iDrawLine;
		int iInstanceId;
        bool iPosSent;
        Array<Command> iPrevLoadCommands;
	private:
		Vector3 convertPositionToMangosRep(float x, float y, float z) const;

	public:
		ModelContainerView(const G3D::GApp::Settings& settings);

		~ModelContainerView(void);

		void addModelContainer(const std::string& pName,const ModelContainer* pModelContainer);
		void removeModelContainer(const std::string& pName, const ModelContainer* pModelContainer);
		void setViewPosition(const Vector3& pPosition);

		void onGraphics(RenderDevice* rd, Array<PosedModelRef> &posed3D, Array<PosedModel2DRef> &posed2D);
        virtual void onInit();
        void init();
		void cleanup();
		void onUserInput(UserInput* ui);

		void fillRenderArray(const SubModel& pSm,Array<TriangleBox> &pArray, const TreeNode* pTreeNode);
		void fillVertexAndIndexArrays(const SubModel& pSm, Array<Vector3>& vArray, Array<int>& iArray);

		bool loadAndShowTile(int pMapId, int x, int y);
		void showMap(int pMapId, int x, int y);

		void showMap(MapTree* mt, std::string dirFileName);
		bool loadAndShowTile(int pMapId);


		void processCommand();

	};

	//==========================================
	//==========================================
}

#endif
