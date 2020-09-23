[![Build Status](https://travis-ci.com/TheDenk/augmixations.svg?branch=master)](https://travis-ci.com/TheDenk/augmixations)
[![codecov.io](https://codecov.io/github/TheDenk/augmixations/coverage.svg?branch=master)](https://codecov.io/github/TheDenk/augmixations?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# augmixations
Some augmentation for object detection.  
Current augmentations:  
  - cutmix
## Cutmix is ...
picture

## Getting Started
    pip install augmixations  

### Example with defautl parameters
    from augmixations import cutmix  

    img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels,
                                fg_img, fg_boxes, fg_labels)  
    
    #  Where  
    #  bg_img - The image into which a rectangle will be inserted  
    #  fg_img - The image from which a random rectangle will be cut  
    