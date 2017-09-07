# kit-libs-linux

Statically-build libraries for games (Linux version).

Includes:
- SDL (a rather stripped-down build)
- glm
- libpng + zlib

All built using `build.py`.

## Using

Clone this directory as a subdirectory of whatever you are building.
Then add compiler/linker arguments as follows:
```
KIT_LIBS = kit-libs-linux

#for zlib:
C++FLAGS += -I$(KIT_LIBS)/zlib/include
LINKLIBS += -L$(KIT_LIBS)/zlib/lib -lz

#for libpng: (note: requires zlib LINKLIBS)
C++FLAGS += -I$(KIT_LIBS)/libpng/include
LINKLIBS += -L$(KIT_LIBS)/libpng/lib -lpng

#for SDL2:
C++FLAGS += `$(KIT_LIBS)/SDL2/bin/sdl2-config --cflags`
LINKLIBS += `$(KIT_LIBS)/SDL2/bin/sdl2-config --static-libs` -framework OpenGL

#for glm:
C++FLAGS += -I$(KIT_LIBS)/glm/include
```

(Note: this is Jam-like syntax; for Make, the variables are `CXXFLAGS` and `LDLIBS`.)

## Notes/Caveats

The `build.py` script hardcodes all library versions except glm, for which it fetches the latest version from git.

If you are maintaining a project that you want to build against local libraries only if they exist, you can simply place the `-I` and `-L` paths for kit-libs before the paths for the system libraries.

For SDL you can modify the `PATH` environment variable in your back-quoted config calls:
```
`PATH=$(KIT_LIBS)/SDL2/bin:$PATH sdl2-config --cflags`
```

Alternatively, you can use shell tests on all options:
```
`if [ -d $(KIT_LIBS) ]; then echo '-Ikit-libs-linux/...'; else echo '-I/usr/local/...'; fi`
```

This can avoid some warnings about non-existent paths from the linker.
