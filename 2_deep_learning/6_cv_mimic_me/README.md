## Udacity - Artificial Intelligence Nanodegree - nd889

# Lab: Mimic Me!

For this Lab we were given the source to the Affectiva JS Demo SDK and asked to implement some simple Canvas code to draw points on various facial marker coords returned from the API.

In addition we were asked to implement a little game to utilize some other data returned from the API. The user is shown an emoji and asked to mimic it with their face. If they get it correct they get a point if they fail within 6 seconds a new random emoji is generated.

## Serving locally over HTTPS

Generate a cert:
```
$ generate-pemfile.sh
```

This creates an SSL certificate file named my-ssl-cert.pem that is used to serve over https.

Now you can launch the server using:

```
$ python serve.py
```
