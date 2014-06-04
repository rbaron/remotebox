Remotebox
=========

A remote control plugin for [Rhythmbox](http://projects.gnome.org/rhythmbox/). It was developed to be used in conjunction with the [Remotebox](https://play.google.com/store/apps/details?id=net.raphaelbaron.Remotebox) android app, but can also be used by any application that can communicate via TCP sockets.

Installation
------------
###For GTK3 / Rhythmbox 3.x users
Copy the files `gtk3/3.x/remotebox.py` and `gtk3/3.x/remotebox.plugin` to a folder called "Remotebox" on your Rhythmbox plugins directory, usually `~/.local/share/rhythmbox/plugins/`.

To automate the process, copy the following and execute on a terminal console:

```bash
$  plugin_path=$HOME"/.local/share/rhythmbox/plugins/remotebox/" && \
   mkdir -p "$plugin_path" && \
   cd "$plugin_path" || exit && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk3/3.x/remotebox.plugin && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk3/3.x/remotebox.py
```

Afterwards, __make sure the plugin is enabled in Rhythmbox__. Go to Edit > Plugins and make sure "Remotebox" is checked.

###For GTK3 / Rhythmbox 2.9x users
Copy the files `gtk3/2.9x/remotebox.py` and `gtk3/2.9x/remotebox.plugin` to a folder called "Remotebox" on your Rhythmbox plugins directory, usually `~/.local/share/rhythmbox/plugins/`.

To automate the process, copy the following and execute on a terminal console:

```bash
$  plugin_path="$HOME/.local/share/rhythmbox/plugins/remotebox/" && \
   mkdir -p "$plugin_path" && \
   cd "$plugin_path" || exit && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk3/2.9x/remotebox.plugin && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk3/2.9x/remotebox.py
```

Afterwards, __make sure the plugin is enabled in Rhythmbox__. Go to Edit > Plugins and make sure "Remotebox" is checked.

###For GTK2 / Rhythmbox 0.x users

The support is experimental (please contribute!). For instructions on how to install, see [Installation](https://github.com/raaapha/remotebox/wiki/Installation).

Usage
-----

If you're using it with the android client, you don't have to do anything else. Just run the app and you're set!

If you want to use this plugin for controlling Rhythmbox through a TCP socket, there is a section just for you at [Usage/Available commands](https://github.com/raaapha/remotebox/wiki/Usage---Commands).

Contribute
----------

Please feel free to send in suggestions and pull requests. If you have written a client which is compatible with this plugin, tell me about it and I'll mention it here!

License
-------

[MIT](http://opensource.org/licenses/MIT).
