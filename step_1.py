import skimage.io as io

class ImageAnalysis:
    def __init__(self, image):
        self.image = io.imread(image) # immediately read picture data into numPy array
    def __str__(self): # method to tell default print() what to write to the output
        # this uses string formatting of the 'shape' int tuple into string
        # notice (<item>,) notation (especially the comma after the first item) /
        # this tells Python that this is a formatting tuple with one operand, /
        # not an expression (<expr>)
        return 'Shape is: %s' % (self.image.shape,) # try removing the comma
    def show(self):
        io.imshow(self.image) # transfer image data into the output queue
        io.show() # show image in queue, using GUI

i = ImageAnalysis('mountain.png')
print(i)
i.show()
