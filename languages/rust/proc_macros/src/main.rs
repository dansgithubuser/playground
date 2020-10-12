component::component!(
    {"in": ["midi"], "out": ["audio"]},
    ["uni", "run_size", "sample_rate"],
    {
        phase: f32,
    },
);

fn main() {
    println!("Hello, world!");
}
