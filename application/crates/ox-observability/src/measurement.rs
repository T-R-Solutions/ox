#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Measurement<T> {
    Measured {
        value: T,
        source: String,
    },
    Estimated {
        value: T,
        method: String,
        source: String,
    },
    Derived {
        value: T,
        method: String,
        source: String,
    },
    Unknown,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Sample<T> {
    pub unit: String,
    pub period: std::ops::Range<std::time::SystemTime>,
    pub measurement: Measurement<T>,
}
