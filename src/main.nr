#[contract]
mod nullifiable_voting {
    struct Storage {
        votes: Field,
        nullifiers: Field
    }

    impl NullifiableVoting for Storage {
        fn init() -> pub Self {
            Self {
                votes: 0,
                nullifiers: 0
            }
        }

        fn cast_vote(self, vote: Field) -> pub Self {
            self.votes = vote;
            self
        }
    }
}

#[test]
fn test_vote() {
    let initial_storage = NullifiableVoting::init();
    let updated_storage = initial_storage.cast_vote(1);
    assert(updated_storage.votes == 1);
}
