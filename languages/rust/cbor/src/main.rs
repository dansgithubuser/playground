fn main() {
    {
        let input = [
            0xc0, 0x74, 0x32, 0x30, 0x31, 0x33, 0x2d, 0x30,
            0x33, 0x2d, 0x32, 0x31, 0x54, 0x32, 0x30, 0x3a,
            0x30, 0x34, 0x3a, 0x30, 0x30, 0x5a,
            0xc0, 0x74, 0x32, 0x30, 0x31, 0x33, 0x2d, 0x30,
            0x33, 0x2d, 0x32, 0x31, 0x54, 0x32, 0x30, 0x3a,
            0x30, 0x34, 0x3a, 0x30, 0x30, 0x5a
        ];

        let mut decoder = minicbor::Decoder::new(&input);
        assert_eq!(minicbor::data::Tag::DateTime, decoder.tag().unwrap());
        assert_eq!("2013-03-21T20:04:00Z", decoder.str().unwrap());
        assert_eq!(minicbor::data::Tag::DateTime, decoder.tag().unwrap());
        assert_eq!("2013-03-21T20:04:00Z", decoder.str().unwrap());
    }
    {
        let msg = r#"{
            "gps": {
              "fix": 1,
              "lat": "43.6552815",
              "lon": "-79.39885518333332",
              "angle": "345.2",
              "speed": 33,
              "snrAvg": 27.75,
              "satellites": 8
            },
            "imu": {
              "samples": [
                [
                  -16,
                  -1525,
                  -3737,
                  60,
                  -152,
                  -35
                ],
                [
                  -43,
                  -1529,
                  -3839,
                  -15,
                  -153,
                  -43
                ],
                [
                  -18,
                  -1459,
                  -3811,
                  -53,
                  -135,
                  -44
                ],
                [
                  69,
                  -1496,
                  -3754,
                  -27,
                  -125,
                  -47
                ],
                [
                  -4,
                  -1525,
                  -3690,
                  21,
                  -159,
                  -31
                ],
                [
                  50,
                  -1548,
                  -3628,
                  89,
                  -163,
                  -20
                ],
                [
                  -29,
                  -1646,
                  -3608,
                  158,
                  -184,
                  -22
                ],
                [
                  -3,
                  -1707,
                  -3559,
                  176,
                  -182,
                  -29
                ],
                [
                  -47,
                  -1766,
                  -3586,
                  143,
                  -182,
                  -28
                ],
                [
                  16,
                  -1783,
                  -3596,
                  94,
                  -156,
                  -39
                ],
                [
                  -41,
                  -1753,
                  -3636,
                  35,
                  -159,
                  -35
                ],
                [
                  9,
                  -1771,
                  -3682,
                  0,
                  -147,
                  -35
                ],
                [
                  59,
                  -1706,
                  -3694,
                  -8,
                  -150,
                  -32
                ]
              ]
            },
            "sys": {
              "ina": {
                "avg": {
                  "cur0": 798,
                  "cur1": 222,
                  "cur2": 1636,
                  "pow0": 10847,
                  "pow1": 734,
                  "pow2": 8120,
                  "volt0": 13559,
                  "volt1": 3284,
                  "volt2": 4964
                },
                "max": {
                  "cur0": 872,
                  "cur1": 232,
                  "cur2": 1800,
                  "pow0": 11984,
                  "pow1": 762,
                  "pow2": 8848,
                  "volt0": 13648,
                  "volt1": 3288,
                  "volt2": 4968
                }
              },
              "pgk": {
                "voltage": 13173,
                "timeRunning": 2120925
              },
              "upTime": 8993,
              "carState": 2,
              "diskSpace": 9160003584,
              "tegraStats": {
                "a0Temp": 62000,
                "cpuTemp": 57500,
                "gpuTemp": 54500,
                "cpuUsage": [
                  1291852,
                  2,
                  1026060,
                  1108964,
                  13433,
                  110374,
                  24062,
                  0,
                  0,
                  0
                ],
                "gpuUsage": 579,
                "ramUsage": 3962848
              },
              "hawkUtcTime": 1670050496773,
              "sdCardSpace": 9165729792
            },
            "ccan": {
              "gas": "0",
              "brake": "2.0109",
              "speed": "29.650000000000002",
              "wheel": "-16.5",
              "seatbelt": {
                "driver": true
              },
              "turnSignal": 0
            },
            "snap": null,
            "j1979": {
              "speed": 29,
              "massAirflow": 1
            },
            "model": {
              "lane": {
                "avg": 0.5784196257591248,
                "max": 1.1275379657745361,
                "min": 0.18906868994235992
              },
              "dayNight": {
                "raw": 0.0123138427734375,
                "class": "night",
                "counter": -15
              },
              "closeness": {
                "avg": 0.9847756624221802,
                "max": 1.4707876443862915,
                "min": 0.29407745599746704
              },
              "clearUnclear": {
                "raw": 2.522181272506714,
                "class": "clear",
                "counter": 60
              }
            },
            "recId": "2022120306545100000487",
            "msgType": "V5_2",
            "deviceId": "nn-487",
            "incident": {},
            "recvTime": 1670050497918,
            "speedAnalyzer": {
              "kind": 1,
              "speed": "29.649999618530273"
            }
        }"#;
        let mut slice = [0u8; 100_000];
        {
            let mut serializer = serde_cbor::Serializer::new(serde_cbor::ser::SliceWrite::new(&mut slice));
            for _ in 0..2 {
                let mut deserializer = serde_json::Deserializer::from_str(msg);
                serde_transcode::transcode(&mut deserializer, &mut serializer).unwrap();
            }
        }
        //let cursor = std::io::Cursor::new(slice);
        //let v1: serde_cbor::Value = serde_cbor::from_reader(cursor).unwrap(); // panic! trailing data
    }
}
