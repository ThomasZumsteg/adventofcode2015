use common::get_input;
use std::collections::HashMap;
use regex::Regex;

type Point = (usize, usize);

#[derive(Debug)]
enum Action {
    TurnOff,
    TurnOn,
    Toggle,
}

#[derive(Debug)]
struct Instruction {
    action: Action,
    from: Point,
    to: Point,
}

impl Instruction {
    fn from_string(text: String) -> Instruction {
        let re = Regex::new(r"^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)").unwrap();
        let captures = re.captures(&text).unwrap();

        let get_int = |n: usize| -> usize {
            captures.get(n).map(|c| c.as_str().parse::<usize>().unwrap()).unwrap()
        };

        let action = match captures.get(1).unwrap().as_str() {
            "toggle" => Action::Toggle,
            "turn on" => Action::TurnOn,
            "turn off" => Action::TurnOff,
            _ => unimplemented!(),
        };

        Instruction {
            action,
            from: (get_int(2), get_int(3)),
            to: (get_int(4), get_int(5)),
        }
    }
}

type Input = Vec<Instruction>;

fn part1(instructions: &Input) -> usize {
    let mut grid: HashMap<Point, bool> = HashMap::new();
    for instruction in instructions {
        for row in instruction.from.0..(instruction.to.0+1) {
            for col in instruction.from.1..(instruction.to.1+1) {
                let point = (row, col);
                match instruction.action {
                    Action::TurnOn => { grid.insert(point, true); }
                    Action::TurnOff => { grid.insert(point, false); },
                    Action::Toggle => { grid.entry((row, col)).and_modify(|v| *v = !*v).or_insert(!false); },
                };
            }
        }
    };
    grid.values().filter(|&&v| v).count()
}

fn part2(instructions: &Input) -> usize {
    let mut grid: HashMap<Point, usize> = HashMap::new();
    for instruction in instructions {
        for row in instruction.from.0..(instruction.to.0+1) {
            for col in instruction.from.1..(instruction.to.1+1) {
                let point = (row, col);
                match instruction.action {
                    Action::TurnOn => *grid.entry(point).or_insert(0) += 1,
                    Action::TurnOff => if let Some(v) = grid.get_mut(&point) { if *v > 0 { *v -= 1 }},
                    Action::Toggle => *grid.entry(point).or_insert(0) += 2,
                };
            }
        }
    };
    grid.values().sum()
}

fn parse(text: String) -> Input {
    text.trim().split("\n").map(|i| Instruction::from_string(i.to_string())).collect()
}

fn main() {
    let input = parse(get_input(06, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
