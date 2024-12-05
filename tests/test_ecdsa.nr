use dep::std;
use dep::aztec::ecdsa::*;
use crate::plume::*;

#[test]
fn test_nullifiable_signature() {
    let h_msg = 53149569592524789644493163850982267525392973055378586746964677922035234800137;
    let pk_x = 100096422141634958090364064444190960274596218696503061031096636459309563376785;
    let pk_y = 110179556293605593341770451694039625307685825321260887149556731310264534197388;
    
    // Generate nullifier
    let nullifier = generate_nullifier(h_msg, pk_x);
    
    // Create signature
    let signature = sign_nullifiable(h_msg, pk_x, nullifier);
    
    // Verify signature
    let is_valid = verify_nullifiable_signature(h_msg, [pk_x, pk_y], signature);
    assert(is_valid);
    
    // Test nullifier uniqueness
    let different_msg = h_msg + 1;
    let different_nullifier = generate_nullifier(different_msg, pk_x);
    assert(nullifier != different_nullifier);
}
