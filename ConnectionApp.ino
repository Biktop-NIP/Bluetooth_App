#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN 7
#define DHTTYPE    DHT11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

int pins[] = {A5, A4, A3, 9, 10, 11, 2, 3, 4, 5};
int pin_cmd[] =  {1, 1, 1, 2, 2, 2, 1, 1, 1, 1};
int len = 10;
int time;
int time_past;
String data;

void action(int pin, int signal){
  switch (pin_cmd[pin]) {
    case 1:
      digitalWrite(pins[pin], signal);
      break;
    case 2:
      analogWrite(pins[pin], map(signal, 0, 100, 0, 255));
      break;
  }
}

void send(){
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    String a1 = String(event.temperature) + "c";
    dht.humidity().getEvent(&event);
    String a2 = String(event.relative_humidity) + "%";
    String a3 = String(random(0,100)) + "%";
    Serial.println("<" + a2 + "," + a1 + "," + a3 + ">");
}


void setup() {
    for (int i; i <= len; i++ ){
        pinMode(pins[i], OUTPUT);
    }
    Serial.begin(9600);
    dht.begin();
    sensor_t sensor;
    dht.temperature().getSensor(&sensor);
    dht.humidity().getSensor(&sensor);
}


void loop() {
    if(Serial.available()){
        data = Serial.readStringUntil('|');
        for (int i=0; i < data.length(); i++){
            if (data[i] == ','){             
                int pin = data.substring(0, i).toInt();
                int signal = data.substring(i+1, data.length()).toInt();
                action(pin, signal);
                break;
            }
        }
    }
    time = millis();
    if(time-time_past > 200){
        time_past = millis();
        send();
    }
}
