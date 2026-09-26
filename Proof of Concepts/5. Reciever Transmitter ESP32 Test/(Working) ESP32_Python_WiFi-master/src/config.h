/* 
 * -----------------------------------------------------------------------------
 * Example: Two way communication between ESP32 and Python using WIFI
 * -----------------------------------------------------------------------------
 * Author: Radhi SGHAIER: https://github.com/Rad-hi
 * -----------------------------------------------------------------------------
 * Date: 07-05-2023 (7th of May, 2023)
 * -----------------------------------------------------------------------------
 * License: Do whatever you want with the code ...
 *          If this was ever useful to you, and we happened to meet on 
 *          the street, I'll appreciate a cup of dark coffee, no sugar please.
 * -----------------------------------------------------------------------------
 */

#ifndef __CONFG_H___
#define __CONFG_H___

/* Pins definitions */
#define LED_PIN                     12
#define BTN_PIN                     14

/* Communication params */
#define ACK                         "A" // acknowledgment packet
#define QUEUE_LEN                   5
#define MAX_BUFFER_LEN              128

/* WiFi params */
#define WIFI_SSID                   "Invigatorium East"
#define WIFI_PASSWORD               "Moose2017!?@"

/* Socket */
#define SERVER_ADDRESS              "192.168.0.13"
#define SERVER_PORT                 11111 // Needs to match port: int in wifi_communicator.py

#endif // __CONFG_H___
