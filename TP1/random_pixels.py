from PIL import Image
from random import randint
 

if __name__=="__main__" : 

    img1 = Image.new('RGBA', (500,500), (0,0,0,0)) # transparent 
    
    (largeur, longueur) = img1.size
    print(largeur,"x",longueur)
    
    for x in range(largeur) :
        for y in range(longueur) :
            r = randint(0,255) ; g = randint(0,255) ; b = randint(0,255)
            img1.putpixel((x,y), (r, g, b))
            

    print(img1.getpixel((0,0)))
    img1.show()



