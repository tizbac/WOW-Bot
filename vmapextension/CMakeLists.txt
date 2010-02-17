project (vmaps)
include_directories ( . ./G3D /usr/include/python2.6)
add_library(vmaps AABox.cpp                  Plane.cpp
BaseModel.cpp              SubModel.cpp
Box.cpp                    System.cpp
CoordModelMapping.cpp      TileAssembler.cpp
Crypto.cpp                 TreeNode.cpp
DebugCmdLogger.cpp         Triangle.cpp
format.cpp                 Vector3.cpp
ManagedModelContainer.cpp  Vector4.cpp
Matrix3.cpp                VMapFactory.cpp
ModelContainer.cpp         VMapManager.cpp

)

#add_library (vmint SHARED Interface.cxx m_wrap.cxx)
add_executable(test test.cpp)
add_executable(exporter MapConverter.cpp GridMap.cpp)
add_library(gridmap SHARED PythonExtension.cpp GridMap.cpp AABox.cpp Thread.cpp   Utility.cpp              Plane.cpp
BaseModel.cpp              SubModel.cpp
Box.cpp                    System.cpp
CoordModelMapping.cpp      TileAssembler.cpp
Crypto.cpp                 TreeNode.cpp
DebugCmdLogger.cpp         Triangle.cpp
format.cpp                 Vector3.cpp
ManagedModelContainer.cpp  Vector4.cpp
Matrix3.cpp                VMapFactory.cpp
ModelContainer.cpp         VMapManager.cpp)
#add_executable(debugger ModelContainerView.cpp)
link_directories(.)
set_target_properties(vmaps PROPERTIES COMPILE_FLAGS -fPIC)
#set_target_properties(vmint PROPERTIES COMPILE_FLAGS -fPIC)
#target_link_libraries(vmint vmaps)
target_link_libraries(test vmaps IL)
#target_link_libraries(debugger vmaps)