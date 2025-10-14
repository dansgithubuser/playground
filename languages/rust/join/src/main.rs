fn main() {
    let x = vec![1, 2, 3];
    let x: Vec<String> = x.iter().map(i32::to_string).collect();
    let x = x.join(", ");
    println!("{}", x);
}
