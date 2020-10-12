use proc_macro::{TokenStream, TokenTree};

fn stream_to_vec(input: TokenStream) -> Vec<TokenTree> {
    input.into_iter().collect::<Vec<_>>()
}

fn inside(tt: &TokenTree) -> TokenStream {
    let group = match tt {
        TokenTree::Group(group) => group,
        _ => panic!("expected a group, found {}", tt),
    };
    group.stream()
}

fn get_literals(input: TokenStream) -> Vec<String> {
    let mut result: Vec<String> = Default::default();
    for tt in input {
        if let TokenTree::Literal(literal) = tt {
          result.push(literal.to_string().replace("\"", ""));  
        }
    }
    result
}

#[proc_macro]
pub fn component(input: TokenStream) -> TokenStream {
    let tts = stream_to_vec(input);
    let info = &tts[0];
    let features = get_literals(inside(&tts[2]));
    let fields = inside(&tts[4]);
    format!(
        r##"
            struct Component {{
                {fields}
            }}

            impl Component {{
                fn info() -> String {{
                    r#"{info}"#.into()
                }}
                
                /*
                {features:?}
                */
            }}
        "##,
        info = info,
        features = features,
        fields = fields,
    ).parse().unwrap()
}
