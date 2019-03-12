## How to use

### UI

*Histogram matching*

``` bash
python main.py hm IMAGE_PATH_1 [IMAGE_PATH_2]
```

*Luminance and contrast*

``` bash
python main.py lc IMAGE_PATH_1
```



### Without UI

*Histogram matching*

``` bash
python main.py hmb IMAGE_PATH_1 IMAGE_PATH_2
```

This command will generate two images which named lumi_result.jpg and rgb_result.jpg by remapping first image to have the Lum. or rgb cdf of another.

``` bash
Python main.py hmb IMAGE_PATH
```

This command will remap the image to have two of its color pdfs match the third.



### Example

There is an example in the output folder.