use common::get_input;
use regex::Regex;

type Input = Vec<Reindeer>;

#[derive(Clone, Debug)]
enum State {
    RESTING(usize),
    FLYING(usize),
}

#[derive(Clone, Debug)]
struct Reindeer {
    #[allow(dead_code)]
    name: String,  // All reindeer have a name, even if they never come when called
    speed: usize,
    flying_time: usize,
    rest_time: usize,
    position: usize,
    state: State,
    score: usize,
}

impl Reindeer {
    fn from_str(text: &str) -> Result<Reindeer, String> {
        let reigndeer_regex = Regex::new(r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.").unwrap();
        let captures = reigndeer_regex.captures(text).ok_or("Reigndeer regex doesn't match")?;
        let flying_time = captures.get(3).ok_or("No Speed Time")?.as_str().parse::<usize>().unwrap();
        Ok(Reindeer {
            name: captures.get(1).ok_or("No Name")?.as_str().to_string(),
            speed: captures.get(2).ok_or("No Speed")?.as_str().parse::<usize>().unwrap(),
            flying_time,
            rest_time: captures.get(4).ok_or("No Rest time")?.as_str().parse::<usize>().unwrap(),
            position: 0,
            state: State::FLYING(flying_time-1),
            score: 0,
        })
    }

    fn update(&mut self, time: usize) {
        match self.state {
            State::FLYING(t) => {
                self.position += self.speed;
                if t <= time { self.state = State::RESTING(self.rest_time + time) };
            },
            State::RESTING(t) if t <= time => self.state = State::FLYING(self.flying_time + time),
            _ => {}
        }
    }
}

fn part1(input: &Input) -> usize {
    let mut reindeers = input.clone();
    for time in 0..2503 {
        for reindeer in reindeers.iter_mut() {
            reindeer.update(time);
        }
    }
    reindeers.iter().map(|r| r.position).max().unwrap()
}

fn part2(input: &Input) -> usize {
    let mut reindeers = input.clone();
    for time in 0..2503 {
        for reindeer in reindeers.iter_mut() {
            reindeer.update(time);
        }
        let mut fast_reindeers = reindeers.iter_mut().fold(Vec::<&mut Reindeer>::new(), |mut acc, r| {
            if let Some(max) = acc.first() {
                if max.position >= r.position {
                    if max.position < r.position { acc.clear(); }
                    acc.push(r)
                }
            } else {
                acc.push(r)
            }
            acc
        });
        for fast_reindeer in fast_reindeers.iter_mut() {
            fast_reindeer.score += 1;
        }
    }
    reindeers.iter().map(|r| r.score).max().unwrap()
}

fn parse(text: String) -> Input {
    text.trim().split("\n").map(|line| Reindeer::from_str(line).unwrap()).collect()
}

fn main() {
    let input = parse(get_input(14, 2015));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
