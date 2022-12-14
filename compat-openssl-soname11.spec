Name:           compat-openssl-soname11
Version:        1.1.1q
Release:        110
License:        OpenSSL
Summary:        Secure Socket Layer
Url:            http://www.openssl.org/
Group:          libs/network
Source0:        https://www.openssl.org/source/openssl-1.1.1q.tar.gz
BuildRequires:  zlib-dev
BuildRequires:  zlib-dev32
BuildRequires:  util-linux-extras
BuildRequires:  util-linux-bin
BuildRequires:  gcc-dev32
BuildRequires:  gcc-libgcc32
BuildRequires:  gcc-libstdc++32
BuildRequires:  glibc-dev32
BuildRequires:  glibc-libc32
BuildRequires:  perl(Test::More)

Requires:       ca-certs
Requires:       p11-kit

Patch1: 0001-Use-clearlinux-CFLAGS-during-build.patch
Patch2: 0002-Hide-a-symbol-from-Steam.patch
Patch3: 0003-Use-OS-provided-copy-of-openssl.cnf-as-fallback.patch


%description
Secure Socket Layer.

%package lib
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network
Requires:       p11-kit

%description lib
Secure Socket Layer.

%package dev
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel

%description dev
Secure Socket Layer.

%package extras
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel
Requires:	c_rehash

%description extras
Secure Socket Layer.

%package filemap
Summary: filemap components for the openssl package.
Group: Default

%description filemap
filemap components for the openssl package.

%package lib32
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network

%description lib32
Secure Socket Layer.

%package dev32
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel

%description dev32
Secure Socket Layer.

%package doc
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          doc

%description doc
Secure Socket Layer.

%prep
%setup -q -n openssl-1.1.1q
%patch1 -p1
%patch2 -p1
%patch3 -p1


pushd ..
cp -a openssl-1.1.1q build32
cp -a openssl-1.1.1q buildavx2
popd


%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="$CFLAGS -flto=8 -fsemantic-interposition -O3"
export CXXFLAGS="$CXXFLAGS -flto=8 -ffunction-sections -fsemantic-interposition -O3 "
export CXXFLAGS="$CXXFLAGS -flto=8 -fsemantic-interposition -O3 -falign-functions=32  "
export CFLAGS_GENERATE="$CFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export FCFLAGS_GENERATE="$FCFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export FFLAGS_GENERATE="$FFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export CXXFLAGS_GENERATE="$CXXFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export CFLAGS_USE="$CFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export FCFLAGS_USE="$FCFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export FFLAGS_USE="$FFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export CXXFLAGS_USE="$CXXFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export LDFLAGS_GENERATE="$LDFLAGS"
export LDFLAGS_USE="$LDFLAGS"

./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3    \
 --prefix=/usr \
 --openssldir=/etc/ssl \
 --libdir=lib64

# parallel build is broken
make depend
make

pushd ../build32
export CFLAGS="$CFLAGS -m32 -fno-lto -mstackrealign"
export LDFLAGS="$LDFLAGS -m32 -fno-lto -mstackrealign"
export CXXFLAGS="$CXXFLAGS -m32 -fno-lto -mstackrealign"
i386 ./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3 no-asm  \
 --prefix=/usr \
 --openssldir=/etc/ssl \
 --libdir=lib32 
make depend
make
popd

%install

CFLAGS_ORIG="$CFLAGS"
LDFLAGS_ORIG="$LDFLAGS"
CXXFLAGS_ORIG="$CXXFLAGS"

pushd ../build32
export CFLAGS="$CFLAGS_ORIG -m32 -fno-lto -mstackrealign"
export LDFLAGS="$LDFLAGS_ORIG -m32 -fno-lto -mstackrealign"
export CXXFLAGS="$CXXFLAGS_ORIG -m32 -fno-lto -mstackrealign"
make  DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install
pushd %{buildroot}/usr/lib32/pkgconfig
for i in *.pc ; do cp $i 32$i ; done
popd
popd

export CFLAGS="$CFLAGS_ORIG -m64 -flto"
export LDFLAGS="$LDFLAGS_ORIG -m64 -flto"
export CXXFLAGS="$CXXFLAGS_ORIG -m64 -flto"
make  DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install

install -D -m0644 apps/openssl.cnf %{buildroot}/usr/share/defaults/ssl11/openssl.cnf
rm -rf %{buildroot}*/etc/ssl
rm -rf %{buildroot}*/usr/lib64/*.a
rm -rf %{buildroot}*/usr/share/doc/openssl/html

%check
#make test

%files
%exclude /usr/bin/openssl
/usr/share/defaults/ssl11/openssl.cnf

%files lib
/usr/lib64/libcrypto.so.1.1
/usr/lib64/libssl.so.1.1
/usr/lib64/engines-1.1/afalg.so
/usr/lib64/engines-1.1/capi.so
/usr/lib64/engines-1.1/padlock.so

%files lib32
/usr/lib32/libcrypto.so.1.1
/usr/lib32/libssl.so.1.1
/usr/lib32/engines-1.1/afalg.so
/usr/lib32/engines-1.1/capi.so
/usr/lib32/engines-1.1/padlock.so

%files dev
%exclude /usr/include/openssl/*.h
%exclude /usr/lib64/libcrypto.so
%exclude /usr/lib64/libssl.so
%exclude /usr/lib64/pkgconfig/libcrypto.pc
%exclude /usr/lib64/pkgconfig/libssl.pc
%exclude /usr/lib64/pkgconfig/openssl.pc

%files extras
%exclude /usr/bin/c_rehash

%files filemap
%defattr(-,root,root,-)

%files dev32
%exclude /usr/lib32/libcrypto.so
%exclude /usr/lib32/libssl.so
%exclude /usr/lib32/pkgconfig/32libcrypto.pc
%exclude /usr/lib32/pkgconfig/32libssl.pc
%exclude /usr/lib32/pkgconfig/32openssl.pc
%exclude /usr/lib32/pkgconfig/libcrypto.pc
%exclude /usr/lib32/pkgconfig/libssl.pc
%exclude /usr/lib32/pkgconfig/openssl.pc
%exclude /usr/lib32/libcrypto.a
%exclude /usr/lib32/libssl.a

%files doc
%exclude /usr/share/man/man1/*
%exclude /usr/share/man/man3/*
%exclude /usr/share/man/man5/*
%exclude /usr/share/man/man7/*
