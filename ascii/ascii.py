import webbrowser
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from ascii.api import search
import math
from ascii.File import filecount, clear_files
from ascii.colormanage import manage
from ascii.metadata import makejson
import json
import ascii.ipfs_pinata.ipfsPy as ipfs
import ascii.dna as dna

def ascii_art(num,ch, token, extra=None):
    dnaStrand = dna.DNA(20)
    print('------------------------------------------------------------------------------')
    print("Generating ASCII art for image number {}".format(num))
    print('------------------------------------------------------------------------------')
    chars=ch
    # chars = "#Wo- "[::-1]
    charArray = list(chars)
    charLength = len(charArray)
    interval = charLength/256

    scaleFactor = 0.5

    oneCharWidth = 8
    oneCharHeight = 12

    def getChar(inputInt):
        return charArray[math.floor(inputInt*interval)]

    # text_file = open("./outputs/metadata/metadata"+str(num)+".json", "w")

    # Making the Metadata
    # makejson(num)

    if extra is None:
        add = './inputs/nft_input'+str(num)+'.jpg'
    else:
        add = './inputs/'+extra
        num=1        

    im = Image.open(add)
    # im.resize((100,100))
    fnt = ImageFont.truetype('ascii/firacode.ttf', 15)

    width, height = im.size

    # basewidth = 50
    # wpercent = (basewidth/float(im.size[0]))
    # hsize = int((float(im.size[1])*float(wpercent)))
    # im = im.resize((basewidth,hsize), Image.ANTIALIAS)
    # # im=im.resize(resi, Image.ANTIALIAS)

    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    width, height = im.size
    pix = im.load()

    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]
            h = int(r/3 + g/3 + b/3)
            pix[j, i] = (h, h, h)
            # text_file.write(getChar(h))
            d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))

        # text_file.write('\n')

    outputImage = manage(outputImage)
    outputImage.save('./outputs/'+dnaStrand+str(num)+'.jpg')
    print('------------------------------------------------------------------------------')
    print("NFT"+str(num)+" created")
    print("JSON"+str(num)+" created")
    print('------------------------------------------------------------------------------')
    print("Uploading to IPFS...")
    print("------------------------------------------------------------------------------")
    ipfs_Res = (ipfs.addImg('./outputs/'+dnaStrand+str(num)+'.jpg'))
    ipfs_Res.update({"token": token})
    ipfs_Res.update({"nft_id": num})
    ipfs_Res.update({"dna": dnaStrand})
    ipfs_Res.update({"imgLink": 'https://gateway.pinata.cloud/ipfs/'+ipfs_Res['IpfsHash']})
    print("------------------------------------------------------------------------------")
    with open('./outputs/metadata/'+dnaStrand+str(num)+'.json', 'w') as outfile:
        json.dump(ipfs_Res, outfile, indent=4)
    metaipfs = ipfs.addJson('./outputs/metadata/'+dnaStrand+str(num)+'.json')
    metaipfs["url"] = 'https://gateway.pinata.cloud/ipfs/'+metaipfs['IpfsHash']
    ipfs_Res.update({"metadata": metaipfs})
    ipfsnew = {dnaStrand : ipfs_Res}
    print('------------------------------------------------------------------------------')
    try:
        with open('./allHashStore.json', 'r') as f:
            data = json.load(f)
            data.update(ipfsnew)
            with open('./allHashStore.json', 'w') as f:
                json.dump(data, f,indent=4)
            print('------------------------------------------------------------------------------')
            print("IPFS Hash added to allHashStore.json")
            print('------------------------------------------------------------------------------')
            print('Showing the result...')
            print('------------------------------------------------------------------------------')
            print(ipfs_Res)
            print('------------------------------------------------------------------------------')
            webbrowser.open('https://gateway.pinata.cloud/ipfs/'+ipfs_Res['IpfsHash'])
    except:
        print("Error in storing the hash details.")
        print('------------------------------------------------------------------------------')
        ipfs.removeFile(ipfs_Res['IpfsHash'])
        print("IPFS Hash removed")
        print('------------------------------------------------------------------------------')
    if extra is not None:
        print('------------------------------------------------------------------------------')
        print("Done! Enjoy!")
        print('------------------------------------------------------------------------------')
# print(ascii.charlist())



def run(tokex, maxn, ch):
    print('------------------------------------------------------------------------------')
    token = tokex
    print("Token : "+ token)
    max_results = maxn
    print("Number of NFTs in progress : "+ str(max_results))
    print('------------------------------------------------------------------------------')

    #Searching and saving the input images
    clear_files('./inputs')
    clear_files('./outputs')
    clear_files('./outputs/metadata')
    search(token,max_results)
    files=filecount('./inputs')

    chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    addon=ch.lower()
    chars += addon
    print('Characters used : '+chars[:25]+"... and many more.")
    print('------------------------------------------------------------------------------')

    
    for i in range(files):
        ascii_art(i,chars, token)
    print('------------------------------------------------------------------------------')
    print("Done! Enjoy!")
    print('------------------------------------------------------------------------------')

if __name__ == '__main__':
    run()