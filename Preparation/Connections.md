# Full connection

<img src = "https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/a6598ca4-4759-44f1-8d5d-3d4604470f40" width = "500">
<br>

The Camera goes straight to the port it is supposed to.

Here is the Raspberry Pi's pinout:

<img src = "https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/899b90e3-2aa7-40eb-ba45-f9d6ac54ea4d" width = "400" >

## Toled Screen Connection

There are 7 pins on the TOLED board: GND, VCC, SCL, SDA(or SDAIN), RST, SA0(or D/C), CS. We only use 5 of those.

  
|     Toled     |     Raspberry Pi   |
| :-------------: | :-------------: |
|     SCL       |       GPIO03      |
|     SDA       |       GPIO04      |
|     GND       |       Any GND pin     |
|     VCC       |       Any 5V pin      |
|     RST       |      GPIO04    |

## Infra-red Sensor


|      HW-201      |     Raspberry Pi   |
| :-------------: | :-------------: |
|     VCC       |       3.3V     |
|     GND       |      Any GND Pin      |
|     OUT        |      GPIO10   |

## The Button


|      Button     |     Raspberry Pi   |
| :-------------: | :-------------: |
|     Any Left Side Pin       |       GPIO20     |
|     Any Right Side Pin      |       GPIO21      |

## Google Drive

You need a Google Drive account.


