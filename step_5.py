import skimage.io as io # basic image methods
import numpy as np # for ndarray
import csv; # for making easy CSV string

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
        # specifying dimensions + type, latter to avoid imprecise conversions
        self.hidden = np.ndarray(( 131, 100, 3 ), np.uint8)
        
        for row in range(131): # for each resulting row...
            for col in range(100): # for each resulting col...
                self.hidden[row, col] = self.image[row * 11][col * 11] # take each 11th pixel
        
        io.imsave('./hidden.jpg', self.hidden) # save

    def fix(self):
        # prepare source image dimensions
        height = len(self.image) 
        width = len(self.image[0])

        # running through each pixel
        for row in range(height):
            for col in range(width):
                # pass ones than are not 11th they are ok
                if row % 11 != 0 and col % 11 != 0:
                    continue

                """
                4 neighbouring pixels (N) around target pixel (A):
                .N.
                NAN
                .N.
                """
                neighboursIndices = [[row + 1, col + 1], [row + 1, col - 1], [row - 1, col + 1], [row - 1, col - 1]]

                # collect only ones that don't step out of bounds
                neighbours = []
                for nI in neighboursIndices:
                    rown, coln = nI
                    if rown < 0 or rown >= height or coln < 0 or coln >= width:
                        continue
                    neighbours.append(self.image[rown, coln])
                
                count = len(neighbours)
                # this shouldn't happen semanticaly, but just in case
                if count == 0:
                    continue
                # count avg of each component
                sumR = sumG = sumB = 0;
                for n in neighbours:
                    r,g,b = n
                    sumR += r
                    sumG += g
                    sumB += b

                # write new pixel
                self.image[row, col, 0] = sumR // count;
                self.image[row, col, 1] = sumG // count;
                self.image[row, col, 2] = sumB // count;
                    
    def averageRGB(self):
        """
        open safely, so the file will be handled properly and closed afterwards without exceptions
        avoiding try ... catch ... construct, using with instead
        keywords:
        - newline '' -- so there wouldn't be an extra carriage return (\r) after each line
        - encoding utf-8, just to be sure it won't be unreadable afterwards
        """
        with open('./RGB.csv', 'w', newline='',  encoding='utf-8') as f:
            """
            Making writer with file hadle and param: 
            quoting QUOTE_NONNUMERIC -- to leave float numbers without quotes
            """
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC) 
            for row in self.hidden:
                newRow = []
                for cell in row.astype(np.float64): # conversion in order not to catch an overflow with uint8 
                    avg = (cell[0] + cell[1] + cell[2]) / 3 # finging average value
                    newRow.append(avg) 
                wr.writerow(newRow) # write new row to CSV 
            f.close() # gracefuly close writing handle

    def load_rgb_from_file(self):
        # read array from csv, set delimiter comma and expect floats in utf-8 encoded text
        arr = np.genfromtxt('./RGB.csv', delimiter = ',', dtype=np.float64, encoding = 'utf-8')
        imgData = np.ndarray(( 131, 100, 3 ), np.uint8) # initialize new array for an image
        for i in range(len(arr)): # going by index so 2 arrays could be connected
            for j in range(len(arr[0])):
                val = arr[i,j].astype(np.uint8) # conversion float64 to uint8
                imgData[i,j,:] = [val, val, val]; # insert whole range 
        io.imshow(imgData)
        io.show() # show image

i = ImageAnalysis('mountain.png')
# print(i)
# i.show()
i.retriveHidden()
# i.showHidden()
i.fix() # fixing "in place", not making new picture
# i.show()
# io.imsave('./fixed.jpg', i.image) # save fixed result into file, just in case 
i.averageRGB()
i.load_rgb_from_file()
