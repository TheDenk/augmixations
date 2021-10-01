## Augmixations
Some augmentations that I hasn't found in other repositories and libraries.  
  

### Current augmentations:  
* Cutmix (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/cutmix_example.ipynb">Colab Example</a>)
* Cutout (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/cutout_example.ipynb">Colab Example</a>)
* Mixup (<a href="https://github.com/TheDenk/augmixations/blob/master/examples/mixin_example.ipynb">Colab Example</a>) 

## Getting Started  

```
pip install augmixations  
```

## Example with default parameters

### Import:  

```
from augmixations import Cutmix, Cutout, Mixup    
```

### Using Cutmix:  
```
#bg_img - The image into which a rectangle will be inserted
#fg_img - The image from which a random rectangle will be cut 

cutmix = Cutmix()
img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels)  
```
### Done.

### Using Cutout:  
```python
cutout = Cutout()
new_img, new_boxes, new_labels = cutmix(img, boxes, labels)
```
### Done.  
  
### Using Mixup:  
```python
mixup = Mixup()
image, boxes, labels = mixup(first_img, first_boxes, first_labels, 
                             second_img, second_boxes, second_labels)
```
### Done.  

## Advansed usage 

<p>You can pass special configs to the cutmix function to override its behavior.</p>   
<a href="https://github.com/TheDenk/augmixations/wiki/Cutmix-Advanced-Usage"><p>Cutmix Advanced Usage</p></a> 

## Contacts
<p>Issues should be raised directly in the repository. For professional support and recommendations please <a>welcomedenk@gmail.com</a>.</p>
 
  
  
