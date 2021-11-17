use ring::signature::{EcdsaKeyPair, KeyPair, ECDSA_P256_SHA256_FIXED_SIGNING}; // generate
use ring::rand::SystemRandom; // sign
use ring::signature::{UnparsedPublicKey, ECDSA_P256_SHA256_FIXED}; // verify

use std::io::Write;

fn main() {
    if let Ok(sig) = std::fs::read("sig") {
        println!("verifying sig");
        let pub_key = std::fs::read("pub").unwrap();
        let pub_key = UnparsedPublicKey::new(&ECDSA_P256_SHA256_FIXED, pub_key);
        pub_key.verify(b"asdf", &sig).unwrap();
    } else {
        println!("generating key pair and signing");
        let pkcs8 = EcdsaKeyPair::generate_pkcs8(
            &ECDSA_P256_SHA256_FIXED_SIGNING,
            &ring::rand::SystemRandom::new(),
        )
        .unwrap();
        let pair =
            EcdsaKeyPair::from_pkcs8(&ECDSA_P256_SHA256_FIXED_SIGNING, pkcs8.as_ref()).unwrap();
        std::fs::File::create("pkcs8")
            .unwrap()
            .write(pkcs8.as_ref())
            .unwrap();
        std::fs::File::create("pub")
            .unwrap()
            .write(pair.public_key().as_ref())
            .unwrap();
        let sig = pair.sign(&SystemRandom::new(), b"asdf").unwrap();
        std::fs::File::create("sig")
            .unwrap()
            .write(sig.as_ref())
            .unwrap();
    }
    println!("success!");
}
