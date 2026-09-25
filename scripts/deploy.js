import hre from "hardhat";

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contract with account:", deployer.address);

  const MyCustomToken = await hre.ethers.getContractFactory("MyCustomToken");
  const token = await MyCustomToken.deploy(deployer.address);

  await token.waitForDeployment();
  console.log("MyCustomToken deployed to:", await token.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

