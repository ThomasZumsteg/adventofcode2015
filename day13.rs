use common::get_input;
use std::collections::HashMap;
use regex::Regex;

type Input = HashMap<String, HashMap<String, isize>>;

struct Permutations<T> {
    items: Vec<T>,
    indexes: Vec<usize>,
}

impl <T> Permutations<T> {
    fn new(items: Vec<T>) -> Permutations<T> {
        let size = items.len() - 1;
        let indexes = vec![0; size];
        Permutations { indexes, items }
    }
}

impl <T: Clone + Copy> Iterator for Permutations <T> {
    type Item = Vec<T>;

    fn next(&mut self) -> Option<Self::Item> {
        /*
         * Implementation of iterative (non-recusive) [heap's algorithm](https://en.wikipedia.org/wiki/Heap%27s_algorithm) 
         * Skips the least significant person to simulate a ring buffer (i.e. A -> B -> C -> A)
         * Thus the least significant person doesn't need to change for all seating arrangments to
         * be explored.
         */
        if self.indexes.iter().all(|&i| i == 0) {
            self.indexes[0] = 1;
            return Some(self.items.clone());
        }
        let mut i = 1;
        let size = self.indexes.len();
        let mut swap = |i: usize, j: usize| { (self.items[i], self.items[j]) = (self.items[j], self.items[i]); };
        while i < size {
            if self.indexes[i] < i {
                if i % 2 == 0 { swap(0, i) }
                else { swap(self.indexes[i], i) }
                self.indexes[i] += 1;
                return Some(self.items.clone());
            } else {
                self.indexes[i] = 0;
                i += 1;
            }
        }
        None
    }
}

fn part1(persons_map: &Input) -> isize { 
    let persons: Vec<&String> = persons_map.keys().collect();
    Permutations::new(persons).into_iter().map(|people| {
        let mut partners = people.clone();
        partners.rotate_right(1);
        people.iter().zip(partners.iter()).map(|(&person, &partner)| {
            persons_map[person][partner] + persons_map[partner][person]
        }).sum::<isize>() 
    }).max().unwrap()
}

fn part2(persons_map: &Input) -> isize { 
    let mut persons: Vec<Option<&String>> = persons_map.keys().map(|k| Some(k)).collect();
    persons.push(None);
    Permutations::new(persons).into_iter().map(|people| {
        let mut partners = people.clone();
        partners.rotate_right(1);
        people.iter().zip(partners.iter()).map(|(&person, &partner)| {
            if let (Some(p), Some(q)) = (person, partner) { persons_map[p][q] + persons_map[q][p] }
            else { 0 }
        }).sum::<isize>() 
    }).max().unwrap()
}

fn parse(text: String) -> Input {
    let re = Regex::new(r"^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).$").unwrap();
    let mut persons = HashMap::<String, HashMap::<String, isize>>::new();
    for line in text.trim().split("\n") {
        let captures = re.captures(line).unwrap();
        let to = captures.get(1).unwrap().as_str().to_string();
        let from = captures.get(4).unwrap().as_str().to_string();
        let mut score = captures.get(3).unwrap().as_str().parse::<isize>().unwrap();
        score *= if captures.get(2).unwrap().as_str() == "gain" { 1 } else { -1 };
        persons.entry(from).or_insert(HashMap::new()).insert(to, score);
    }
    persons
}

fn main() {
    let input = parse(get_input(13, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
