use common::get_input;

type Input = Vec<Present>;

struct Present {
    edges: Vec<usize>,
}

impl Present {
    fn from_string(text: &str) -> Present {
        Present { edges: text.split("x").map(|n| n.parse::<usize>().unwrap()).collect() }
    }

    fn ribbon(&self) -> usize {
        let mut edges = self.edges.clone();
        edges.sort();
        2 * (edges[0] + edges[1])  + edges[0]*edges[1]*edges[2]
    }

    fn paper(&self) -> usize {
        let edges =  &self.edges;
        let sides = [edges[0]*edges[1], edges[1]*edges[2], edges[0]*edges[2]];
        2*(sides.iter().sum::<usize>()) + sides.iter().min().unwrap()
        
    }
}

fn part1(packages: &Input) -> usize {
    packages.iter().map(|p| p.paper()).sum()
}

fn part2(packages: &Input) -> usize {
    packages.iter().map(|p| p.ribbon()).sum()
}

fn parse(text: String) -> Vec<Present> {
    text.trim().split("\n").map(|p| Present::from_string(p)).collect()
}

fn main() {
    let input = parse(get_input(02, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
