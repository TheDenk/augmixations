CHANGELOG
=========

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
