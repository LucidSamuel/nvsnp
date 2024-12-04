fn main(
    h_msg: Field, 
    pk: Field, 
    r: Field, 
    s: Field, 
    nullifier: Field, 
    proof: Field, 
    sk: Field, 
    msg: Field
) -> bool {
    // Call the signature verification function
    let is_valid = verify_signature(h_msg, pk, r, s);

    // Call the nullifier validation function
    let is_nullifier_valid = verify_nullifier(nullifier, sk, msg);

    // Combine the checks
    return is_valid && is_nullifier_valid;
}

fn verify_signature(h_msg: Field, pk: Field, r: Field, s: Field) -> bool {
    return ecc::ecdsa_verify(h_msg, pk, r, s);
}

fn verify_nullifier(nullifier: Field, sk: Field, msg: Field) -> bool {
    // Hash the secret key and message together to generate a nullifier
    let computed_nullifier = sha256::hash(sk + msg);
    
    return computed_nullifier == nullifier;
}
