#[derive(Debug)]
pub struct Error {
    msg: String,
}

impl Error {
    pub fn err<T>(msg: &str) -> Result<T, Box<dyn std::error::Error>> {
        Err(Box::new(Self { msg: msg.into() }))
    }

    pub fn boxed(msg: &str) -> Box<dyn std::error::Error> {
        Box::new(Self { msg: msg.into() })
    }
}

impl std::error::Error for Error {
    fn description(&self) -> &str {
        &self.msg
    }

    fn cause(&self) -> Option<&(dyn std::error::Error)> {
        None
    }
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.msg)
    }
}

fn parse_not_6_or_7(s: &str) -> Result<i32, Box<dyn std::error::Error>> {
    let i = s.parse::<i32>()?;
    if i == 6 {
        Err(Error::boxed("it's 6"))?;
    }
    if i == 7 {
        Error::err("it's 7")?;
    }
    Err(Error { msg: "asdf".into() })?;
    return Ok(i)
}

fn main() {
    println!("{:?}", parse_not_6_or_7("7"));
}
