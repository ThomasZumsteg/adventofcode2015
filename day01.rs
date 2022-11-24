use common::get_input;

type Input = Vec<isize>;

fn part1(brackets: &Input) -> isize {
    brackets.iter().sum()
}

fn part2(brackets: &Input) -> isize {
    let mut total: isize = 0;
    for (b, bracket) in brackets.iter().enumerate() {
        total += bracket;
        if total < 0 {
            return 1 + b as isize;
        }
    }
    unimplemented!()
}

fn parse(text: String) -> Input {
    text.trim().chars().map(|c| match c {
        ')' => -1,
        '(' => 1,
        _ => unimplemented!()
    }).collect()
}

fn main() {
    let input = parse(get_input(01, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
