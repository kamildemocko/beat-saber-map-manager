[Setup]
AppName=Beat Sabre Map Manager
AppVersion=1.0.0
DefaultDirName={userappdata}\Beat Sabre Map Manager
DefaultGroupName=Beat Sabre Map Manager
DisableDirPage=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\Beat Sabre Map Manager\Beat Sabre Map Manager.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "dist\Beat Sabre Map Manager\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Beat Sabre Map Manager"; Filename: "{app}\Beat Sabre Map Manager.exe"
Name: "{userdesktop}\Beat Sabre Map Manager"; Filename: "{app}\Beat Sabre Map Manager.exe"
