mod signature;
mod nullifier;

use dep::std;
use dep::aztec::ecdsa::*;

pub struct PlumeSignature {
    r: Field,
    s: Field,
    nullifier: Field
}

pub fn verify_nullifiable_signature(
    msg: Field,
    pk: [Field; 2],
    signature: PlumeSignature,
) -> bool {
    let valid_signature = verify_ecdsa_secp256k1(
        msg,
        pk[0],
        pk[1],
        signature.r,
        signature.s
    );

    let valid_nullifier = verify_nullifier(signature.nullifier, msg, pk[0]);
    
    valid_signature && valid_nullifier
}

fn verify_nullifier(nullifier: Field, msg: Field, pk_x: Field) -> bool {
    let expected = std::hash::pedersen_hash([msg, pk_x]);
    nullifier == expected
}
