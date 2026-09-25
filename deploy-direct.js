import { ethers } from "ethers";
import fs from "fs";

async function main() {
  // Connect to Wirex Pay Testnet or XO Chain Testnet via provider URL
  const provider = new ethers.JsonRpcProvider("https://rpc-dev.wirexpaychain.com"); // or "https://testnet-rpc-1.xo.market"
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

  console.log("Deploying from account:", wallet.address);

  // Load your compiled artifact abi and bytecode if available, 
  // or supply them directly here from your build artifacts folder
  const rawArtifact = fs.readFileSync("./artifacts/contracts/MyCustomToken.sol/MyCustomToken.json", "utf8");
  const artifact = JSON.parse(rawArtifact);

  const Factory = new ethers.ContractFactory(artifact.abi, artifact.bytecode, wallet);

  console.log("Deploying contract...");
  const contract = await Factory.deploy(wallet.address);
  await contract.waitForDeployment();

  console.log("Contract deployed successfully to:", await contract.getAddress());
}

main().catch(console.error);

