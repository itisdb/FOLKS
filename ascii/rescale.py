from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def rescale():
    im = Image.open("./inputs/nft_input2.jpg")
    size = im.size
    print("Input Image Res: "+ str(size))
    # basewidth = 50
    # wpercent = (basewidth/float(im.size[0]))
    # hsize = int((float(im.size[1])*float(wpercent)))
    # im = im.resize((basewidth,hsize), Image.ANTIALIAS)
    # print(im.size)
    scaleFactor = 0.4
    width, height = im.size
    oneCharWidth = 10
    oneCharHeight = 18
    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    print("Processing Image Res: "+str(im.size))
    outputImage = Image.new('RGB', (int(oneCharWidth * width), int(oneCharHeight * height)), color = (0, 0, 0))
    print("Output Image Res: "+str(outputImage.size))

rescale()