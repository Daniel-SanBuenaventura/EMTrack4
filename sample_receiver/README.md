### Sample receiver is a stub of an app that receives and displays data. It needs docker and docker-compose

#### Build the app

```
    cd sample_receiver/
    docker-compose up
```

#### Run the unit tests

```
    cd sample_receiver/
``` 
1) with environment variables from local.env file:

```
    docker run --env-file ./env/local.env sample_receiver_external_app pytest
```

2) with default environment variables
```    
    docker run sample_receiver_external_app pytest
```

#### Authenticate to test manually: Method POST

```
    curl -X POST http://localhost:8100/o/token/ -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" --data "grant_type=client_credentials&client_id=1234&client_secret=12345678"
```

#### Output  

```
{"access_token": "WN0ZDvkEVEupPXbOeOhTZ5uPgcXh6f", "expires_in": 36000, "token_type": "Bearer", "scope": "read write"}
```

#### Success Response

    200 

#### Verify the token: Method GET

```
    curl -X GET http://localhost:8100/api/verification/ -H "Authorization: Bearer WN0ZDvkEVEupPXbOeOhTZ5uPgcXh6f"
```

#### Output  

```
"Token verified"
```

#### Success Response

    200 

#### Send the message to test manually the service: Method POST

Use the token received in Authentication step

```
     curl -X POST http://localhost:8100/api/message/ -H "Authorization: Bearer WN0ZDvkEVEupPXbOeOhTZ5uPgcXh6f" -H "Content-Type: application/json" -d '{"customer": "Customer name", ...}'
```

In Windows either use Git Bash or, when using the command prompt enclose data in a separate json file

```
    curl -X POST http://localhost:8100/api/message/ -H "Authorization: Bearer WN0ZDvkEVEupPXbOeOhTZ5uPgcXh6f" -H "Content-Type: application/json" -d "@message.json"
```

#### Example JSON input

``` 
  "{
   "customer": <string> or null, 
   "created": <string> or null,  // 2019-10-16T06:22:33Z
   "license_plate": <string> or null, // max 40 chars
   "fleet_id": <string> or null, //max 64 chars
   "longitude": <float> or null,
   "latitude": <float> or null,
   "event_type": <string> or null,  // max 32 chars options: "pressure_low", "temperature_high", "pressure_fast_leak", "pressure_slow_leak", "new_position"
   "iso_position": <int> or null,
   "pressure": <int> or null,  // in Pascals
   "temperature": <int> or null,  // in degrees Celsius
   "mileage": <int> or null,
   "speed": <int> or null,
   "heading": <int> or null,
  }"
``` 

#### Output  

Message which has been received and printed to the terminal.

#### Success Response

    200  

If you run the application on your custom host, please replace "http://localhost:8100" with https://your-host-name