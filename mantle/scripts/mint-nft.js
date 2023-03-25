
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
    const tokenUri = "https://gateway.pinata.cloud/ipfs/Qmdm1QSWKgbYmV9A11CUaybRmmJGwRMULQULJ78pq99v1Y?_gl=1*1pulrcs*_ga*MjAyYWIyYWUtMmRmYi00M2RiLWFlMjctYzNkOTgyYmZjYzIy*_ga_5RMPXG14TE*MTY3OTU4Mjk4Ny4xNC4wLjE2Nzk1ODI5OTkuNDguMC4w";

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
    