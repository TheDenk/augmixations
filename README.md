[![Build Status](https://travis-ci.com/TheDenk/augmixations.svg?branch=master)](https://travis-ci.com/TheDenk/augmixations)
[![codecov.io](https://codecov.io/github/TheDenk/augmixations/coverage.svg?branch=master)](https://codecov.io/github/TheDenk/augmixations?branch=master)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Generic badge](https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg)](https://shields.io/)
[![Downloads](https://pepy.tech/badge/augmixations)](https://pepy.tech/project/augmixations)

# augmixations
Some augmentations that I hasn't found in other repositories and libraries.  
  
For more details you can see the <a href="https://github.com/TheDenk/augmixations/wiki">WIKI</a> page of this repo.  


Current augmentations:  
  - Cutmix (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/cutmix_example.ipynb">Colab Example</a>, <a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage">Advanced Usage</a>)  
  - Cutout (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/cutout_example.ipynb">Colab Example</a>)  
  - Mixup (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/mixup_example.ipynb">Colab Example</a>)    
   
## Cutmix  
#### Dependencies  

- numpy>=1.11.1
  
<p>
<img src="images/cutmix_current.png" width="600" height="360" title="Current cutmix"/> 
</p> 

## Getting Started
    pip install augmixations  

### Example with default parameters  


  Import:  
```python
from augmixations import Cutmix, Cutout, Mixup  
```
  Using Cutmix:  
```python
#  bg_img - The image into which a rectangle will be inserted  
#  fg_img - The image from which a random rectangle will be cut 
cutmix = Cutmix()
img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels,
                            fg_img, fg_boxes, fg_labels)  
```
  Done.  
 
  Using Cutout:  
```python
cutout = Cutout()
new_img, new_boxes, new_labels = cutmix(img, boxes, labels)
```
  Done.  
  
  Using Mixup:  
```python
mixup = Mixup()
image, boxes, labels = mixup(first_img, first_boxes, first_labels, 
                             second_img, second_boxes, second_labels)
```
  Done.  

## Advansed usage 

<p>You can pass special configs to the cutmix function to override its behavior.</p>   
<a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage"><p>Cutmix Advanced Usage</p></a> 

## Contacts
<p>Issues should be raised directly in the repository. For professional support and recommendations please <a>welcomedenk@gmail.com</a>.</p>
  
  
