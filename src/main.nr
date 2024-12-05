mod test_ecdsa;
fn main(x: Field, y: pub Field) {
    assert(x != y);
}

#[test]
fn test_main() {
    main(1, 2);

    // Uncomment to make test fail
    // main(1, 1);
}

fn ecdsa_verify(h_msg: Field, pk: [Field; 2], r: Field, s: Field, n: Field, g: [Field; 2]) -> bool {
    // Your ECDSA verification implementation
}
