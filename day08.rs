use common::get_input;

type Input = Vec<String>;

fn decode(text: &String) -> Vec<String> {
    let mut chars = text.chars();
    let mut result: Vec<String> = Vec::new();
    while let Some(next) = chars.next() {
        match next {
            '"' => {},
            '\\' => {
                let follow = chars.next().unwrap();
                if follow == 'x' {
                    let hex = format!("{}{}", chars.next().unwrap(), chars.next().unwrap());
                    result.push(char::from_u32(u32::from_str_radix(&hex, 16).unwrap()).unwrap().to_string());
                } else {
                    assert!(vec!['"', '\\'].contains(&follow));
                    result.push(follow.to_string());
                }
            }
            c => result.push(c.to_string()),
        }
    }
    result
}

fn encode(text: &String) -> Vec<char> {
    let mut result: Vec<char> = text.chars().map(|c| {
        if vec!['"', '\\'].contains(&c) { vec!['\\', c] }
        else { vec![c] }
    }).flatten().collect();
    result.push('"');
    result.insert(0, '"');
    result
}

fn part1(strings: &Input) -> usize {
    strings.iter().map(|s| s.chars().count() - decode(&s).len()).sum()
}

fn part2(strings: &Input) -> usize {
    strings.iter().map(|s| encode(&s).len() - s.chars().count()).sum()
}

fn parse(text: String) -> Input {
    text.trim().split("\n").map(|l| l.to_string()).collect()
}

fn main() {
    let input = parse(get_input(08, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
