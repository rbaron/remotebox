remotebox
=========

Remotebox is a plugin for rhythmbox [Rhythmbox](http://projects.gnome.org/rhythmbox/) which opens a socket at port 36666 and listens for remote commands. It was developed as a backend for [Remotebox](http://not.online.yet/) android app, but it can be used by any application that supports communication via TCP sockets.

Installation
------------

To install the plugin, simply copy the files `rhythmbox.py` and `rhythmbox.plugin` to your Rhythmbox plugin directory, usually `~/.local/share/rhythmbox/plugins/`. If you want to automate this process, simply type

```
$> REMOTEBOXPATH="~/.local/share/rhythmbox/plugins/remotebox/" && \
   mkdir -p $REMOTEBOXPATH && \
   cd $REMOTEBOXPATH && \
   wget https://raw.github.com/raaapha/remotebox/master/remotebox.plugin && \
   wget https://raw.github.com/raaapha/remotebox/master/remotebox.py
```

on your terminal.

Usage
-----

As said above, you can use remotebox to control your rhythmbox remotely through a TCP socket. Once the plugin is installed and Rhythmbox is running, a typical remote session might be as follows (using netcat as a client, assuming Rhythmbox us running and playing a file on IP 192.168.0.100):

```shell
 $ netcat 192.168.0.100 36666

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
<td>Request</td><td>Response</td><td>Explanation</td>
<td>play</td><td>`ok\n`</td><td>If there isn't any file selected, the response is ``</td>
<td>pause</td><td>`ok\n`</td><td></td>
<td>stop</td><td>`ok\n`</td><td></td>
<td>next</td><td>`ok\n`</td><td></td>
<td>prev</td><td>`ok\n`</td><td></td>
<td>vol</td><td>`0.9\n`</td><td>The response is the current volume setting, a float point between 0.0 and 1.0</td>
<td>vol 0.7</td><td>`ok\n`</td><td>Set the volume to a float point between 0.0 and 1.0. If the requested setting is invalid, return ``</td>
<td>goto file://path/to/a/file.mp3</td><td>`ok\n`</td><td>Plays the specified file. If it doens't exist, return ``</td>
<td>list</td><td>xml-formatted string containing base64 encoded information about the files on rhythmbox library.</td><td>See example below</td>

###Example of a xml-formatted file list in response to a `list` request###

```
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
      <title>THVjeSBpbiB0aGUgZGt5IHdpdGggZGlhbW9uZHMK</title>
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
The values in everyfield (`<artist>`, `<title>`, `<album>`, `<url>`) are base64 encoded uft8 strings. If we decode these fields, we get:

```
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
      <title>Lucy in the dky with diamonds</title>
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
