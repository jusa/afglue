%define strip /bin/true
%define __requires_exclude  ^.*$
%define __find_requires     %{nil}
%global debug_package       %{nil}
%define __provides_exclude_from ^.*$

%define _target_cpu armv7hl

Name:          afglue
Summary:       Android AudioFlinger glue library
Version:       0.0.0
Release:       1
Group:         System/Libraries
License:       TBD
BuildRequires: ubu-trusty
BuildRequires: sudo-for-abuild
BuildRequires: droid-bin-src-full
Source0:       %{name}-%{version}.tgz
AutoReqProv:   no

%description
%{summary}

%package       devel
Summary:       afglue development headers
Group:         System/Libraries
Requires:      afglue = %{version}-%{release}
BuildArch:     noarch

%description   devel
%{summary}

%prep

#%if %{?device_rpm_architecture_string:0}%{!?device_rpm_architecture_string:1}
#echo "device_rpm_architecture_string is not defined"
#exit -1
#%endif

%setup -T -c -n afglue
sudo chown -R abuild:abuild /home/abuild/src/droid/
mv /home/abuild/src/droid/* .
mkdir -p external
pushd external
tar -zxf %SOURCE0
mv afglue* afglue
popd

%build
droid-make -j4 libafglue miniafservice

%install

mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/lib/
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/bin/
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/afglue/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/afglue/

cp out/target/product/*/system/lib/libafglue.so \
    $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/lib/

cp out/target/product/*/system/bin/miniafservice \
    $RPM_BUILD_ROOT/%{_libexecdir}/droid-hybris/system/bin/

cp external/afglue/afglue.h $RPM_BUILD_ROOT/%{_includedir}/afglue/
cp external/afglue/hybris.c $RPM_BUILD_ROOT/%{_datadir}/afglue/

%files
%defattr(-,root,root,-)
%{_libexecdir}/droid-hybris/system/lib/libafglue.so
%{_libexecdir}/droid-hybris/system/bin/miniafservice

%files devel
%defattr(-,root,root,-)
%{_includedir}/afglue/*.h
%{_datadir}/afglue/hybris.c
