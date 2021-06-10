import skimage.io as io # basic image methods
import skimage.color as color # color conversion module
import numpy as np # for ndarray

class ImageAnalysis:
    def __init__(self, image):
        self.image = io.imread(image) # immediately read picture data into numPy array
        self.hidden = None # blank for hidden image data
        
    def __str__(self): # method to tell default print() what to write to the output
        # this uses string formatting of the 'shape' int tuple into string
        # notice (<item>,) notation (especially the comma after the first item) /
        # this tells Python that this is a formatting tuple with one operand, /
        # not an expression (<expr>)
        return 'Shape is: {}'.format(self.image.shape)
    
    def show(self):
        io.imshow(self.image) # transfer image data into the output queue
        io.show() # show image in queue, using GUI

    # to display hidden picture and ensure it was saved in the class instance
    def showHidden(self):
        if self.hidden is None:
            print('No hidden picture built!')
        else:
            io.imshow(self.hidden)
            io.show()

    def retriveHidden(self):
        # initialize sedulting array in the class instance
        # specifying dimensions and type to avoid imprecise conversions
        self.hidden = np.ndarray(( 131, 100, 3 ), np.uint8)
        
        for row in range(131): # for each resulting row...
            for col in range(100): # for each resulting col...
                self.hidden[row, col] = self.image[row * 11][col * 11] # take each 11th pixel
        
        io.imsave('./hidden.jpg', self.hidden) # save
        

i = ImageAnalysis('mountain.png')
# print(i)
# i.show()
i.retriveHidden()
i.showHidden()
