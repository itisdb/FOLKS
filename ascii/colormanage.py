from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def manage(outputImage):
    # outputImage = ImageEnhance.Contrast(outputImage).enhance(2)
    outputImage = ImageEnhance.Color(outputImage).enhance(2)
    # outputImage = ImageEnhance.Sharpness(outputImage).enhance(0.2)
    outputImage = ImageEnhance.Brightness(outputImage).enhance(1.1)
    # outputImage = ImageEnhance.Sharpness(outputImage).enhance(0.2)

    return outputImage

if __name__ == '__main__':
    n=input("Enter the number of the NFT: ")
    add = '../outputs/nft'+n+'.jpg'
    im = Image.open(add)
    im=manage(im)
    im.save('../outputs/nft'+n+'.jpg')
