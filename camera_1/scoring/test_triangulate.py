from triangulate import main as triangulate
from Draw_board import main as draw
import logging

def main():

#    score = triangulate([590, 232], [250, 250])
#    print (score)
    score = triangulate([1007, 229], [1045, 186])
    print (score)
    #draw(0,50)
    
if __name__=='__main__':

    logging.basicConfig(format='%(message)s',level=logging.INFO)

    main()

