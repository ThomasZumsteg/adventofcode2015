use common::get_input;
use std::cmp::max;

type Input = String;

struct Password {
    chars: Vec<u8>,
}

impl <'a> Iterator for Password {
    type Item = Password;
    
    fn next(&mut self) -> Option<Self::Item> {
        *self.chars.last_mut().unwrap() += 1;
        let mut carry: u8 = 0;
        let mut chars = Vec::new();
        for ch in self.chars.iter().rev() {
            chars.insert(0, (ch + carry) % 26); 
            carry = (ch + carry) / 26;
        };
        self.chars = chars.clone();
        if carry != 0 { None }
        else { Some(Password { chars })}
    }
}


impl Password {
    fn from_string(text: &String) -> Password {
        let chars = text.chars().map(|c| (c as u8) - ('a' as u8)).collect();
        Password { chars }
    }

    fn straight(&self) -> usize {
        let mut longest = 0;
        let mut current = 1;
        for (&prev, &next) in self.chars.iter().zip(self.chars.iter().skip(1)) {
            if (next as u8) == (prev as u8) + 1 {
                current += 1;
            } else {
                longest = max(longest, current);
                current = 1;
            }
        }
        longest
    }

    fn contains(&self, chars: &Vec<char>) -> bool {
        chars.iter()
            .map(|&c| c as u8 - ('a' as u8))
            .any(|ch| self.chars.iter().any(|&c| c == ch))
    }

    fn find_doubles(&self) -> Vec<Vec<char>> {
        let mut doubles: Vec<Vec<char>> = Vec::new();
        let mut chars: std::slice::Iter<u8> = self.chars.iter();
        let mut ch = if let Some(ch) = chars.next() { ch } else { return doubles };
        while let Some(mut next) = chars.next() {
            if ch == next {
                let double = (ch + 'a' as u8) as char;
                doubles.push(vec![double, double]);
                next = if let Some(ch) = chars.next() { ch } else { break };
            }
            ch = next;
        }
        doubles
    }
}

impl ToString for Password {
    fn to_string(&self) -> String {
        self.chars.iter().map(|&c| (c + ('a' as u8)) as char).collect()
    }
}

fn part1(input: &Input) -> String { 
    let password_iter = Password::from_string(input);
    for password in password_iter {
        if password.straight() >= 3 &&
            !password.contains(&vec!['i', 'o', 'l']) &&
            password.find_doubles().len() >= 2 {
            return password.to_string()
        }


    }
    unimplemented!()
}

fn part2(input: &Input) -> String { 
    let password_iter = Password::from_string(input);
    let mut first = true;
    for password in password_iter {
        if password.straight() >= 3 &&
            !password.contains(&vec!['i', 'o', 'l']) &&
            password.find_doubles().len() >= 2 {
            if !first { return password.to_string(); }
            first = false;
        }
    }
    unimplemented!()
}

fn parse(text: String) -> Input {
    text.trim().to_string()
}


fn main() {
    let input = parse(get_input(11, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
