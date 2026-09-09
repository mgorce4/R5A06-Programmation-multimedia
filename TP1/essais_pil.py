from PIL import Image, ImageDraw

def modif_ecrase() :
    image = Image.open("IUT.png")
    image_redim = image.resize((400,200))
    image_redim.show()

    draw = ImageDraw.Draw(image)
    rayon = 32
    x = 55
    y = 165
    draw.ellipse((x-rayon, y-rayon, x+rayon, y+rayon), fill=(127,0,255) )
    image.show()

    image.save("IUT_mod.png")



def modif_composite() :
    iut = Image.open("IUT.png")
    #iut = Image.open("__fondNoir.png")
    #iut = iut.convert('RGBA')
    boule = Image.new('RGBA',iut.size, (0,0,0,0)) # varier le canal alpha

    draw = ImageDraw.Draw(boule)
    rayon = 32
    x = 55
    y = 165
    draw.ellipse((x-rayon, y-rayon, x+rayon, y+rayon), fill=(127,0,255) )
    
    composite = Image.alpha_composite(iut, boule)
    
    composite.show()

    composite.save("IUT_mod_comp.png")




if __name__=="__main__" :  
    #modif_ecrase()
    modif_composite()
