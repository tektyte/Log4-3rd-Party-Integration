/*
 Log4 USB and POE Serial Output

 Takes in serial information from Log4 USB or POE device (FW = 2.x.x) then
 displays measurements on Arduino Serial Monitor.

 created 2020
 by Tekt Industries

 This example code is in the public domain.

Using Arduino Mega 2560
Power 5v pin
pin TX1 18
pin RX1 19
GND pin
 */

// Constant won't change. They are always the same at the
// beginning of a measurement packet
#define COLON 58
#define ADDRESS 1
#define SLAVE_CMD 11
#define DATA_COUNT_USB 18
#define DATA_COUNT_POE 26
#define END 10

/*
Time between keep alive messages, device will stop streaming if no KEEP_ALIVE message is received within 2000ms
*/
#define KEEP_ALIVE_INTERVAL_MS 500

unsigned long last_updated_time;

#define SET_STREAMING_MODE_CMD 0x11
#define KEEP_ALIVE_CMD 0x02

uint8_t start_byte;
uint8_t address_byte;
uint8_t command_byte;
uint8_t data_count_byte;
uint8_t data_byte[32];
uint8_t current_byte_A[4];
uint8_t voltage_byte_A[4];
uint8_t current_byte_B[4];
uint8_t voltage_byte_B[4];
uint8_t end_byte;

float current_A;
float voltage_A;
float power_A;
float current_B;
float voltage_B;
float power_B;

enum decode_state {
    START_BYTE,
    ADDR_BYTE,
    CMD_BYTE,
    DATA_COUNT_BYTE,
    DATA_STORE,
    END_BYTE,
};

int32_t convert_to_int32(uint8_t * buff) {
    int32_t integer=0;
    integer = ((int32_t)buff[3]<<24) | ((int32_t)buff[2]<<16) | ((int32_t)buff[1]<<8) | (int32_t)buff[0];
    return integer;
}

//Set Streaming Mode is only for Log4 F.W. = 2.X.X
// Enable Streaming mode by passing true otherwise false.
void set_streaming_mode(bool mode){
    uint8_t streaming_mode = 0;
    if (mode)
    {
        streaming_mode = 1;
    }
    uint8_t out_buffer[6];
    out_buffer[0] = COLON;
    out_buffer[1] = ADDRESS;
    out_buffer[2] = SET_STREAMING_MODE_CMD;
    out_buffer[3] = 1;
    out_buffer[4] = streaming_mode;
    out_buffer[5] = END;
    Serial1.write(out_buffer,sizeof(out_buffer));
}

// Send Keep Alive to keep streaming mode open
void keep_alive(void){
    uint8_t out_buffer[5];
    out_buffer[0] = COLON;
    out_buffer[1] = ADDRESS;
    out_buffer[2] = KEEP_ALIVE_CMD;
    out_buffer[3] = 0;
    out_buffer[4] = END;
    Serial1.write(out_buffer,sizeof(out_buffer));
}

void print_measurements(uint8_t data_length) {
    for (int i=10; i<14; i++) {
        current_byte_A[i-10]=data_byte[i];
        voltage_byte_A[i-10]=data_byte[i+4];
    }
    current_A=convert_to_int32(current_byte_A)/float(1000);
    voltage_A=convert_to_int32(voltage_byte_A)/float(1000);
    power_A = current_A * voltage_A;
    if (data_length==DATA_COUNT_USB) {
        Serial.println("Log4_USB device");
        Serial.print(current_A);
        Serial.println(" mA");
        Serial.print(voltage_A);
        Serial.println(" V");
        Serial.print(power_A);
        Serial.println(" mW");
    }
    else if (data_length==DATA_COUNT_POE) {
        Serial.println("Log4_POE device");
        for (int i=10; i<14; i++) {
            current_byte_B[i-10]=data_byte[i+8];
            voltage_byte_B[i-10]=data_byte[i+12];
        }
        current_B=convert_to_int32(current_byte_B)/float(1000);
        voltage_B=convert_to_int32(voltage_byte_B)/float(1000);
        power_B= current_B * voltage_B;
        Serial.println("Channel A");
        Serial.print(current_A);
        Serial.println(" mA");
        Serial.print(voltage_A);
        Serial.println(" V");
        Serial.print(power_A);
        Serial.println(" mW");
        Serial.println("Channel B");
        Serial.print(current_B);
        Serial.println(" mA");
        Serial.print(voltage_B);
        Serial.println(" V");
        Serial.print(power_B);
        Serial.println(" mW");
    }
}

void setup() {
    Serial.begin(115200);
    Serial1.begin(115200);
    while (!Serial); // wait for Serial device to be ready
    while (!Serial1); // wait for Serial1 device to be ready
    Serial.println("Enabling Streaming Mode");
    set_streaming_mode(true);
    last_updated_time = millis();
}

void loop() {
    static enum decode_state dec = START_BYTE;
    static uint8_t cur_cmd=0;
    static uint8_t cur_len=0;
    static uint8_t data_byte_idx=0;

    unsigned long now = millis();

    if ((now - last_updated_time) > KEEP_ALIVE_INTERVAL_MS) {
        last_updated_time = now;
        keep_alive();
    }

    if (Serial1.available()>0) {     // If anything comes in Serial1 (pins 0 & 1)
        uint8_t read_byte = Serial1.read();
        switch(dec) {
        case START_BYTE:
            if(read_byte == COLON) {
                dec = ADDR_BYTE;
            }
            else {
                dec=START_BYTE;
            }
            break;
        case ADDR_BYTE:
            if(read_byte == ADDRESS) {
                dec = CMD_BYTE;
            }
            else {
                dec = START_BYTE;
            }
            break;
        case CMD_BYTE:
            if(read_byte == SLAVE_CMD) {
                cur_cmd=read_byte;
                dec = DATA_COUNT_BYTE;
            }
            else {
                dec=START_BYTE;
            }
            break;
        case DATA_COUNT_BYTE:
            if(read_byte==DATA_COUNT_POE) {
                cur_len = read_byte;
                data_byte_idx = 0;
                dec = DATA_STORE;
            }
            else if (read_byte==DATA_COUNT_USB) {
                cur_len = read_byte;
                data_byte_idx = 0;
                dec = DATA_STORE;
            }
            else {
                dec= START_BYTE;
            }
            break;
        case DATA_STORE:
            if (data_byte_idx<cur_len) {
                data_byte[data_byte_idx]=read_byte;
                data_byte_idx+=1;
            }
            else {
                dec=END_BYTE;
            }
            break;
        case END_BYTE:
            if(read_byte==END) {
                print_measurements(cur_len);
                dec = START_BYTE;
            }
            break;
        }
    }
}
