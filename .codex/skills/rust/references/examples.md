# Short decision examples

These examples are original illustrations of the decisions in [design](design.md), not copied book listings. Each Rust block is self-contained. From the repository root, check this file with `rustdoc --test skills/rust/references/examples.md --edition=2021`; use `--edition=2024` for the second supported example configuration. They use the standard library only. After copying this skill, substitute the actual path to its `references/examples.md`. Adapting their contracts still requires checking the target project's edition and MSRV.

## Borrow the result from the relevant input

The result borrows the contents, not the temporary query. An owned return would be appropriate if it must outlive those contents. Empty input is ordinary absence.

```rust
fn matching_line<'a>(contents: &'a str, query: &str) -> Option<&'a str> {
    contents.lines().find(|line| line.contains(query))
}

fn main() {
    let contents = String::from(
        "alpha
café
omega",
    );
    let found = {
        let query = String::from("fé");
        matching_line(&contents, &query)
    };
    assert_eq!(found, Some("café"));
    assert_eq!(matching_line("", "missing"), None);
}
```

This deliberately uses substring matching, not normalization or linguistic equivalence. Basis: TRPL ch. 4 and 10, RFR ch. 1, ER Items 8 and 14–15.

## Validate once and retain the invariant

A private field prevents callers outside the module from bypassing construction. Invalid input is an expected error; a panicking constructor would instead need an explicit programmer-contract rationale. The upper bound is illustrative domain policy, not a Rust limit.

```rust
mod domain {
    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub struct BatchSize(u16);

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub struct InvalidBatchSize;

    impl std::fmt::Display for InvalidBatchSize {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            f.write_str("batch size must be between 1 and 1000")
        }
    }

    impl std::error::Error for InvalidBatchSize {}

    impl TryFrom<u16> for BatchSize {
        type Error = InvalidBatchSize;

        fn try_from(value: u16) -> Result<Self, Self::Error> {
            if (1..=1000).contains(&value) {
                Ok(Self(value))
            } else {
                Err(InvalidBatchSize)
            }
        }
    }

    impl BatchSize {
        pub fn get(self) -> u16 {
            self.0
        }
    }
}

fn main() {
    use domain::{BatchSize, InvalidBatchSize};

    assert_eq!(BatchSize::try_from(1).map(BatchSize::get), Ok(1));
    assert_eq!(BatchSize::try_from(1000).map(BatchSize::get), Ok(1000));
    assert_eq!(BatchSize::try_from(0), Err(InvalidBatchSize));
    assert_eq!(BatchSize::try_from(1001), Err(InvalidBatchSize));
}
```

Basis: ER Items 1 and 5, RFR ch. 2–4, ZTP ch. 6, and TRPL ch. 9.3. The example uses editions 2021/2024, where `TryFrom` is in the prelude; an earlier edition needs an explicit import and still needs an appropriate compiler version.

## Preserve parsing failures while collecting

Here any invalid item fails the operation. A partial-success contract would instead return accepted values together with rejected items or explicitly document dropping failures.

```rust
fn parse_counts(input: &str) -> Result<Vec<u16>, std::num::ParseIntError> {
    input.split_whitespace().map(str::parse).collect()
}

fn main() {
    assert_eq!(
        parse_counts("2 4 8").expect("all tokens are valid u16 values"),
        vec![2, 4, 8]
    );
    assert!(parse_counts("2 invalid 8").is_err());
    assert!(parse_counts("65536").is_err());
    assert_eq!(
        parse_counts("").expect("empty input has no invalid tokens"),
        Vec::<u16>::new()
    );
}
```

The `expect` calls belong to the demonstration assertions, where failure should fail the test. The parser itself returns a recoverable error. Basis: ER Items 4 and 9; ZTP ch. 9, p. 380; TRPL ch. 9 and 13.
