# Full connection

<img src = "https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/e5fed023-aac9-4cfa-89b7-2e7cd6e92c83" width = "500">

<br>

The Camera goes straight to the port it is supposed to.

Here is the Raspberry Pi's pinout:

<img src = "https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/1f1b40d6-cab6-4acf-9f55-1758c2df7adf" width = "400" >

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


