use common::get_input;
use std::collections::VecDeque;
use serde_json::{self, Value};

type Input = Value;

fn part1(input: &Input) -> i64 { 
    let mut queue: VecDeque<&Value> = VecDeque::from(vec![input]);
    let mut total = 0;
    while let Some(item) = queue.pop_back() {
        match item {
            Value::Null => unimplemented!(),
            Value::Bool(_) => unimplemented!(),
            Value::Number(n) => total += n.as_i64().unwrap() as i64,
            Value::String(_) => {},
            Value::Array(v) => queue.append(&mut v.iter().collect()),
            Value::Object(m) => queue.append(&mut m.values().collect()),
        }
    };
    total
}

fn part2(input: &Input) -> i64 { 
    let mut queue: VecDeque<&Value> = VecDeque::from(vec![input]);
    let mut total = 0;
    while let Some(item) = queue.pop_back() {
        match item {
            Value::Null => unimplemented!(),
            Value::Bool(_) => unimplemented!(),
            Value::Number(n) => total += n.as_i64().unwrap() as i64,
            Value::String(_) => {},
            Value::Array(v) => queue.append(&mut v.iter().collect()),
            Value::Object(m) => {
                if !m.values().any(|v| v == "red") {
                    queue.append(&mut m.values().collect())
                }
            },
        }
    };
    total
}

fn parse(text: String) -> Input {
    serde_json::from_str(text.as_str()).unwrap()
}

fn main() {
    let input = parse(get_input(12, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

