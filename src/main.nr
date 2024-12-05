use dep::aztec::macros::aztec;
use crate::plume::*;

#[aztec]
contract NullifiableVoting {
    use dep::aztec::{
        keys::getters::get_public_keys,
        macros::{functions::*, storage::storage},
    };
    use dep::aztec::prelude::*;

    #[storage]
    struct Storage<Context> {
        admin: PublicMutable<AztecAddress, Context>,
        tally: Map<Field, PublicMutable<Field, Context>, Context>,
        vote_ended: PublicMutable<bool, Context>,
        nullifiers: Map<Field, PublicMutable<bool, Context>, Context>, // Track used nullifiers
    }

    #[public]
    #[initializer]
    fn constructor(admin: AztecAddress) {
        storage.admin.write(admin);
        storage.vote_ended.write(false);
    }

    #[private]
    fn cast_vote(candidate: Field) {
        let msg_sender_npk_m_hash = get_public_keys(context.msg_sender()).npk_m.hash();
        let secret = context.request_nsk_app(msg_sender_npk_m_hash);
        let nullifier = generate_nullifier(context.msg_sender().to_field(), secret);
        context.push_nullifier(nullifier);
        NullifiableVoting::at(context.this_address()).add_to_tally_public(candidate).enqueue(&mut context);
    }

    #[public]
    #[internal]
    fn add_to_tally_public(candidate: Field) {
        assert(storage.vote_ended.read() == false, "Vote has ended");
        let new_tally = storage.tally.at(candidate).read() + 1;
        storage.tally.at(candidate).write(new_tally);
    }

    #[public]
    fn end_vote() {
        assert(storage.admin.read().eq(context.msg_sender()), "Only admin can end votes");
        storage.vote_ended.write(true);
    }

    unconstrained fn get_vote(candidate: Field) -> pub Field {
        storage.tally.at(candidate).read()
    }

    #[private]
    fn cast_vote_with_nullifier(
        candidate: Field,
        signature: PlumeSignature,
        pk: [Field; 2]
    ) {
        // Verify signature and nullifier
        assert(verify_nullifiable_signature(
            context.msg_sender().to_field(),
            pk,
            signature
        ), "Invalid signature");

        // Check if nullifier has been used
        assert(storage.nullifiers.at(signature.nullifier).read() == false, "Nullifier already used");

        // Mark nullifier as used
        storage.nullifiers.at(signature.nullifier).write(true);

        // Cast vote
        add_to_tally_public(candidate);
    }
}
