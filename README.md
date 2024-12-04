# Nullifiable Voting System Using Noir and PLUME

## Overview
This project implements a privacy-preserving voting system leveraging the PLUME nullifiable ECDSA signature scheme and Noir zkSNARK circuits. The system enables voters to cast anonymous votes, with support for nullification (revoking a vote) without compromising privacy.

## Features
- **Privacy-Preserving Voting:** Fully anonymous voting system using zkSNARKs.
- **Data Nullification:** Revocation of votes using PLUME nullifiers.
- **Zero-Knowledge Proofs:** Ensures correctness without exposing sensitive information.

## Technology Stack
- **Noir:** For creating zkSNARK circuits.
- **PLUME:** For nullifiable ECDSA signature scheme.
- **Rust:** Backend implementation.
- **Aztec Network:** Optional privacy-preserving layer.

## Usage
1. **Setup Environment:** Install required dependencies.
2. **Implement PLUME in Noir:** Adapt the PLUME nullifiable signature scheme.
3. **Build Circuits:** Create circuits to verify signatures and manage nullifiers.
4. **Integrate Backend:** Orchestrate the voting process and tally results.
5. **Test & Deploy:** Run tests and deploy to a secure environment.

---

### Progress
- [x] Setup environment.
- [ ] Implement PLUME in Noir.
- [ ] Build circuits.
- [ ] Create backend and integrate.
- [ ] Optimize and deploy.

# nvsnp
