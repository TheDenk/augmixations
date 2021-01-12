## Augmixations
Some augmentations that I hasn't found in other repositories and libraries.  
  
Warning: This library does not install all dependencies for each augmentation.  

### Current augmentations:  
* cutmix (<a href="https://github.com/TheDenk/augmixations/examples/cutmix_example.ipynb">Colab Example</a>)
* cutout (<a href="https://github.com/TheDenk/augmixations/examples/cutout_example.ipynb">Colab Example</a>)
* blots (<a href="https://github.com/TheDenk/augmixations/examples/blots_example.ipynb">Colab Example</a>)

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
from augmixations import SmartCutmix  
```

### Using:  

```
#bg_img - The image into which a rectangle will be inserted
#fg_img - The image from which a random rectangle will be cut 

cutmix = SmartCutmix()
img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels)  
```

### Done.

## Advansed usage 

<p>You can pass special configs to the cutmix function to override its behavior.</p>   
<a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage"><p>Cutmix Advanced Usage</p></a>  
<a href="https://github.com/TheDenk/augmixations/wiki/Cutout-Advanced-Usage"><p>Cutout Advanced Usage</p></a>  
<a href="https://github.com/TheDenk/augmixations/wiki/Blots-Advanced-Usage"><p>Blots Advanced Usage</p></a>  

## Contacts
<p>Issues should be raised directly in the repository. For professional support and recommendations please <a>welcomedenk@gmail.com</a>.</p>
 
  
  
