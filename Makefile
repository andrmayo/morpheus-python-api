.PHONY: all install build-morphlib build-greek build-latin build-italian clean clean-morphlib

all:
	@ if [ ! -d morpheus ]; then git clone --depth 1 https://github.com/perseids-tools/morpheus.git; fi
	@ if [ ! -d perseus-morpheus ]; then git clone --depth 1 --filter blob:none --sparse https://github.com/PerseusDL/morpheus.git perseus-morpheus; fi
	@ git -C perseus-morpheus sparse-checkout set stemlib/Italian
	@ cp -r perseus-morpheus/stemlib/Italian morpheus/stemlib
	@ cd morpheus/src && CFLAGS='-std=gnu89 -fcommon' make

install:
	@ cd morpheus/src && make install
	@ $(MAKE) build-morphlib
	cp -r morpheus/bin src/morpheus_python_api/
	cp -r morpheus/stemlib src/morpheus_python_api/
	@ echo "To use bin/cruncher, ensure that MORPHLIB=stemlib is available as an env variable"

build-morphlib: build-greek build-latin build-italian

build-greek:
	@ cd morpheus/stemlib/Greek && PATH="$$PATH:../../bin" MORPHLIB='..' make
	@ cd morpheus/stemlib/Greek && PATH="$$PATH:../../bin" MORPHLIB='..' make

build-latin:
	@ cd morpheus/stemlib/Latin && PATH="$$PATH:../../bin" MORPHLIB='..' make
	@ cd morpheus/stemlib/Latin && PATH="$$PATH:../../bin" MORPHLIB='..' make

build-italian:
	@ cd morpheus/stemlib/Italian && PATH="$$PATH:../../bin" MORPHLIB=".." make -o stemsrc/nom.italian -o stemsrc/vbs.italian

clean: clean-morphlib
	@ cd morpheus/src 2>/dev/null && make clean

clean-morphlib:
	@ cd morpheus/stemlib/Greek 2>/dev/null && make clean
	@ cd morpheus/stemlib/Latin 2>/dev/null && make clean
	@ cd morpheus/stemlib/Italian 2>/dev/null && make clean


