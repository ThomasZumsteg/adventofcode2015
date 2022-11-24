use common::get_input;
use std::collections::{HashMap, HashSet};

type Input = Vec<String>;

fn part1_rules(&string: &&String) -> bool {
    let mut doubles: HashMap<String, Vec<usize>> = HashMap::new();
    let mut singles = HashMap::new();
    for (i, c) in string.chars().enumerate() {
        *singles.entry(c).or_insert(0) += 1;
        if i == 0 { continue }
        let double = string[(i-1)..i+1].to_string();
        if let Some(values) = doubles.get_mut(&double) {
            values.push(i)
        } else {
            doubles.insert(double, vec![i]);
        }
    }
    if "aeiou".chars().filter_map(|c| singles.get(&c)).sum::<usize>() < 3 {
        return false
    }
    if !doubles.keys().any(|d| d.chars().nth(0) == d.chars().nth(1)) {
        return false
    }
    if vec!["ab", "cd", "pq", "xy"].iter().any(|key| doubles.contains_key(&key.to_string())) {
        return false
    }
    true
}

fn part1(strings: &Input) -> usize {
    strings.iter().filter(part1_rules).count()
}

fn part2_rules(&string: &&String) -> bool {
    let mut doubles: HashMap<String, Vec<usize>> = HashMap::new();
    let mut triples: HashSet<String> = HashSet::new();
    for i in 1..string.len() {
        let double = string[(i-1)..i+1].to_string();
        if let Some(values) = doubles.get_mut(&double) {
            if values.last() != Some(&(i-1)) {
                values.push(i);
            }
        } else {
            doubles.insert(double, vec![i]);
        }
        if i < 2 {
            continue
        }
        let triple = string[(i-2)..i+1].to_string();
        triples.insert(triple);
    }
    if !doubles.values().any(|v| v.len() > 1) {
        return false
    }
    if !triples.iter().any(|t| t.chars().nth(0) == t.chars().nth(2)) {
        return false
    }
    true
}


fn part2(strings: &Input) -> usize {
    strings.iter().filter(part2_rules).count()
}

fn parse(text: String) -> Input {
    text.trim().split("\n").map(|s| s.to_string()).collect()
}

fn main() {
    let input = parse(get_input(05, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
