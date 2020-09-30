## Augmixations
Some augmentation for object detection.  
### Current augmentations:  
* cutmix (<a href="https://github.com/TheDenk/augmixations/examples/cutmix_example.ipynb">Colab Example</a>)

### In progress:  
* mozaic  
* gridmask  
* mixin

## Getting Started  

```
pip install augmixations  
```

## Example with default parameters

### Import:  

```
from augmixations import cutmix  
```

### Using:  

```
#bg_img - The image into which a rectangle will be inserted
#fg_img - The image from which a random rectangle will be cut 

img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels)  
```

### Done.

## Advansed usage 

<p>You can pass special configs to the cutmix function to override its behavior.</p>  
  
<a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage"><p>Cutmix Advanced Usage</p></a> 
 
  
  
