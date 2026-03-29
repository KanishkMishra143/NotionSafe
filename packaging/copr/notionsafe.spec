Name:           notionsafe
Version:        0.1.0
Release:        4%{?dist}
Summary:        A cross-platform desktop app to backup Notion workspaces locally.

License:        MIT
URL:            https://github.com/KanishkMishra143/NotionSafe
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

# Core build tools. The pyproject-rpm-macros will handle other build dependencies.
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel

# Runtime dependencies available in Fedora.
# The package itself will pull in the others from PyPI via its metadata.
Requires:       python3-gobject
Requires:       git-core


%description
NotionSafe is a Python-based application for creating secure, local backups of a Notion workspace.
It features a command-line interface (CLI) and a graphical user interface (GUI) built with PyGObject/GTK4 for Linux.

%prep
# Corrected autosetup macro
%autosetup -n %{name}-%{version}

%build
# Use the modern macro for pyproject.toml projects
%pyproject_build

%install
# Use the modern macro for pyproject.toml projects
%pyproject_install

# Install desktop file and icon
install -D -p -m 0644 assets/logo.png %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.png
install -D -p -m 0644 packaging/common/notionsafe.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md GEMINI.md
%{_bindir}/notionsafe
%{python3_sitelib}/notebackup
%{python3_sitelib}/notionsafe-*.dist-info
%{_datadir}/applications/notionsafe.desktop
%{_datadir}/icons/hicolor/scalable/apps/notionsafe.png

%changelog
* Fri Nov 21 2025 Kanishk Mishra <kanishk.kumar412@example.com> - 0.1.0-4
- Correct %%autosetup macro usage.

* Fri Nov 21 2025 Kanishk Mishra <kanishk.kumar412@example.com> - 0.1.0-3
- Use modern %%pyproject macros for build.

* Fri Nov 21 2025 Kanishk Mishra <kanishk.kumar412@example.com> - 0.1.0-2
- Use pip to install dependencies from PyPI during COPR build.

* Fri Nov 21 2025 Kanishk Mishra <kanishk.kumar412@example.com> - 0.1.0-1
- Initial COPR release
