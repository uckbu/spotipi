# spotipi

this is a spotify display for a waveshare e-ink display connected to a raspberry pi.

you'll need to clone the git repository, and run **git pull** every time you need to update the files in it.

to begin with, you'll need to run spotify_auth.py.

python3 spotify_auth.py

then, paste the URL it gives you into a browser. copy the redirected link, run spotify_auth.py again, and paste in the **redirect link** you just copied.

after that, run 

python3 spotify_display.py

and youre done!
