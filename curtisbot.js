require('dotenv').config();
const fs = require('fs');
const readline = require('readline-sync');
const { ethers } = require('ethers');

const rpcUrl = "https://curtis.rpc.caldera.xyz/http";
const provider = new ethers.JsonRpcProvider(rpcUrl);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

const addressCurtisToArb = "0x0000000000000000000000000000000000000064"; // alamat bridge Curtis > Arb
const addressArbToCurtis = "0x990A3402F3358A1Ac9886c42d12A5C47aD97cb94"; // alamat bridge Arb > Curtis

// Load ABI 
const abiC2A = JSON.parse(fs.readFileSync('abiCurtisToArbitrum.json'));
const abiA2C = JSON.parse(fs.readFileSync('abiArbitrumToCurtis.json'));

// Inisialisasi contract
const contractC2A = new ethers.Contract(addressCurtisToArb, abiC2A, wallet);
const contractA2C = new ethers.Contract(addressArbToCurtis, abiA2C, wallet);

const totalC2A = readline.questionInt("Masukkan jumlah bridge Curtis ke Arbitrum: ");
const totalA2C = readline.questionInt("Masukkan jumlah bridge Arbitrum ke Curtis: ");

async function bridgeCurtisToArb() {
  for(let i = 0; i < totalC2A; i++) {
    try {
      // Ganti dengan fungsi & parameter sesuai kontrak
      // misal: contractC2A.withdrawEth(destinationAddress, {value: amount})
      // contoh random (update sesuai kebutuhan):
      const tx = await contractC2A.withdrawEth(0x0000000000000000000000000000000000000064, { value: ethers.parseUnits("0.001", 18) });
      console.log(`Bridge Curtis -> Arbitrum tx ${i + 1}:`, tx.hash);
      await tx.wait();
      console.log(`Bridge Curtis -> Arbitrum tx ${i + 1} confirmed!\n`);
    } catch (err) {
      console.error("Error pada bridge C2A:", err);
    }
  }
}

async function bridgeArbToCurtis() {
  for(let i = 0; i < totalA2C; i++) {
    try {
      // Ganti dengan fungsi & parameter sesuai kontrak
      // misal: contractA2C.sendTxToL1(destinationAddress, encodedData, {value: ...})
      // contoh random (update sesuai kebutuhan):
      const tx = await contractA2C.sendTxToL1(0x990A3402F3358A1Ac9886c42d12A5C47aD97cb94, "0x", { value: ethers.parseUnits("0.001", 18) });
      console.log(`Bridge Arbitrum -> Curtis tx ${i + 1}:`, tx.hash);
      await tx.wait();
      console.log(`Bridge Arbitrum -> Curtis tx ${i + 1} confirmed!\n`);
    } catch (err) {
      console.error("Error pada bridge A2C:", err);
    }
  }
}

(async () => {
  if (totalC2A > 0) await bridgeCurtisToArb();
  if (totalA2C > 0) await bridgeArbToCurtis();
  console.log("All bridge tasks completed!");
})();
