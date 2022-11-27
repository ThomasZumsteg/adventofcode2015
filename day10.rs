use common::get_input;

type Input = Vec<char>;

fn round(chars: &Vec<char>) -> Vec<char> {
    let mut result: Vec<char> = Vec::new();
    let mut count = 0;
    for (d, next) in chars.iter().zip(chars.iter().skip(1).chain(vec!['\0'].iter())) {
        count += 1;
        if d != next {
            let mut count_chars = count.to_string().chars().collect();
            result.append(&mut count_chars);
            result.push(*d);
            count = 0;
        }
    }
    result
}

fn part1(text: &Input) -> usize {
    let mut chars = text.to_owned();
    for _ in 0..40 {
        chars = round(&chars); 
    }
    chars.len()
}

fn part2(text: &Input) -> usize {
    let mut chars = text.to_owned();
    for _ in 0..50 {
        chars = round(&chars); 
    }
    chars.len()
}

fn parse(text: String) -> Input {
    text.trim().to_string().chars().collect()
}


fn main() {
    let input = parse(get_input(10, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
