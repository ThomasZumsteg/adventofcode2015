use common::get_input;
use std::collections::HashSet;

type Point = (isize, isize);
type Input = Vec<Point>;

fn part1(directions: &Input) -> usize {
    let mut location = (0, 0);
    let mut locations = HashSet::new();
    for direction in directions {
        location = (location.0 + direction.0, location.1 + direction.1);
        locations.insert(location);
    }
    locations.len()
}

fn part2(directions: &Input) -> usize {
    let mut santas = vec![(0, 0), (0, 0)];
    let mut locations = HashSet::new();
    for (s, direction) in directions.iter().enumerate().map(|(s, d)| (s%2, d)) {
        santas[s] = (santas[s].0 + direction.0, santas[s].1 + direction.1);
        locations.insert(santas[s]);
    }
    locations.len()
}

fn parse(text: String) -> Input {
    text.trim().chars().map(|c| match c {
        '^' => (1, 0),
        '<' => (0, -1),
        '>' => (0, 1),
        'v' => (-1, 0),
        _ => unimplemented!(),
    }).collect()
}

fn main() {
    let input = parse(get_input(03, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
