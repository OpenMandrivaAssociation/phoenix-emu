%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define sver %(echo %{version} | sed s,'\\.',,g)

Summary:	3DO emulator
Name:		phoenix-emu
Version:	2.3.1
Release:	2
License:	Freeware
Group:		Emulators
Url:		http://www.arts-union.ru/node/23
Source0:	http://www.arts-union.ru/sites/default/files/ph%{sver}-linux-x86.zip
Source1:	http://www.arts-union.ru/sites/default/files/ph%{sver}-linux-x64.zip
BuildRequires:	imagemagick
ExclusiveArch:	%{ix86} x86_64

%description
3DO emulator. Requires a BIOS image.

%files
%{_bindir}/%{name}
%attr(777,-,-) %dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

#----------------------------------------------------------------------------

%prep
%setup -qcT
%ifarch %{ix86}
unzip %{SOURCE0}
%else
unzip %{SOURCE1}
%endif

%build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
install -m 0755 PhoenixEmuProject-%{version} %{buildroot}%{_libdir}/%{name}/%{name}-real

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Phoenix-Emu
Comment=3DO Emulator
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Emulator;
EOF

# install menu icons
for N in 16 32 48 64 128 256;
do
convert logo.png -scale ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

# install wrapper script
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
cd %{_libdir}/%{name}
./%{name}-real "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}
