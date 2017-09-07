#!/usr/bin/env python

import os, re;
from subprocess import check_call;

def build_zlib():
	zlib_file = 'zlib-1.2.11.tar.gz'
	zlib_dir = 'zlib-1.2.11'
	zlib_out = 'zlib'

	print("Deleting zlib...")
	check_call(['rm', '-rf', zlib_file, zlib_dir, zlib_out])

	print("Fetching zlib...")
	check_call(['wget', 'https://zlib.net/' + zlib_file, '-O' + zlib_file])
	check_call(['tar','xfz', zlib_file])

	print("Building zlib...")
	os.chdir(zlib_dir)
	env = os.environ.copy()
	env['prefix'] = '../' + zlib_out
	check_call(['./configure', '--static'], env=env)
	check_call(['make'])
	check_call(['make', 'install'])
	os.chdir('..')

	print("Fixing up zlib (removing extra stuff)...")
	check_call(['rm', '-rf', zlib_out + "/lib/pkgconfig", zlib_out + "/share"])


def build_libpng():
	png_file = 'libpng-1.6.32.tar.gz'
	png_dir = 'libpng-1.6.32'
	png_out = 'libpng'

	print("Deleting libpng...")
	check_call(['rm', '-rf', png_file, png_dir, png_out])

	print("Fetching libpng...")
	check_call(['wget', 'http://prdownloads.sourceforge.net/libpng/' + png_file + '?download', '-O' + png_file])
	check_call(['tar','xfz', png_file])

	prefix = os.getcwd() + '/' + png_out;
	os.chdir(png_dir)
	env = os.environ.copy()
	env['CPPFLAGS'] = '-L../zlib/lib -I../zlib/include'
	env['LDFLAGS'] = '-L../zlib/lib'
	check_call(['./configure',
		'--prefix=' + prefix,
		'--with-zlib-prefix=../zlib',
		'--disable-shared'], env=env);
	check_call(['make'])
	check_call(['make', 'install'])
	os.chdir('..')

	print("Fixing up libpng (removing extra stuff)...")
	check_call(['rm', '-rf', png_out + "/bin", png_out + "/lib/pkgconfig", png_out + "/share"])


def build_libogg():
	libogg_dir = 'libogg-1.3.0'
	check_call(['rm', '-rf', libogg_dir])
	check_call(['git', 'checkout', libogg_dir])
	prefix = os.getcwd() + '/out';
	os.chdir(libogg_dir)
	env = os.environ.copy()
	env['CFLAGS'] = '-mmacosx-version-min=' + min_osx_version
	check_call(['./configure', '--prefix=' + prefix, '--disable-shared'], env=env);
	check_call(['make'])
	check_call(['make', 'install'])

	os.chdir('..')
	check_call(['rm', '-rf', libogg_dir])
	check_call(['git', 'checkout', libogg_dir])

def build_libvorbis():
	libvorbis_dir = 'libvorbis-1.3.3'
	check_call(['rm', '-rf', libvorbis_dir])
	check_call(['git', 'checkout', libvorbis_dir])
	prefix = os.getcwd() + '/out'
	ogg = os.getcwd() + '/out'

	os.chdir(libvorbis_dir)
	env = os.environ.copy()
	env['CFLAGS'] = '-mmacosx-version-min=' + min_osx_version
	check_call(['./configure', '--prefix=' + prefix, '--disable-shared', '--with-ogg=' + ogg], env=env)
	check_call(['make'])
	check_call(['make', 'install'])
	os.chdir('..')

	check_call(['rm', '-rf', libvorbis_dir])
	check_call(['git', 'checkout', libvorbis_dir])

def build_glm():
	glm_dir = 'glm-git'
	glm_out = 'glm'

	print("Cleaning up old glm...")
	check_call(['rm', '-rf', glm_dir, glm_out])

	print("Cloning glm...")
	check_call(['git', 'clone', 'https://github.com/g-truc/glm', glm_dir])

	print("Copying glm to output directory...")
	check_call(['mkdir', '-p', glm_out + '/include'])
	check_call(['cp', '-r', glm_dir + '/glm', glm_out + '/include/glm'])

	print("Fixing up glm (removing extra stuff)...")
	check_call(['rm', '-rf', glm_out + '/include/glm/CMakeLists.txt'])


def build_sdl():
	sdl_file = 'SDL2-2.0.5.tar.gz'
	sdl_dir = 'SDL2-2.0.5'
	sdl_out = 'SDL2'

	print("Deleting SDL...")
	check_call(['rm', '-rf', sdl_file, sdl_dir, sdl_out])

	print("Fetching SDL...")
	check_call(['wget', 'https://www.libsdl.org/release/' + sdl_file, '-O' + sdl_file])
	check_call(['tar','xfz', sdl_file])

	print("Building SDL...")
	prefix = os.getcwd() + '/SDL2'

	os.mkdir(sdl_dir + '/build')
	os.chdir(sdl_dir + '/build')
	env = os.environ.copy()
	check_call(['../configure', '--prefix=' + prefix,
		'--disable-shared', '--enable-static',
		'--disable-render', '--disable-haptic', '--disable-file', '--disable-filesystem', '--disable-loadso', '--disable-power',
		'--enable-sse2',
		'--disable-oss', '--enable-alsa',
		'--disable-esd', '--disable-pulseaudio', '--disable-arts',
		'--disable-nas', '--disable-diskaudio', '--disable-dummyaudio',
		'--enable-video-x11',
		'--disable-video-cocoa',
		'--disable-video-directfb',
		'--disable-video-dummy',
		'--enable-video-opengl',
		'--enable-video-opengles',
		'--disable-input-tslib',
		'--enable-pthreads',
		'--enable-pthread-sem',
		'--disable-directx',
		'--disable-render',
		'--enable-sdl-dlopen',
	],env=env)
	check_call(['make'])
	check_call(['make', 'install'])
	os.chdir('../..')

	print("Fixing up SDL (munging config script, directories)...")
	check_call(['rm', '-rf', sdl_out + "/lib/cmake", sdl_out + "/lib/pkgconfig", sdl_out + "/share"])
	with open(sdl_out + "/bin/sdl2-config", 'r') as f:
		found_prefix = False
		out = []
		for line in f:
			if re.match('^prefix=.*$', line) != None:
				assert(not found_prefix)
				out.append("prefix=kit-libs-linux/" + sdl_out + "\n")
				found_prefix = True
			else:
				out.append(line)
		assert(found_prefix)
	with open(sdl_out + "/bin/sdl2-config", 'w') as f:
		f.write("".join(out))

build_glm()
build_zlib()
build_libpng()
build_sdl()
