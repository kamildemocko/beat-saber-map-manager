[Setup]
AppName=Beat Saber Map Manager
AppVersion=1.1.1
DefaultDirName={userappdata}\Beat Saber Map Manager
DefaultGroupName=Beat Saber Map Manager
DisableDirPage=yes
PrivilegesRequired=lowest
OutputBaseFilename=bsmm-setup-{#SetupSetting("AppVersion")}

[Files]
Source: "dist\Beat Saber Map Manager\Beat Saber Map Manager.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "dist\Beat Saber Map Manager\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Beat Saber Map Manager"; Filename: "{app}\Beat Saber Map Manager.exe"
Name: "{userdesktop}\Beat Saber Map Manager"; Filename: "{app}\Beat Saber Map Manager.exe"
