# Crawl data, search and list database
- Sử dụng Python, VScode để viết, kiểm tra bằng Postman

## Crawl dữ liệu
1. Crawl dữ liệu từ nguồn [malwarebazaar](https://bazaar.abuse.ch/browse/)
- Lấy danh sách các file đọc hại có đuôi exe, zip, ace, 7z, elf, js, rar được người dùng gửi lên 
- post dữ liệu thu được lên mongodb, định dạng
```
{
    "timestamp": 012345678,
    "type": "asdf",
    "data": [],
}
```
- truy cập {POST} http://127.0.0.1:5505/api/v1 để crawl data từ malwarebazaar và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- body:
```
{
    "source":"bazaar"
}
```
- tiêu chí
* [x] Thu thập 10 file mỗi loại của danh sách đuôi trên
* [x] Data thu thập không bị duplicate

2. crawl dữ liệu từ nguồn [otx alientvault](https://otx.alienvault.com/dashboard/new)
- lấy danh sách các bài viết có tên chứa 1 trong số các từ (IOCs, malware, IP addresses, Domains, URLs, File hashes, Email addresses)
- sử dụng otx api để lấy data cần thiết , sau đó đấy lên db, định dạng như p1
- truy cập {POST} http://127.0.0.1:5505/api/v1 để crawl data từ otx và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- body:
```
{
    "source":"otx"
}
```
- tiêu chí
* [x] Thu thập 10 pulses mỗi loại chứa các từ trên
* [x] Data thu thập không bị duplicate

3. crawl dữ liệu từ [virustotal](https://www.virustotal.com/gui/home/search)
- tìm files thông tin bằng cách sử dụng file id đã mã hóa sha256 của chúng, các file id này được lấy từ mongodb, được crawl về từ malwarebazaar
- truy cập {POST} http://127.0.0.1:5505/vt_api/v1 để crawl data từ virustotal và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- body:
```
{
    "source":"virustotal"
}
```
- lưu tất cả những thông tin của file lấy được về mongodb
- định dạng
```
{
    "timestamp": 012345678,
    "data": [],
}
```
- tiêu chí
* [x] Thu thập tất cả data với mỗi file id lấy ra từ db được crawl về từ bazaar
* [x] Data thu thập không bị duplicate

4. crawl dữ liệu từ [virusshare](https://virusshare.com/apiv2_reference)
- crawl các tên md5 của [trang](https://virusshare.com/hashes), sau đó lưu vào db
- tìm thông tin các files bằng cách sử dụng file id đã mã hóa md5 của chúng, các file id này được lấy từ mongodb, được crawl về từ virusshare
- lưu tất cả những thông tin của file lấy được về mongodb
- truy cập {POST} http://127.0.0.1:5505/api/v1 để crawl data từ virusshare và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- body:
```
{
    "source":"virusshare"
}
```
- định dạng
```
{
    "timestamp": 012345678,
    "data": [],
}
```
- truy cập {POST} http://127.0.0.1:5505/vs_api/v2 để crawl tên md5 từ virusshare và gửi lên db, body gồm 1 json
```
{
    "id":"xxx", #xxx = 000,001,...463
}
```
- tiêu chí
* [x] Thu thập tất cả data với mỗi file id lấy ra từ db được crawl về từ bazaar
* [x] Data thu thập không bị duplicate

## Search and list database
1. Search all data from database
- truy cập {GET} http://127.0.0.1:5505/all_data 
- body:
```
{
    "source":"virustotal"  # can be replaced with bazaar, otx, virusshare
}
```
- kết quả trả về là 1 json chứa tất cả thông tin được crawl từ malwarebazaar, otx, virustotal, virusshare

2. Search data by type from db
- tìm kiếm theo type , có thể dùng : {POST} http://127.0.0.1:5505/query_by_type
- trong phần body gồm json:
```
{
    "source":"bazaar" # can be replace by ....
    "type":"SHA256"  # type of data query
}
```
- response:
```
 {
        "timestamp": 1679304728,
        "type": "SHA256",
        "data": [
            "0d668847ca2c3d1f086781a07ddab94dfb5129a4ec18db97123daa2aa18cf460",
            "2b7dd6b0cf1fdb9808219bcf5c9fc2ddeddf08da4ae1dc4c9b75cb90062d34e1",
            "4fc37b100e8dbdea27042487dd94e37cf6a79f2182884231eb1e6e6c2d4a1955",
            "1ef14f23c1c3fad652b81376340e8882a942b27052f85e96040067fc0ac4cd5a",
            "f7f2e73a832d09d4ccda0e3d584eb40af695ed21726be42850f9ad0f4a4ed7dd",
            "29f24efe9e0ff0f013a992cabb6dd15dd0923a5541807d1e4fc541c6e1b02592",
            "0fc7d652b6fdeb252920589cd09eee181301822f0456bc62d8f298a6bdf6f8ce",
            "73df28ac2f3e843630a538f99947c5f1cafdc2ec77a22e76063ce35d4f9f606c",
            "7b19720913425839002145fec9db388330e2b6dd411a8673a277b3ef5c6b42a8",
            "36c4218d8c975157b562afb8853e44ce1fb52f75eafa5849a23b7dfd4a7c0acb",
            "ff98b8da0fc33f048d672f8c46fe2a7103215a5c96087bf705602d0984bf6608",
            ....
        ]
 }
```
- source: otx , type: md5

- response:
```
{
        "timestamp": 1679296124,
        "type": "MD5",
        "data": [
            "edb660ef32e2fd59ad1e610e9842c2df",
            "779d4c1ce9fb2befb775a9f7f245a83f",
            "9afecfaa484c66f2dd11f2d7e9dc4816",
            "2ad4dcabfb78497ab92f74aec6fac5c6",
            "379c67ae879872d3fa0b601892c59605",
            "6eb761ea46a40ad72018d3cee915c4cd",
            "3f11c42687d09d4a56c715f671143a58",
            "f21072077e88c74b9b6d67f81ae63d84",
            "520cd9ee4395ee85ccbe073a00649602",
            "966953034b7d7501906d8b4cd3f90f6b",
            "cc68fcc0a4fab798763632f9515b3f92",
            "48fb0166c5e2248b665f480deac9f5e1",
            "10e16e36fe459f6f2899a8cea1303f06",
            "c7c647a14cb1b8bc141b089775130834",
            .....
        ]
}
```

- source: virustotal , type: rar

- response:
``` 
{
        "timestamp": 1679455311,
        "data": {
            "attributes": {
                "type_description": "RAR",
                "tlsh": "T17C2533F4F4A0C6ABD071BB6BDB16CF8728836B33ED5812646F93DA45D324F54422D822",
                "trid": [
                    {
                        "file_type": "RAR compressed archive (v5.0)",
                        "probability": 61.5
                    },
                    {
                        "file_type": "RAR compressed archive (gen)",
                        "probability": 38.4
                    }
                ],
                "names": [
                    "662acbf7478f5415e9675d9c74e26aa4e90d839e43a8fc73de624a8a10d39e8b.7z",
                    "MT103_Halkbank_pdf.7z",
                    "MT103 Halkbank,pdf.7z"
                ],
                "last_modification_date": 1679081559,
                "type_tag": "rar",
                "times_submitted": 8,
                "total_votes": {
                    "harmless": 0,
                    "malicious": 0
                },
                ....
            }
        }
}
```
- source: virusshare , type: s

- response
```
{
    "timestamp": 1679555702,
    "data": {
        "md5": "cc2b0d297470b90ca4b98c72aecaa1ea",
        "ssdeep": "3072:p/61om6ZyKwQXHjUaBoDDJVQHSPM9TIhH+xV4EHNxlv1pFS:p/MoqvQX4aCDDJY0qHxlv1pF",
        "asha256": "93c35b8cec24f2a0f72c76bdaf1d62f6db7a6b1a85b4b2b91d5c662d93e9dd05",
        "sha224": "df617ea93920b9f52f8763b4299ba7462a7a86c36bd0c2c2c9cb1956",
        "virustotal":object
        "sha1":"f35e0207ba1ed70c6df7c0d411a0195d29d95dd4"
        "filetype":"HTML document, UTF-8 Unicode text, with very long lines"
        "sha512":"807bf896604700bf6cbaff2e843801d7ff2393835a875cf628502834df955118cef6cf…"
        "trid":object
        "sha384":"46e62266112a4ab4c3fa3246394397b8cc3aab1758fba6e83854f45d4b23b044fa446b…"
        "extension":"s"
        "mimetype:""text/html"
        "sha256":"82b35889742bf14604a27a83613540d795a11894f18cc82652cb40c963aa458d"
        "size":374190
        "exif":Object
        "response":1
    }
}
```