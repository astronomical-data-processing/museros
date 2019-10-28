# muserOS - fits
# museruvfits - generate uvfits file
# muserreaduvfits - read uvfits file
#

INCLUDE_DIRECTORIES(
${CMAKE_SOURCE_DIR}/src/ephem
)

LINK_DIRECTORIES(
${CMAKE_SOURCE_DIR}/src/ephem
)

ADD_EXECUTABLE(museruvfits museruvfits.c muserrawdata.c uvfits.c)
TARGET_LINK_LIBRARIES(museruvfits novas cfitsio m)

ADD_EXECUTABLE(muserreaduvfits muserreaduvfits.c muserrawdata.c uvfits.c)
TARGET_LINK_LIBRARIES(muserreaduvfits novas cfitsio m)

ADD_EXECUTABLE(musersumuvfits musersumuvfits.c muserrawdata.c uvfits.c fastbit.c)
TARGET_LINK_LIBRARIES(musersumuvfits novas cfitsio m fastbit)

ADD_EXECUTABLE(muserscanrawdata muserscanrawdata.c muserrawdata.c fastbit.c )
TARGET_LINK_LIBRARIES(muserscanrawdata novas cfitsio m fastbit)

ADD_EXECUTABLE(musertest musertest.c muserrawdata.c fastbit.c )
TARGET_LINK_LIBRARIES(musertest novas cfitsio m fastbit)

ADD_EXECUTABLE(fastbittest fastbittest.c fastbit.c)
TARGET_LINK_LIBRARIES(fastbittest m fastbit)

INSTALL(TARGETS museruvfits DESTINATION bin)
INSTALL(TARGETS muserreaduvfits DESTINATION bin)
INSTALL(TARGETS musersumuvfits DESTINATION bin)
INSTALL(TARGETS muserscanrawdata DESTINATION bin)
INSTALL(TARGETS musertest DESTINATION bin)
