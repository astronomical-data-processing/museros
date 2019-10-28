# CSRHOS - fusion subdirectory
# Other example files

#set( CMAKE_C_FLAGS " -O2 -fPIC -flat_namespace -arch x86_64")
#set( CMAKE_MODULE_LINK_FLAGS " -O2 -fPIC -flat_namespace -arch x86_64")

#ADD_EXECUTABLE(fusionServer fusionServer.c)
#TARGET_LINK_LIBRARIES(fusionServer mysqlclient czmq)

#ADD_EXECUTABLE(fusionClient fusionClient.c)
#TARGET_LINK_LIBRARIES(fusionClient czmq)

include_directories (${CMAKE_CURRENT_SOURCE_DIR})
#Message(${CMAKE_BINARY_DIR})

#INSTALL(TARGETS fusionServer DESTINATION bin)
#INSTALL(TARGETS fusionClient DESTINATION bin)
