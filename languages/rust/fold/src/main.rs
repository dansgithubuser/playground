use std::collections::HashMap;

fn main() {
    let x = vec![(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)];
    let m: HashMap<i32, Vec<i32>> = x.into_iter().fold(HashMap::new(), |mut acc, (a, b)| {
        acc.entry(a).or_insert(Vec::new()).push(b);
        acc
    });
    println!("{:?}", m);
}
