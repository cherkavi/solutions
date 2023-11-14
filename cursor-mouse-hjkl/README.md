# hjkl for managing cursor and mouse
current solution works ( tested ) for Ubuntu OS.

## cursor with [caps lock]+hjkl
```sh
sudo vim /usr/share/X11/xkb/symbols/us
```
find out block 
```properties
xkb_symbols "basic" {
    ...
    key <BKSL> {        [ backslash,         bar        ]       };
```
and add next lines
```properties
    key <AC06> {        [         h, H, Left            ]       };
    key <AC07> {        [         j, J, Down            ]       };
    key <AC08> {        [         k, K, Up              ]       };
    key <AC09> {        [         l, L, Right           ]       };
    key <AD07> {        [         u, U, Home            ]       };
    key <AB07> {        [         m, M, End             ]       };
    key <AC10> {        [ semicolon, colon, KP_Enter    ]       };
    key <AD06> {        [         y, Y, BackSpace       ]       };
    key <AB06> {        [         n, N, Delete          ]       };
    key <AD08> {        [         i, I, Page_Up        ]       };
    key <AB08> {        [     comma, less, Page_Down   ]       };
    key <CAPS> { [ ISO_Level3_Shift ] };
}
```
alternative solution
```sh
sudo apt-get install xbindkeys xautomation 

xbindkeys -mk
# press your Shift+Backspace shortcut
# m:0x11 + c:22        
# Shift+Mod2 + BackSpace 

# xbindkeys --defaults > $HOME/.xbindkeysrc  
vim $HOME/.xbindkeysrc  

# "xte 'key Delete'"
# m:0x11 + c:22        
# Shift+Mod2 + BackSpace  

```



## mouse with [super]+[alt]+hjkl
```sh
sudo apt install xdotool
```
gnome-custom-keybindings.properties
```properties
[custom0]
binding='<Super>Return'
command='/usr/bin/terminator'
name='terminal'

[custom1]
binding='<Alt><Super>h'
command='xdotool mousemove_relative --sync -- -10 0'
name='mouse-left'

[custom2]
binding='<Alt><Super>l'
command='xdotool mousemove_relative --sync 10 0'
name='mouse-right'

[custom3]
binding='<Alt><Super>j'
command='xdotool mousemove_relative --sync 0 10'
name='mouse-down'

[custom4]
binding='<Alt><Super>k'
command='xdotool mousemove_relative --sync 0 -10'
name='mouse-up'

[custom5]
binding='<Alt><Super>semicolon'
command='xdotool click 1'
name='mouse-click'
```
apply gnome settings ( or just do it manually via UI )
```sh
dconf load /org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/ < gnome-custom-keybindings.properties
```
in case of issue with moving mouse, pls check your `/etc/gdm3/custom.conf`
```
WaylandEnable=false
```
