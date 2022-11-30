use common::get_input;
use std::collections::{HashMap, HashSet};

type Input = HashMap<String, HashMap<String, isize>>;

struct Combinations {
    indexes: Vec<usize>,
}

impl Combinations {
    fn new(size: usize, max: usize) -> Combinations {
        let mut indexes = vec![0; size];
        indexes[0] = max;
        Combinations { indexes }
    }
}


/*
 *  ...
 *  0, 100,   0,   0
 * 99,   0,   1,   0
 * ...
 *  0,  99,   1,   0
 * 98,   0,   2,   0
 * ...
 *  0,    0, 100,   0
 * 99,    0,   0,   1
 */
impl Iterator for Combinations {
    type Item = Vec<usize>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.indexes.iter().all(|&n| n == 0) { return None }
        let value = self.indexes.clone();
        for i in 0..(self.indexes.len()-2) {
            if self.indexes[i] > 0 {
                self.indexes[i] -= 1;
                self.indexes[i+1] += 1;
                return Some(value);
            } else if self.indexes[i+1] != 0 {
                self.indexes[0] = self.indexes[i+1] - 1;
                self.indexes[i+1] = 0;
                self.indexes[i+2] += 1;
                return Some(value);
            }
        }
        *self.indexes.last_mut().unwrap() = 0;
        Some(value)
    }
}


fn abs(counts: &Vec<usize>, values: &Vec<isize>) -> usize {
    let total: isize = counts.iter().zip(values.iter()).map(|(&c, &v)| (c as isize) * v).sum();
    if total >= 0 { total as usize } else { 0 }
}

fn part1(ingredients: &Input) -> usize {
    let properties = ingredients.values().map(|v| v.keys()).flatten().collect::<HashSet<&String>>();
    Combinations::new(4, 100).into_iter().map(|counts| {
        properties.iter().filter(|&p| p.as_str() != "calories").map(|&p| {
            abs(&counts, &ingredients.values().map(|r| r[p]).collect())
        }).fold(1, |acc, n| acc * n)
    }).max().unwrap()
}

fn part2(ingredients: &Input) -> usize {
    let properties = ingredients.values().map(|v| v.keys()).flatten().collect::<HashSet<&String>>();
    Combinations::new(4, 100).into_iter().filter(|counts| {
        abs(&counts, &ingredients.values().map(|r| r["calories"]).collect()) == 500
    }).map(|counts| {
        properties.iter().filter(|&p| p.as_str() != "calories").map(|&p| {
            abs(&counts, &ingredients.values().map(|r| r[p]).collect())
        }).fold(1, |acc, n| acc * n)
    }).max().unwrap()
}

fn parse(text: String) -> Input {
    text.trim().split("\n").map(|line| {
        let mut iter = line.splitn(2, ": ");
        let name: String = iter.next().unwrap().to_string();
        let groups: HashMap<String, isize> = iter.next().unwrap().split(", ").map(|prop| {
            let mut prop_iter = prop.splitn(2, " ");
            let name = prop_iter.next().unwrap().to_string();
            let value = prop_iter.next().unwrap().parse::<isize>().unwrap();
            (name, value)
        }).collect();
        (name, groups)
    }).collect::<Input>()
}

fn main() {
    let input = parse(get_input(15, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
