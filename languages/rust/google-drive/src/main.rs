use google_drive3::{api::Scope, hyper_rustls, hyper_util, yup_oauth2, DriveHub};

use std::{env, fs};

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    assert!(
        args.len() == 2,
        "Please provide a path to a service account key .json file."
    );
    let key = yup_oauth2::read_service_account_key(&args[1])
        .await
        .unwrap();
    let auth = yup_oauth2::ServiceAccountAuthenticator::builder(key)
        .build()
        .await
        .unwrap();
    let client = hyper_util::client::legacy::Client::builder(hyper_util::rt::TokioExecutor::new())
        .build(
            hyper_rustls::HttpsConnectorBuilder::new()
                .with_native_roots()
                .unwrap()
                .https_or_http()
                .enable_http1()
                .build(),
        );
    let hub = DriveHub::new(client, auth);
    println!("\nABOUT");
    match hub.about().get().param("fields", "*").doit().await {
        Ok((_rsp, about)) => {
            println!(
                "storage quota limit: {:?}",
                about.storage_quota.map(|q| q.limit)
            );
            println!("user email: {:?}", about.user.map(|u| u.email_address));
        }
        Err(e) => println!("{:?}", e),
    }
    println!("\nFILES");
    let mut downloaded = false;
    match hub.files().list().add_scope(Scope::Readonly).doit().await {
        Ok((_rsp, list)) => {
            if let Some(files) = list.files {
                for file in files {
                    println!(
                        "id: {:?}\n\tname: {:?}\n\ttype: {:?}",
                        file.id, file.name, file.mime_type
                    );
                    if !downloaded
                        && file.id.is_some()
                        && file.name.is_some()
                        && match file.mime_type {
                            Some(mime_type) => mime_type != "application/vnd.google-apps.folder",
                            None => false,
                        }
                    {
                        println!("\tdownloading");
                        match hub
                            .files()
                            .get(&file.id.unwrap())
                            .add_scope(Scope::Readonly)
                            .param("alt", "media")
                            .acknowledge_abuse(true)
                            .doit()
                            .await
                        {
                            Ok((rsp, _file)) => {
                                use http_body_util::BodyExt;
                                let body = match rsp.into_body().collect().await {
                                    Ok(collected) => collected.to_bytes(),
                                    Err(e) => {
                                        println!("{:?}", e);
                                        continue;
                                    }
                                };
                                fs::write(file.name.unwrap(), body).unwrap();
                                downloaded = true;
                            }
                            Err(e) => println!("{:?}", e),
                        }
                    }
                }
            }
        }
        Err(e) => println!("{:?}", e),
    }
}
