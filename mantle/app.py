import json

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import subprocess
import random
import requests
import json

def push_chat(mantle_url, img):
    #mantle_url = "sample"
    #img = "sample"
    file = open(r'C:/Users/jayav/Desktop/scaling ethereum/push/push.js','w+')

    k= """import * as PushAPI from "@pushprotocol/restapi";
    import * as ethers from "ethers";

    //const PK = ""; // channel private key

    const Pkey = `0xbfda15ce3b8a6405882e7571d9953e9435d45d713eff2fee080b9a4873094d05`;
    const signer = new ethers.Wallet(Pkey);
    const sendNotification = async () => {
    try {
        const apiResponse = await PushAPI.payloads.sendNotification({
        signer,
        type: 4, // subset
        identityType: 2, // direct payload
        notification: {
            title: `Gamify - New NFt minted!`,
            body: `Hey here's your new NFT!`,
        },
        payload: {
            title: `Congrats you have minted a new NFT!`,
            body: `\n Hey here's your new nft! \n Find it on the mantle block explorer \n %s`,
            cta: "",
            img: "%s",
        },
        recipients: [
            "eip155:5:0x25cEA86d3309AFA37bEd0412810c5a4d9Ffdb9D7",
            "eip155:5:0xAdF8af32653ffdF5c5cD4ae760b54598a51536d3",
            "eip155:5:0xDfB90E5f7f3f62aC4B15b431F4674354A21eed56",
        ], // recipients addresses
        channel: "eip155:5:0xE49ab5380e332AC3456bB33cf588Db2770536f27", // your channel address
        env: "staging",
        });

        // apiResponse?.status === 204, if sent successfully!
        console.log("API repsonse: ", apiResponse);
    } catch (err) {
        console.error("Error: ", err);
    }
    };
    sendNotification()"""%(mantle_url,img)
    file.write(k)
    file.close()

    result = subprocess.run(['node', r"C:\Users\jayav\Desktop\scaling ethereum\push\push.js"], capture_output=True, text=True)
    #print(result.stdout)

def nft_meta(img):
    file = open(r'nft-metadata.json','w+')
    k = """{
        "attributes": [
            {
                "trait_type": "Wallpaper",
                "value": "MEkaku"
            },
            {
                "trait_type": "colors",
                "value": "orange"
            }
        ],
        "description": "Hey this is your NFT!",
        "image_url": "%s"
    }"""%(img)

    file.write(k)
    file.close()

def mint_js(img):
    file = open(r'scripts\mint-nft.js', 'w')
    k = """
    require("dotenv").config();
    require("./MyNFT.json").abi;
    const { JsonRpcProvider, Signer } = require("@ethersproject/providers");
    const ethers = require("ethers");

    // Create a JsonRpcProvider instance
    const rpcUrl = "https://rpc.testnet.mantle.xyz";
    const chainId = 5001;
    const provider = new JsonRpcProvider(rpcUrl, chainId);

    // Create a signer using the private key from the environment variable
    const privateKey = process.env.PRIV_KEY;
    const signer = new ethers.Wallet(privateKey, provider);

    // Get contract ABI and address
    const abi = require("../artifacts/contracts/MyNFT.sol/MyNFT.json").abi;
    const contractAddress = "0x941a364F4BDadbAbE876201200104a4d90042f77";

    // Create a contract instance
    const myNftContract = new ethers.Contract(contractAddress, abi, signer);

    // Get the NFT Metadata IPFS URL
    const tokenUri = "%s";

    // Call mintNFT function
    async function mintNFT() {
        let nftTxn = await myNftContract.mintNFT(signer.address, tokenUri);
        await nftTxn.wait();
        console.log(`NFT Minted! Check it out at: https://explorer.testnet.mantle.xyz/tx/${nftTxn.hash}`);
    }

    mintNFT()
        .then(() => process.exit(0))
        .catch(error => {
            console.error(error);
            process.exit(1);
        });
    """%(img)

    file.write(k)
    file.close()

def mantle_run(k):
    images = {"n1":"https://gateway.pinata.cloud/ipfs/QmapU3Qn5hqhuPx2qfPz8wPE5NvXyjVsJhojdhEKJ6zBSY?_gl=1*fwqyp3*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n2":"https://gateway.pinata.cloud/ipfs/Qmf8rVFUXwUeBRMfffhuo2WYaS7XJG282PdTuhnT95bn55?_gl=1*fwqyp3*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n3":"https://gateway.pinata.cloud/ipfs/Qmdm1QSWKgbYmV9A11CUaybRmmJGwRMULQULJ78pq99v1Y?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n4":"https://gateway.pinata.cloud/ipfs/QmQKrqBKLbWqtLYSSfdmpEPwjnTtPMBJBYND9CiLBSkWKD?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n5":"https://gateway.pinata.cloud/ipfs/Qmdo3gXuJ5vTf2iEJSsjQKX9ioYPHfmKYWdws7s1VDNMeA?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w"}
    img_url = images[k] 
    nft_meta(img_url)
    mint_js(img_url)
    node_script_path = r'scripts/mint-nft.js'
    result = subprocess.run(['node', node_script_path], capture_output=True, text=True) 
    print(result.stdout)
    push_chat(result.stdout[29:-1], img_url)
    return result.stdout[:-1]

def mongo_find():
    url = "https://data.mongodb-api.com/app/data-stoly/endpoint/data/v1/action/find"

    headers = {
        "Content-Type": "application/json",
        "apiKey": "V2jAj0WKRWitf1Tzw0UdTg5cCcWckSZLErF4AAOcVEJavrOO65MY6Ia65uOQDazQ"
    }

    payload = {
        "dataSource": "Cluster0",
        "database": "Ethforall_blogs",
        "collection": "games"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.text
    data = json.loads(data)
    return data

def mongo_resp():
    url = "https://data.mongodb-api.com/app/data-stoly/endpoint/data/v1/action/find"

    headers = {
        "Content-Type": "application/json",
        "apiKey": "V2jAj0WKRWitf1Tzw0UdTg5cCcWckSZLErF4AAOcVEJavrOO65MY6Ia65uOQDazQ"
    }

    payload = {
        "dataSource": "Cluster0",
        "database": "Ethforall_blogs",
        "collection": "games"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.text
    data = json.loads(data)
    return data

def nft_randomizer():
    k = random.choice(['n1','n2',"n3","n4",'n5'])
    d1 = {"n1":"https://gateway.pinata.cloud/ipfs/QmapU3Qn5hqhuPx2qfPz8wPE5NvXyjVsJhojdhEKJ6zBSY?_gl=1*fwqyp3*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n2":"https://gateway.pinata.cloud/ipfs/Qmf8rVFUXwUeBRMfffhuo2WYaS7XJG282PdTuhnT95bn55?_gl=1*fwqyp3*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n3":"https://gateway.pinata.cloud/ipfs/Qmdm1QSWKgbYmV9A11CUaybRmmJGwRMULQULJ78pq99v1Y?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n4":"https://gateway.pinata.cloud/ipfs/QmQKrqBKLbWqtLYSSfdmpEPwjnTtPMBJBYND9CiLBSkWKD?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w",
         "n5":"https://gateway.pinata.cloud/ipfs/Qmdo3gXuJ5vTf2iEJSsjQKX9ioYPHfmKYWdws7s1VDNMeA?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w"}
    d2 = {"n1":"Space Panda",
          "n2":"Phoenix",
          "n3":"Glock",
          "n4":"Golden mask",
          "n5":"Space Warrior"}
    d3 = {"n1":"Silver - rare",
          "n2":"Red - Common",
          "n3":"Silver - rare",
          "n4":"Gold - Super rare",
          "n5":"Platinum - Ultra rare"}
    
    nft_url = d1[k]
    nft_name = d2[k]
    nft_rarity = d3[k]

    return nft_url, k, nft_name, nft_rarity

def getNFT():
    nft_url, k , nft_name, nft_rarity = nft_randomizer()
    djson = mongo_resp()
    djson = djson['documents'][0]
    
    for i in range(5):
        try:
            djson['nft{}'.format(i)]
        except:
            djson['nft{}'.format(i)] = [nft_url,nft_name, nft_rarity]
            break
    #print(djson)

    url = "https://data.mongodb-api.com/app/data-stoly/endpoint/data/v1/action/updateOne"

    headers = {
        "Content-Type": "application/json",
        "apiKey": "V2jAj0WKRWitf1Tzw0UdTg5cCcWckSZLErF4AAOcVEJavrOO65MY6Ia65uOQDazQ"
    }

    payload = {
    "dataSource": "Cluster0",
    "database": "Ethforall_blogs",
    "collection": "games",
    "filter":{"_id":"641e12a34a7c02ae7ef31999"},
    "update":{"$set": djson}
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    except:
        payload = {
            "dataSource": "Cluster0",
            "database": "Ethforall_blogs",
            "collection": "games",
            "document": djson
            }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    return k


app=Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return {"server":"active"}

"""
    metamask wallet
    game name
    price
    reciever address

"""

@app.route("/nftmint")
@cross_origin()
def nftmintyo():
    d = getNFT()
    mantle_url = mantle_run(d)
    print(mantle_url)
    return({
        "nft":d,
        "mantle_link":mantle_url
    })

@app.route("/express")
@cross_origin()
def express():
    k = mongo_find()
    #return k['documents'][0]
    return k

if __name__=='__main__':
    app.run(debug=True)
