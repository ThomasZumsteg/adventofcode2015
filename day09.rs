use common::get_input;
use regex::Regex;
use std::cmp::Reverse;
use std::collections::{HashMap, HashSet, BinaryHeap};

type Input = HashMap<String, HashMap<String, usize>>;

#[derive(Debug)]
struct Node<'a> {
    distance: usize,
    visited: Vec<&'a String>,
}

impl <'a> PartialOrd for Node<'a> {
    fn partial_cmp(&self, other: &Node) -> Option<std::cmp::Ordering> { Some(self.cmp(&other)) }
}


impl <'a> PartialEq for Node<'a> {
    fn eq(&self, other: &Node) -> bool { self.distance == other.distance }
}

impl <'a> Eq for Node<'a> {}

impl <'a> Ord for Node<'a> {
    fn cmp(&self, other: &Node) -> std::cmp::Ordering { self.distance.cmp(&other.distance) }
}

fn part1(map: &Input) -> usize {
    let destnations = map.keys().collect::<HashSet<&String>>();
    let mut queue: BinaryHeap<Reverse<Node>> = destnations.iter().map(|d| {
        Reverse(Node { distance: 0, visited: vec![d] })
    }).collect();
    while let Some(Reverse(node)) = queue.pop() {
        if destnations.iter().all(|d| node.visited.contains(d)) {
            return node.distance;
        }
        let current = node.visited.last().unwrap();
        for (dest, dist) in map[*current].iter().filter(|(d, _)| !node.visited.contains(d)) {
            let mut visited = node.visited.clone();
            visited.push(dest);
            queue.push(Reverse(Node {
                distance: node.distance + dist,
                visited,
            }));
        }
    }
    unimplemented!()
}

fn part2(map: &Input) -> usize {
    let destnations = map.keys().collect::<HashSet<&String>>();
    let mut result = BinaryHeap::new();
    let mut queue: Vec<Node> = destnations.iter().map(|d| {
        Node { distance: 0, visited: vec![d] }
    }).collect();
    while let Some(node)  = queue.pop() {
        if destnations.iter().all(|d| node.visited.contains(d)) {
            result.push(node);
            continue
        }
        let current = node.visited.last().unwrap();
        for (dest, dist) in map[*current].iter().filter(|(d, _)| !node.visited.contains(d)) {
            let mut visited = node.visited.clone();
            visited.push(dest);
            queue.push(Node {
                distance: node.distance + dist,
                visited,
            });
        }
    }
    result.pop().unwrap().distance
}

fn parse(text: String) -> Input {
    let mut result = HashMap::new();
    let re = Regex::new(r"(\w+) to (\w+) = (\d+)").unwrap();
    for line in text.trim().split("\n") {
        let captures = re.captures(line).unwrap();
        let from = captures.get(1).unwrap().as_str().to_string();
        let to = captures.get(2).unwrap().as_str().to_string();
        let distance = captures.get(3).unwrap().as_str().parse::<usize>().unwrap();
        result.entry(from.clone()).or_insert(HashMap::new()).insert(to.clone(), distance);
        result.entry(to.clone()).or_insert(HashMap::new()).insert(from.clone(), distance);
    }
    result
}

fn main() {
    let input = parse(get_input(09, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
