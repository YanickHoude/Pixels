# Pixels

An interactive, shared canvas for online communities to create mosaics. 
It is inspired by the collaborative project and social experiment on Reddit, Place.
The idea is that users can work together in real-time to paint together on an empty canvas.

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used

## API Documentation

### GET /
- A one-time request to retrieve the index.html file and associated Javascript and CSS files.

### GET /pixels
- Requests the current state of the ongoing canvas. Used repeatedly to poll for updates on the state of the canvas. Each new request retrieves the timestamp of the canvas update. By adding a number of seconds to this timestamp, the request will be sent again when the client time has reached the new time. The number of seconds added is the difference between the current client time and the received server timestamp, and the resulting difference with the refresh cycle (how often the request is made). 

### POST /pixelRequest/<int:pixelNumber>/<requestedColor>
- A request to send the user input of which pixel to change and what color to change the pixel. The color sent is based on the user’s assigned color.

### Subscribe /stream
- A socket to notify the client when the server has terminated.

### GET /kill/se3313
- Gracefully terminates server and notifies the stream to update clients that server has been closed

## Authors

* **Laban Lin** - *Front End UI* - [labanlin1](https://github.com/labanlin1)
* **Patrick Lee** - *Project Design & Documentation* - [trickly](https://github.com/trickly)
* **Yanick Houde** - *Back-end Server* - [YanickHoude](https://github.com/YanickHoude)


