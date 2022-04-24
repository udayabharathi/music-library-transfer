# music-library-transfer
Transfer Apple Music Library to Spotify Liked Songs.

### Steps to do:
- Go to https://soundiiz.com and sign up.
- Connect Spotify and Apple Music to Soundiiz.
- Press F12 and Navigate to tracks section.
- Under network section in dev console, filter XHR requests and search for endpoint ending with `/tracks`. Click any one of it and check for `authorization` in Request Headers. Copy the part next to `Bearer ` and keep it safe.
- Now in Soundiiz, Filter Apple music songs and select any one of the songs and `right click` -> `Add to library on...` and select `Spotify`. In parallel, in network console, you'll be able to see a request ending with `/add`. Click on it and copy the request header value of `x-csrf-token`.
- Run the script with both the token as arguments for initiating the transfer process.

### How to run the script:
- Run `/path/to/python -m pip install -r requirements.txt`
- Run `/path/to/python apple_music_to_spotify.py -b <BEARER_TOKEN_WITHOUT_BEARER_PREFIX> -c <CSRF_TOKEN>`
