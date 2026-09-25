import { defineConfig, configVariable } from "hardhat/config";
import hardhatEthers from "@nomicfoundation/hardhat-ethers";

export default defineConfig({
  plugins: [hardhatEthers],
  solidity: "0.8.20",
  networks: {
    xoTestnet: {
      type: "http",
      chainType: "l1",
      url: "https://testnet-rpc-1.xo.market",
      chainId: 1000101,
      accounts: [configVariable("PRIVATE_KEY")]
    },
    wirexTestnet: {
      type: "http",
      chainType: "l1",
      url: "https://rpc-dev.wirexpaychain.com",
      chainId: 1001996,
      accounts: [configVariable("PRIVATE_KEY")]
    }
  }
});

