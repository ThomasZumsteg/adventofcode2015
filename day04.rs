use common::get_input;
use md5;

type Input = String;

fn part1(key: &Input) -> usize {
    for n in 0.. {
        let result = format!("{:x}", md5::compute(format!("{}{}", key, n)));
        if (&result[..5]).chars().all(|d| d == '0') {
            return n;
        }
    }
    unimplemented!()
}

fn part2(key: &Input) -> usize {
    for n in 0.. {
        let result = format!("{:x}", md5::compute(format!("{}{}", key, n)));
        if (&result[..6]).chars().all(|d| d == '0') {
            return n;
        }
    }
    unimplemented!()
}

fn parse(text: String) -> Input {
    text.trim().to_string()
}

fn main() {
    let input = parse(get_input(04, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
