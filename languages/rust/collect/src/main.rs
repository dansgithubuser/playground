use std::collections::HashMap;

fn main() {
    let m: HashMap::<i32, i32> = vec![(1, 1), (2, 2), (1, 2)].into_iter().collect();
    println!("{:?}", m);
}
