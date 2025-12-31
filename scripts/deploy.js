const { ethers } = require("hardhat");

async function main() {
    // Get the contract factory
    const Traceability = await ethers.getContractFactory("Traceability");

    // Deploy the contract (ethers v6 auto-waits)
    const traceability = await Traceability.deploy();

    console.log("Traceability contract deployed to:", traceability.target);
}

// Run the deployment script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
