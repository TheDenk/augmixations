CHANGELOG
=========

v0.2.2
-------
- Changed default Mixin transparency to (0.4, 0.6)

v0.2.1
-------
- Added Mixin augmentation

v0.2.0
-------
- Move Blots to https://github.com/TheDenk/hwb
- Renamed Cutmix and Cutout (was removed prefix Smart)

v0.1.1
-------
- Fixed bug hwb (long int)
- Fixed bug cutout (holes count)

v0.1.0
-------
- Renamed Cutmix to SmartCutmix
- Added SmartCutout

v0.0.4
-------
- Changed config type of cutmix
- Added Handwritten blots augmentation and tests 

v0.0.3
-------
- Now taking minimum size parameters of background image and foreground image to generate rectangle  
- Changed default min rectangle height to img_height // 10 (the same with width)  
- Changed default max rectangle height to img_height // 3 (the same with width)  

v0.0.2
-------
- fixed generate rect coordinates 

v0.0.1
-------
- initial version
