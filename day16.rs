use common::get_input;
use std::collections::HashMap;
use regex::Regex;

type Input = Vec<HashMap<String, usize>>;

fn part1(sues: &Input) -> usize {
    let facts = HashMap::from([ 
        ("children", 3),
        ("cats", 7),
        ("samoyeds", 2),
        ("pomeranians", 3),
        ("akitas", 0),
        ("vizslas", 0),
        ("goldfish", 5),
        ("trees", 3),
        ("cars", 2),
        ("perfumes", 1),
    ]);
    let matches: Vec<&HashMap<String, usize>> = sues.iter().filter(|sue| sue.iter().all(|(fact, value)| {
        fact == "Sue" ||
        facts[fact.as_str()] == *value
    })).collect();
    assert!(matches.len() == 1);
    matches[0]["Sue"]
}

fn part2(sues: &Input) -> usize {
    let facts = HashMap::from([ 
        ("children", 3),
        ("cats", 7),
        ("samoyeds", 2),
        ("pomeranians", 3),
        ("akitas", 0),
        ("vizslas", 0),
        ("goldfish", 5),
        ("trees", 3),
        ("cars", 2),
        ("perfumes", 1),
    ]);
    let matches: Vec<&HashMap<String, usize>> = sues.iter().filter(|sue| sue.iter().all(|(fact, value)| {
        match fact.as_str() {
            "Sue" => true,
            f if f == "cats" || f == "trees" => facts[f] < *value,
            f if f == "pomeranians" || f == "goldfish" => facts[f] > *value,
            f => facts[f] == *value
        }
    })).collect();
    assert!(matches.len() == 1);
    matches[0]["Sue"]
}

fn parse(text: String) -> Input {
    let re_ader = Regex::new(r"^Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)$").unwrap();
    text.trim().split("\n").map(|line| {
        let captures = re_ader.captures(line).unwrap();
        let mut facts: HashMap<String, usize> = (1..4).map(|n| (
                captures.get(2*n).unwrap().as_str().to_string(),
                captures.get(2*n+1).unwrap().as_str().parse::<usize>().unwrap()
        )).collect();
        facts.insert("Sue".to_string(), captures.get(1).unwrap().as_str().parse::<usize>().unwrap());
        facts
    }).collect()
}

fn main() {
    let input = parse(get_input(16, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
