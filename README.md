[![Build Status](https://travis-ci.com/TheDenk/augmixations.svg?branch=master)](https://travis-ci.com/TheDenk/augmixations)
[![codecov.io](https://codecov.io/github/TheDenk/augmixations/coverage.svg?branch=master)](https://codecov.io/github/TheDenk/augmixations?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# augmixations
Some augmentation for object detection.  
Current augmentations:  
  - cutmix

In progress:  
  - mozaic  
  - gridmask  
   
## Cutmix  
### Default Cutmix for classifiers
<p>
<img src="images/cutmix_default.png" width="750" height="450" title="Default cutmix"/> 
</p>  
<p>  Paper: <a href="https://arxiv.org/abs/1905.04899">https://arxiv.org/abs/1905.04899</a> </p>

### Current cutmix
<p>
<img src="images/cutmix_current.png" width="750" height="450" title="Current cutmix"/> 
</p> 

## Getting Started
    pip install augmixations  

### Example with defautl parameters  

  Import:  
```python
from augmixations import cutmix  
```
  Using:  
```python
#  bg_img - The image into which a rectangle will be inserted  
#  fg_img - The image from which a random rectangle will be cut 
img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels,
                            fg_img, fg_boxes, fg_labels)  
```
  Done.
 
## Config Desctiption  

```python
rectangle_info = {
    'crop_min_x': None,  ## Minimum and maximum left-top X coordinate for rectangle crop
    'crop_max_x': None,  ## By default using 0

    'crop_min_y': None,  ## Minimum and maximum left-top Y coordinate for rectangle crop
    'crop_max_y': None,  ## By default using 0

    'min_rect_h': None,  ## Minimum and maximum rectangle height
    'max_rect_h': None,  ## By default is a random value from 1 to image height minus min X coordinate

    'min_rect_w': None,  ## Minimum and maximum rectangle width
    'max_rect_w': None,  ## By default is a random value from 1 to image width minus min X coordinate

    'insert_min_x': None,  ## Minimum and maximum left-top X coordinate for rectangle insert
    'insert_max_x': None,  ## By default is a random value from 0 to image height minus rectangle height

    'insert_min_y': None,  ## Minimum and maximum left-top X coordinate for rectangle insert
    'insert_max_y': None,  ## By default is a random value from 0 to image width minus rectangle width
}
```

```python 
process_box_config_default = {
    # Maximum allowable overlap threshold. 
    # If the overlap ratio is greater than this threshold, then the box is ignored.
    'max_overlap_area_ratio': 0.75,  

    'min_height_result_ratio': 0.25,
    'min_width_result_ratio': 0.25,

    'max_height_intersection': 0.9,
    'max_width_intersection': 0.9,
}
```