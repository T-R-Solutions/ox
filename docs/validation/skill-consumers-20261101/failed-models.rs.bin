//! Bounded evaluation consumers. Contracts and exclusions are in README.md.
use std::{
    collections::{BTreeMap, BTreeSet, VecDeque},
    ops::Range,
    path::{Path, PathBuf},
};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Usage {
    pub input: u64,
    pub cached: u64,
    pub output: u64,
    pub occurred: i64,
}
#[derive(Default)]
pub struct Ledger {
    events: BTreeMap<(String, String), Usage>,
    pub context: u64,
}
impl Ledger {
    pub fn insert(&mut self, provider: &str, id: &str, event: Usage) -> Result<bool, String> {
        if event.cached > event.input {
            return Err("cache exceeds input".into());
        }
        let key = (provider.into(), id.into());
        if let Some(old) = self.events.get(&key) {
            return if old == &event {
                Ok(false)
            } else {
                Err("conflicting duplicate".into())
            };
        }
        self.events.insert(key, event);
        Ok(true)
    }
    pub fn totals(&self, day: i64, offset_seconds: i32) -> Result<(u64, u64, u64), String> {
        if !(-86400..86400).contains(&offset_seconds) {
            return Err("offset".into());
        }
        let mut total = (0u64, 0u64, 0u64);
        for e in self.events.values() {
            let local = e
                .occurred
                .checked_add(i64::from(offset_seconds))
                .ok_or("time overflow")?;
            if local.div_euclid(86400) != day {
                continue;
            }
            total.0 = total.0.checked_add(e.input).ok_or("overflow")?;
            total.1 = total.1.checked_add(e.cached).ok_or("overflow")?;
            total.2 = total.2.checked_add(e.output).ok_or("overflow")?;
        }
        Ok(total)
    }
    // Integer microcurrency units per token, deliberately no float or market price lookup.
    pub fn cost(
        &self,
        day: i64,
        offset: i32,
        rate: Option<(u64, u64, u64)>,
    ) -> Result<Option<u64>, String> {
        let Some((input_rate, cache_rate, output_rate)) = rate else {
            return Ok(None);
        };
        let (input, cached, output) = self.totals(day, offset)?;
        let a = (input - cached).checked_mul(input_rate).ok_or("overflow")?;
        let b = cached.checked_mul(cache_rate).ok_or("overflow")?;
        let c = output.checked_mul(output_rate).ok_or("overflow")?;
        Ok(Some(
            a.checked_add(b)
                .and_then(|n| n.checked_add(c))
                .ok_or("overflow")?,
        ))
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Hit {
    pub path: String,
    pub range: Range<usize>,
    pub snapshot: u64,
    pub method: &'static str,
    pub bytes: Vec<u8>,
}
#[derive(Default)]
pub struct Index {
    generation: u64,
    documents: BTreeMap<String, Vec<u8>>,
    symbols: BTreeMap<String, Vec<Hit>>,
    pub parsed_files: usize,
}
impl Index {
    pub fn replace(&mut self, documents: BTreeMap<String, Vec<u8>>) -> Result<(), String> {
        let next = self
            .generation
            .checked_add(1)
            .ok_or("generation overflow")?;
        let mut symbols: BTreeMap<String, Vec<Hit>> = BTreeMap::new();
        let mut parsed_files = 0;
        for (path, bytes) in &documents {
            if self.documents.get(path) == Some(bytes) {
                for (name, hits) in &self.symbols {
                    for old in hits.iter().filter(|h| &h.path == path) {
                        let mut hit = old.clone();
                        hit.snapshot = next;
                        symbols.entry(name.clone()).or_default().push(hit);
                    }
                }
                continue;
            }
            parsed_files += 1;
            let content = std::str::from_utf8(bytes).map_err(|_| "invalid UTF8")?;
            let mut offset = 0;
            for line in content.split_inclusive('\n') {
                if let Some(rest) = line.strip_prefix("fn ") {
                    let name = rest.trim_end();
                    if name.is_empty() || !name.chars().all(|c| c.is_alphanumeric() || c == '_') {
                        return Err("invalid fixture declaration".into());
                    }
                    symbols.entry(name.into()).or_default().push(Hit {
                        path: path.clone(),
                        range: offset + 3..offset + 3 + name.len(),
                        snapshot: next,
                        method: "fixture-syntax-v1",
                        bytes: bytes.clone(),
                    });
                }
                offset += line.len();
            }
        }
        self.parsed_files = parsed_files;
        self.documents = documents;
        self.symbols = symbols;
        self.generation = next;
        Ok(())
    }
    pub fn apply_changes(&mut self, changes: Vec<(String, Option<Vec<u8>>)>) -> Result<(), String> {
        let mut next = self.documents.clone();
        for (path, bytes) in changes {
            match bytes {
                Some(bytes) => {
                    next.insert(path, bytes);
                }
                None => {
                    next.remove(&path);
                }
            }
        }
        self.replace(next)
    }
    pub fn query(&self, name: &str) -> Vec<Hit> {
        self.symbols.get(name).cloned().unwrap_or_default()
    }
    pub fn resolve_without_provider(&self, name: &str) -> (Vec<Hit>, &'static str, bool) {
        (self.query(name), "semantic-provider-unavailable", false)
    }
    pub fn resolve_with_provider(
        &self,
        name: &str,
        executable: &Path,
    ) -> Result<(Vec<Hit>, &'static str, bool), String> {
        // This fixture consumer has no LSP decoder: never infer semantic success from exit 0.
        match std::process::Command::new(executable)
            .arg("--version")
            .output()
        {
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                Ok(self.resolve_without_provider(name))
            }
            Err(e) => Err(e.to_string()),
            Ok(_) => Err("semantic protocol unsupported by fixture consumer".into()),
        }
    }
    pub fn current(&self, hit: &Hit) -> bool {
        hit.snapshot == self.generation && self.documents.get(&hit.path) == Some(&hit.bytes)
    }
}

#[derive(Clone, Debug)]
pub enum Evidence {
    Resolved {
        path: String,
        bytes: Vec<u8>,
        range: Range<usize>,
        method: String,
    },
    Inferred,
}
#[derive(Clone, Debug)]
pub struct Edge {
    pub from: String,
    pub to: String,
    pub verified: bool,
    pub evidence: Evidence,
}
#[derive(Default)]
pub struct Graph {
    edges: Vec<Edge>,
}
#[derive(Debug)]
pub struct Subgraph {
    pub nodes: BTreeSet<String>,
    pub examined: usize,
    pub truncated: bool,
}
// The synthetic language resolves only unique functions within one file.
fn fixture_call(bytes: &[u8], range: &Range<usize>, from: &str, to: &str) -> bool {
    let Ok(source) = std::str::from_utf8(bytes) else {
        return false;
    };
    let declarations: Vec<_> = source
        .lines()
        .filter_map(|line| line.strip_prefix("fn "))
        .collect();
    if declarations.iter().filter(|name| **name == from).count() != 1
        || declarations.iter().filter(|name| **name == to).count() != 1
    {
        return false;
    }
    let mut caller = None;
    let mut offset = 0;
    for line in source.split_inclusive('\n') {
        if let Some(name) = line.trim_end().strip_prefix("fn ") {
            caller = Some(name);
        }
        if offset == range.start {
            return caller == Some(from) && range.end == offset + line.trim_end().len();
        }
        offset += line.len();
    }
    false
}
impl Graph {
    pub fn add(&mut self, e: Edge) -> Result<(), String> {
        if e.verified {
            match &e.evidence {
                Evidence::Resolved {
                    bytes,
                    range,
                    method,
                    ..
                } if method == "fixture-resolver-v1"
                    && bytes.get(range.clone()) == Some(format!("call {}", e.to).as_bytes())
                    && fixture_call(bytes, range, &e.from, &e.to) => {}
                _ => return Err("verified edge lacks matching source evidence".into()),
            }
        }
        self.edges.push(e);
        Ok(())
    }
    pub fn edges(&self) -> &[Edge] {
        &self.edges
    }
    pub fn reconcile(&mut self, docs: &BTreeMap<String, Vec<u8>>) {
        self.edges.retain(|e| match &e.evidence {
            Evidence::Resolved { path, bytes, .. } => docs.get(path) == Some(bytes),
            Evidence::Inferred => false,
        });
    }
    pub fn subgraph(&self, start: &str, max_nodes: usize, max_examined: usize) -> Subgraph {
        let mut out = Subgraph {
            nodes: BTreeSet::new(),
            examined: 0,
            truncated: false,
        };
        if max_nodes == 0 {
            out.truncated = true;
            return out;
        }
        out.nodes.insert(start.into());
        let mut queue = VecDeque::from([start.to_owned()]);
        while let Some(n) = queue.pop_front() {
            // All candidate scans count, including nonmatching edges. Budget bounds actual work.
            for e in &self.edges {
                if out.examined == max_examined {
                    out.truncated = true;
                    return out;
                }
                out.examined += 1;
                if e.from != n || out.nodes.contains(&e.to) {
                    continue;
                }
                if out.nodes.len() == max_nodes {
                    out.truncated = true;
                    return out;
                }
                out.nodes.insert(e.to.clone());
                queue.push_back(e.to.clone());
            }
        }
        out
    }
}

#[derive(Debug)]
pub struct Projection {
    pub display: String,
    pub fallback: bool,
    pub truncated: bool,
    pub raw: PathBuf,
    pub exit: i32,
    pub estimated_tokens: usize,
    pub billed_tokens: Option<u64>,
}
pub fn project(bytes: &[u8], exit: i32, raw: &Path, budget: usize) -> std::io::Result<Projection> {
    use std::io::Write;
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(raw)?;
    file.write_all(bytes)?;
    file.sync_all()?;
    let valid = std::str::from_utf8(bytes);
    let fallback = valid.is_err()
        || bytes
            .iter()
            .any(|b| (*b < 32 && ![b'\n', b'\t'].contains(b)) || *b == 127)
        || !valid
            .as_ref()
            .map(|s| s.starts_with("error:") || s.starts_with("ok:"))
            .unwrap_or(false);
    // Escape terminal controls and undecodable bytes in the display only.
    // Prioritize known error lines so a long successful prefix cannot bury the location.
    let prioritized;
    let display_bytes = if !fallback {
        let source = valid.as_ref().expect("valid known format");
        let errors: Vec<_> = source
            .lines()
            .filter(|line| line.starts_with("error:"))
            .collect();
        prioritized = if errors.is_empty() {
            bytes.to_vec()
        } else {
            [errors.join("\n").as_bytes(), b"\n", bytes].concat()
        };
        prioritized.as_slice()
    } else {
        bytes
    };
    let escaped = display_bytes
        .iter()
        .map(|b| match b {
            b'\n' => "\n".into(),
            b'\t' => "\t".into(),
            32..=126 => (*b as char).to_string(),
            _ => format!("\\x{b:02x}"),
        })
        .collect::<String>();
    let header = format!(
        "exit={exit}; fallback={fallback}; raw={}; estimate=byte-heuristic; billing=unknown\n",
        raw.display()
    );
    let reserve = "\n[TRUNCATED: recover raw file]";
    if budget < header.len() + reserve.len() {
        return Err(std::io::Error::other(
            "budget cannot carry failure/retention envelope",
        ));
    }
    let room = budget - header.len() - reserve.len();
    let truncated = escaped.len() > room;
    let display = if truncated {
        format!("{header}{}{reserve}", &escaped[..room])
    } else {
        format!("{header}{escaped}")
    };
    Ok(Projection {
        display,
        fallback,
        truncated,
        raw: raw.to_owned(),
        exit,
        estimated_tokens: bytes.len().div_ceil(4),
        billed_tokens: None,
    })
}
