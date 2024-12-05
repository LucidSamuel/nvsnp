use dep::std;

pub fn generate_nullifier(
    msg: Field,
    pk_x: Field
) -> Field {
    std::hash::pedersen_hash([msg, pk_x])
}

pub fn verify_nullifier_not_used(
    nullifier: Field,
    used_nullifiers: [Field; 10] // Example size
) -> bool {
    let mut is_used = false;
    for i in 0..10 {
        if used_nullifiers[i] == nullifier {
            is_used = true;
            break;
        }
    }
    !is_used
}
