use common::get_input;
use std::collections::HashMap;

type Input = HashMap<String, (String, Vec<String>)>;

fn fill_values<'a, 'b: 'a>(wires: &'b Input, values: &mut HashMap<&'a str, usize>) -> Result<(), String> {
    let mut keys: Vec<&String> = wires.keys().filter(|k| !values.contains_key(k.as_str())).collect();

    let get_int = |k: &str, v: &HashMap<&str, usize>| -> Option<usize> {
        if let Ok(int) = k.parse::<usize>() { Some(int) }
        else { v.get(k).map(|i: &usize | i.to_owned()) }
    };

    while !keys.is_empty() {
        let key = keys.remove(0);
        let (op, args): &(String, Vec<String>) = wires.get(key).unwrap();
        let vals: Vec<Option<usize>> = args.iter().map(|a| get_int(a, &values)).collect();
        if vals.iter().any(|v| v.is_none()) {
            keys.push(key);
        } else {
            values.insert(
                key,
                match op.as_str() {
                    "" => vals[0].unwrap(),
                    "NOT" => !vals[0].unwrap(),
                    "AND" => vals[0].unwrap() & vals[1].unwrap(),
                    "OR" => vals[0].unwrap() | vals[1].unwrap(),
                    "LSHIFT" => vals[0].unwrap() << vals[1].unwrap(),
                    "RSHIFT" => vals[0].unwrap() >> vals[1].unwrap(),
                    _ => unimplemented!(),
                }
            );
        }
    }
    Ok(())
}

fn part1(wires: &Input) -> usize {
    let mut values = HashMap::<&str, usize>::new();
    assert!(fill_values(wires, &mut values).is_ok());
    values["a"]
}

fn part2(wires: &Input) -> usize {
    let mut values = HashMap::<&str, usize>::new();
    assert!(fill_values(wires, &mut values).is_ok());
    let a: usize = *values.get("a").unwrap();
    values.clear();
    values.insert("b", a);
    assert!(fill_values(wires, &mut values).is_ok());
    values["a"]
}

fn parse(text: String) -> Input {
    text.trim().split("\n").map(|line| {
        let mut fields = line.split(" ");
        let ops: Vec<&str> = fields.by_ref().take_while(|&f| f != "->").collect();
        let name = fields.next().unwrap().to_string();
        (
            name,
            match ops[..] {
                [a] => ("".to_string(), vec![a.to_string()]),
                ["NOT", a] => ("NOT".to_string(), vec![a.to_string()]),
                [a, op, b] => (op.to_string(), vec![a.to_string(), b.to_string()]),
                _ => unimplemented!()
            }
        )
    }).collect()
}

fn main() {
    let input = parse(get_input(07, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
