import json
import ascii.dna as dna

def makejson(num,ipfs='ipfs://', Descriptions=dna.DNA(20)):
        metadata = {
            "description": Descriptions, 
            "external_url": "https://barterlink.vercel.app | https://sads.vercel.app", 
            "image": ipfs, 
            "name": "Dave Starbelly",
            "attributes": [
                {
                "trait_type": "Base", 
                "value": "Starfish"
                }, 
                {
                "trait_type": "Eyes", 
                "value": "Big"
                }, 
                {
                "trait_type": "Mouth", 
                "value": "Surprised"
                }, 
                {
                "trait_type": "Level", 
                "value": 5
                }, 
                {
                "trait_type": "Stamina", 
                "value": 1.4
                }, 
                {
                "trait_type": "Personality", 
                "value": "Sad"
                }, 
                {
                "display_type": "boost_number", 
                "trait_type": "Aqua Power", 
                "value": 40
                }, 
                {
                "display_type": "boost_percentage", 
                "trait_type": "Stamina Increase", 
                "value": 10
                }, 
                {
                "display_type": "number", 
                "trait_type": "Generation", 
                "value": 2
                }
            ], 
        }

        # Serializing json 
        json_object = json.dumps(metadata, indent = 4)
        
        # Writing to sample.json
        with open("./outputs/metadata/metadata"+str(num)+".json", "w") as outjson:
            outjson.write(json_object)
        

if __name__ == "__main__":
    makejson(0)