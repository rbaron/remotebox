remotebox
=========

Remotebox is a plugin for rhythmbox [Rhythmbox](http://projects.gnome.org/rhythmbox/) which opens a socket at port 30666 and listens for remote commands. It was developed as a backend for [Remotebox](http://not.online.yet/) android app, but it can be used by any application that supports communication via TCP sockets.

Installation
------------

###For GTK3 / Rhythmbox 2.9x users
Copy the files `gtk3/remotebox.py` and `gtk3/remotebox.plugin` to a folder called "remotebox" on your Rhythmbox plugins directory, usually `~/.local/share/rhythmbox/plugins/`. If you want to automate this process, simply type

```bash
>  REMOTEBOXPATH=$HOME"/.local/share/rhythmbox/plugins/remotebox/" && \
   mkdir -p $REMOTEBOXPATH && \
   cd $REMOTEBOXPATH && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk3/remotebox.plugin && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk3/remotebox.py
```

on your terminal. Afterwards, make sure the plugin is enabled in Rhythmbox. Go to Edit > Plugins and make sure "remotebox" is checked.

###For GTK2 / Rhythmbox 0.12.x users
Copy the files `gtk2/remotebox.py` and `gtk2/remotebox.rb-plugin` to a folder called "remotebox" on your Rhythmbox plugins directory, usually `~/.local/share/rhythmbox/plugins/`. If you want to automate this process, simply type

```bash
>  REMOTEBOXPATH=$HOME"/.local/share/rhythmbox/plugins/remotebox/" && \
   mkdir -p $REMOTEBOXPATH && \
   cd $REMOTEBOXPATH && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk2/remotebox.rb-plugin && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk2/remotebox.py
```

on your terminal. Afterwards, make sure the plugin is enabled in Rhythmbox. Go to Edit > Plugins and make sure "remotebox" is checked.

###For GTK2 / Rhythmbox <= 0.11.x users
Copy the files `gtk2/remotebox.py` and `gtk2/remotebox.rb-plugin` to a folder called "remotebox" on your Rhythmbox plugins directory, usually `~/.gnome2/rhythmbox/plugins/`. If you want to automate this process, simply type

```bash
>  REMOTEBOXPATH=$HOME"/.gnome2/rhythmbox/plugins/remotebox/" && \
   mkdir -p $REMOTEBOXPATH && \
   cd $REMOTEBOXPATH && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk2/remotebox.rb-plugin && \
   wget https://raw.github.com/raaapha/remotebox/master/gtk2/remotebox.py
```

on your terminal. Afterwards, make sure the plugin is enabled in Rhythmbox. Go to Edit > Plugins and make sure "remotebox" is checked.

Usage
-----

As said above, you can use remotebox to control your Rhythmbox remotely through a TCP socket. Once the plugin is installed and Rhythmbox is running, a typical remote session might be as follows (using netcat as a client, assuming Rhythmbox us running locally and playing a file):

```bash
 $ netcat localhost 30666

next # -> Client request
ok # -> remotebox response

prev
ok

vol
1.0

vol 0.3
ok

vol
0.3

pause 
ok

goto file://path/to/a/file.mp3
ok

stop
ok

list # -> Request the list of all files on Rhythmbox library
... # -> Response is a xml-formatted string. See "Avaliable commands" for more information.
```

Available commands
------------------

<table>
<tr><th>Request</th><th>Response</th><th>Explanation</th></tr>
<tr><td>play</td><td>`ok\n`</td><td>If there isn't any file selected, the response is `Error on play: no track selected!`</td></tr>
<tr><td>pause</td><td>`ok\n`</td><td></td></tr>
<tr><td>stop</td><td>`ok\n`</td><td></td></tr>
<tr><td>next</td><td>`ok\n`</td><td></td></tr>
<tr><td>prev</td><td>`ok\n`</td><td></td></tr>
<tr><td>vol</td><td>`0.9\n`</td><td>The response is the current volume setting, a float point between 0.0 and 1.0</td></tr>
<tr><td>vol 0.7</td><td>`ok\n`</td><td>Sets the volume to a float point between 0.0 and 1.0. If the requested setting is invalid, returns `Invalid volume setting.`</td></tr>
<tr><td>goto file://path/to/a/file.mp3</td><td>`ok\n`</td><td>Plays the specified file. If it doens't exist, return ``</td></tr>
<tr><td>list</td><td>XML-formatted string containing base64 encoded information about the files on rhythmbox library.</td><td>See example below</td></tr>
</table>

###Example of a xml-formatted file list in response to a `list` request###

```xml
<xml version='1.0' encoding='utf-8'>
  <tracks>
    <track>
      <artist>VGhlIEJlYXRsZXMK</artist>
      <title>V2l0aCBhIGxpdHRsZSBoZWxwIGZyb20gbXkgZnJpZW5kcwo=</title>
      <album>U2d0LiBQZXBwZXLigJlzIExvbmVseSBIZWFydHMgQ2x1YiBCYW5kCg==</album>
      <url>ZmlsZTovL215L2F1ZGlvL2ZvbGRlci90aGUlMjBiZWF0bGVzJTIwLSUyMHdpd
          GglMjBhJTIwbGl0dGxlJTIwaGVscCUyMGZyb20lMjBteSUyMGZyaWVuZHMubXAzCg==
      </url>
    </track>
    <track>
      <artist>VGhlIEJlYXRsZXMK</artist>
      <title>THVjeSBpbiB0aGUgc2t5IHdpdGggZGlhbW9uZHMK</title>
      <album>U2d0LiBQZXBwZXLigJlzIExvbmVseSBIZWFydHMgQ2x1YiBCYW5kCg==</album>
      <url>ZmlsZTovL215L2F1ZGlvL2ZvbGRlci90aGUlMjBiZWF0bGVzJTIwLSUyMGx1Y
          3klMjBpbiUyMHRoZSUyMHNreSUyMHdpdGglMjBkaWFtb25kcy5tcDMK
      </url>
    </track>
    .
    .
    .
  </tracks>
</xml>

```
The values in every field (`<artist>`, `<title>`, `<album>`, `<url>`) are base64 encoded uft8 strings. If we decode these fields, we get:

```xml
<xml version='1.0' encoding='utf-8'>
  <tracks>
    <track>
      <artist>The Beatles</artist>
      <title>With a little help from my friends</title>
      <album>Sgt. Pepper’s Lonely Hearts Club Band</album>
      <url>file://my/audio/folder/the%20beatles%20-%20with%20a%20little%20help%20from%20my%20friends.mp3</url>
    </track>
    <track>
      <artist>The Beatles</artist>
      <title>Lucy in the sky with diamonds</title>
      <album>Sgt. Pepper’s Lonely Hearts Club Band</album>
      <url>file://my/audio/folder/the%20beatles%20-%20lucy%20in%20the%20sky%20with%20diamonds.mp3</url>
    </track>
    .
    .
    .
  </tracks>
</xml>

```

Contribute
----------

Please feel free to add suggestions. If you have written a client which is compatible with this plugin, tell me and I'll mention it here! :)

License
-------

[MIT](http://opensource.org/licenses/MIT).
