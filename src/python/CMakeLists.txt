# MUSEROS - src
set(CMAKE_BUILD_TYPE Debug)

# Two subdirectories included

# All Python files should be copied to DESTINATION/scripts

#INSTALL(PROGRAMS scripts/museros.sh DESTINATION .
#     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY scripts/ DESTINATION python
     PATTERN ".*" EXCLUDE
     PATTERN "./svn" EXCLUDE
     PATTERN "novas.py" EXCLUDE
     PATTERN "_*.so" EXCLUDE
     PATTERN "*.TXT" EXCLUDE
     PATTERN "*.sh" EXCLUDE
     PATTERN "*.txt" EXCLUDE
     PATTERN "*.py"
     PATTERN "*.xml"
     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY pymuser/ DESTINATION python/pymuser
     PATTERN ".*" EXCLUDE
     PATTERN "./svn" EXCLUDE
     PATTERN "novas.py" EXCLUDE
     PATTERN "_*.so" EXCLUDE
     PATTERN "*.TXT" EXCLUDE
     PATTERN "*.sh" EXCLUDE
     PATTERN "*.txt" EXCLUDE
     PATTERN "*.py"
     PATTERN "*.xml"
     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY musercli/ DESTINATION python/musercli
     PATTERN ".*" EXCLUDE
     PATTERN "./svn" EXCLUDE
     PATTERN "novas.py" EXCLUDE
     PATTERN "_*.so" EXCLUDE
     PATTERN "*.TXT" EXCLUDE
     PATTERN "*.sh" EXCLUDE
     PATTERN "*.txt" EXCLUDE
     PATTERN "*.py"
     PATTERN "*.xml"
     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY ocscripts/ DESTINATION python/ocscripts
     PATTERN ".*" EXCLUDE
     PATTERN "./svn" EXCLUDE
     PATTERN "novas.py" EXCLUDE
     PATTERN "_*.so" EXCLUDE
     PATTERN "*.TXT" EXCLUDE
     PATTERN "*.sh" EXCLUDE
     PATTERN "*.txt" EXCLUDE
     PATTERN "*.py"
     PATTERN "*.xml"
     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY monitor/ DESTINATION python/monitor
     PATTERN ".*" EXCLUDE
     PATTERN "./svn" EXCLUDE
     PATTERN "novas.py" EXCLUDE
     PATTERN "_*.so" EXCLUDE
     PATTERN "*.TXT" EXCLUDE
     PATTERN "*.sh" EXCLUDE
     PATTERN "*.txt" EXCLUDE
     PATTERN "*.py"
     PATTERN "*.xml"
     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY opencluster/ DESTINATION python/opencluster
     PATTERN ".*" EXCLUDE
     PATTERN "./svn" EXCLUDE
     PATTERN "novas.py" EXCLUDE
     PATTERN "_*.so" EXCLUDE
     PATTERN "*.TXT" EXCLUDE
     PATTERN "*.sh" EXCLUDE
     PATTERN "*.txt" EXCLUDE
     PATTERN "*.py"
     PATTERN "*.xml"
     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

#INSTALL(PROGRAMS scripts/museros.py DESTINATION scripts
#     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

