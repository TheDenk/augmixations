[![Build Status](https://travis-ci.com/TheDenk/augmixations.svg?branch=master)](https://travis-ci.com/TheDenk/augmixations)
[![codecov.io](https://codecov.io/github/TheDenk/augmixations/coverage.svg?branch=master)](https://codecov.io/github/TheDenk/augmixations?branch=master)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Generic badge](https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg)](https://shields.io/)
[![Downloads](https://pepy.tech/badge/augmixations)](https://pepy.tech/project/augmixations)

# augmixations
Some augmentations that I hasn't found in other repositories and libraries.  
  
Warning: This library does not install all dependencies for each augmentation.  

I wrote dependencies in each description and you should install it by yourself.  
  
For more details you can see the <a href="https://github.com/TheDenk/augmixations/wiki">wiki</a> page of this repo.  


Current augmentations:  
  - cutmix (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/cutmix_example.ipynb">Colab Example</a>, <a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage">Advanced Usage</a>)  
  - cutout (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/cutout_example.ipynb">Colab Example</a>, <a href="https://github.com/TheDenk/augmixations/wiki/Cutout-Advanced-Usage">Advanced Usage</a>)  
  - hand written blots (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/blots_example.ipynb">Colab Example</a>, <a href="https://github.com/TheDenk/augmixations/wiki/Blots-Advanced-Usage">Advanced Usage</a>)  


In progress:  
  - mozaic (object detection)  
  - gridmask (object detection)  
  - mixin (object detection)  
   
## Cutmix  
#### Dependencies  

- numpy>=1.11.1 (installed) 
  
<p>
<img src="images/cutmix_current.png" width="600" height="360" title="Current cutmix"/> 
</p> 

## Handwritten Blots
#### Dependencies  


- numpy>=1.11.1 (installed)
- bezier==2020.5.19 (NOT installed)
- opencv-python>=4.1.1 (NOT installed)

<p>
<img src="images/blots.png" width="600" height="200" title="Blots"/> 
</p> 

## Getting Started
    pip install augmixations  

### Example with default parameters  


  Import:  
```python
from augmixations import SmartCutmix  
```
  Using:  
```python
#  bg_img - The image into which a rectangle will be inserted  
#  fg_img - The image from which a random rectangle will be cut 
cutmix = SmartCutmix()
img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels,
                            fg_img, fg_boxes, fg_labels)  
```
  Done.
 
## Advansed usage 

<p>You can pass special configs to the cutmix function to override its behavior.</p>   
<a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage"><p>Cutmix Advanced Usage</p></a>  
<a href="https://github.com/TheDenk/augmixations/wiki/Cutout-Advanced-Usage"><p>Cutout Advanced Usage</p></a>  
<a href="https://github.com/TheDenk/augmixations/wiki/Blots-Advanced-Usage"><p>Blots Advanced Usage</p></a>  

## Contacts
<p>Issues should be raised directly in the repository. For professional support and recommendations please <a>welcomedenk@gmail.com</a>.</p>
  
  
