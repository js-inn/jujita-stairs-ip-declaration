import { ethers } from "ethers";
import fs from "fs";
import path from "path";
import solc from "solc";
import { pathToFileURL } from "url";

async function main() {
  const chainIdArg = process.argv[2] || "10088";
  console.log(`Target Chain ID: ${chainIdArg}`);

  // Automatically locate the chain configuration file
  // Searches common patterns like 'chainid-{chainId}.js' in the current workspace or subdirectories
  const possiblePaths = [
    `./chainid-${chainIdArg}.js`,
    `./constants/additionalChainRegistry/chainid-${chainIdArg}.js`,
    `./registry/chainid-${chainIdArg}.js`
  ];

  let configPath = null;
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      configPath = p;
      break;
    }
  }

  if (!configPath) {
    console.error(`Error: Could not find configuration file for Chain ID ${chainIdArg}.`);
    console.error("Make sure a file named chainid-" + chainIdArg + ".js exists in your workspace.");
    process.exit(1);
  }

  console.log(`Loading configuration from: ${configPath}`);
  
  // Dynamically import the ES module configuration file
  const chainModule = await import(pathToFileURL(path.resolve(configPath)).href);
  const chainData = chainModule.default || chainModule.data || chainModule;

  // Extract RPC endpoint (handling both array and string formats)
  const rpcUrl = Array.isArray(chainData.rpc) ? chainData.rpc[0] : chainData.rpc;
  const networkName = chainData.name || `Chain ${chainIdArg}`;

  if (!rpcUrl) {
    console.error(`Error: No valid RPC endpoint found in configuration for ${networkName}.`);
    process.exit(1);
  }

  console.log(`Connecting to network: ${networkName} (${rpcUrl})`);

  // 1. Compile contract
  const contractPath = "./contracts/MyCustomToken.sol";
  if (!fs.existsSync(contractPath)) {
    console.error(`Error: Could not find contract at ${contractPath}`);
    process.exit(1);
  }
  const sourceCode = fs.readFileSync(contractPath, "utf8");

  const input = {
    language: "Solidity",
    sources: {
      "MyCustomToken.sol": { content: sourceCode },
    },
    settings: {
      outputSelection: { "*": { "*": ["abi", "evm.bytecode"] } },
    },
  };

  function findImports(importPath) {
    try {
      const resolvedPath = path.resolve("node_modules", importPath);
      if (fs.existsSync(resolvedPath)) {
        return { contents: fs.readFileSync(resolvedPath, "utf8") };
      }
      return { error: "File not found" };
    } catch (e) {
      return { error: e.message };
    }
  }

  console.log("Compiling contract using pure-JS compiler...");
  const output = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));

  if (output.errors) {
    let hasError = false;
    output.errors.forEach((err) => {
      console.error(err.formattedMessage);
      if (err.severity === "error") hasError = true;
    });
    if (hasError) {
      console.error("Compilation failed.");
      process.exit(1);
    }
  }

  const targetName = "MyCustomToken";
  const contractData = output.contracts["MyCustomToken.sol"][targetName];
  if (!contractData) {
    console.error("Error: MyCustomToken contract not found in compilation output.");
    process.exit(1);
  }

  const abi = contractData.abi;
  const bytecode = contractData.evm.bytecode.object;

  // 2. Setup Provider & Wallet
  const provider = new ethers.JsonRpcProvider(rpcUrl);

  const privKey = process.env.PRIVATE_KEY;
  if (!privKey || privKey === "0xYourActualRealPrivateKeyHere" || privKey.length !== 66) {
    console.error("Error: PRIVATE_KEY environment variable is missing, invalid, or still set to a placeholder.");
    process.exit(1);
  }

  const wallet = new ethers.Wallet(privKey, provider);
  console.log("Deploying from account:", wallet.address);

  // 3. Deploy
  const factory = new ethers.ContractFactory(abi, bytecode, wallet);
  console.log("Broadcasting deployment transaction...");
  
  const contract = await factory.deploy(wallet.address);
  await contract.waitForDeployment();

  console.log(`${targetName} deployed successfully on ${networkName} to:`, await contract.getAddress());
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exit(1);
});

