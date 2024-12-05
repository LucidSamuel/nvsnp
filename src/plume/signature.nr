use dep::std;
use dep::aztec::ecdsa::*;
use crate::plume::PlumeSignature;

pub fn sign_nullifiable(
    msg: Field,
    sk: Field,
    nullifier: Field
) -> PlumeSignature {
    let k = std::hash::pedersen_hash([msg, sk]); // Deterministic k value
    let (r, s) = sign_ecdsa_secp256k1(msg, sk, k);
    
    PlumeSignature {
        r,
        s,
        nullifier
    }
}
