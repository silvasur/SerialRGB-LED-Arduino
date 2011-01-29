#define LEDR      9
#define LEDG     10
#define LEDB     11

int r, g, b;

void setup()
{
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  r = g = b = 0;
  
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available() >= 3)
  {
    r = Serial.read();
    g = Serial.read();
    b = Serial.read();
  }
  analogWrite(LEDR, r);
  analogWrite(LEDG, g);
  analogWrite(LEDB, b);
}
