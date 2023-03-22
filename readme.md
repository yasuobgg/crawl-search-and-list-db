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
- truy cập {POST} http://127.0.0.1:5505/bazaar_api/v1 để crawl data từ malwarebazaar và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- tiêu chí
* [x] Thu thập 10 file mỗi loại của danh sách đuôi trên
* [x] Data thu thập không bị duplicate

2. crawl dữ liệu từ nguồn [otx alientvault](https://otx.alienvault.com/dashboard/new)
- lấy danh sách các bài viết có tên chứa 1 trong số các từ (IOCs, malware, IP addresses, Domains, URLs, File hashes, Email addresses)
- sử dụng otx api để lấy data cần thiết , sau đó đấy lên db, định dạng như p1
- truy cập {POST} http://127.0.0.1:5505/otx_api/v1 để crawl data từ otx và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- tiêu chí
* [x] Thu thập 10 pulses mỗi loại chứa các từ trên
* [x] Data thu thập không bị duplicate

3. crawl dữ liệu từ [virustotal](https://www.virustotal.com/gui/home/search)
- tìm files thông tin bằng cách sử dụng file id đã mã hóa sha256 của chúng, các file id này được lấy từ mongodb, được crawl về từ malwarebazaar
- lưu tất cả những thông tin của file lấy được về mongodb
- định dạng
```
{
    "timestamp": 012345678,
    "data": [],
}
```
- truy cập {POST} http://127.0.0.1:5505/vt_api/v1 để crawl data từ virustotal và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- tiêu chí
* [x] Thu thập tất cả data với mỗi file id lấy ra từ db được crawl về từ bazaar
* [x] Data thu thập không bị duplicate

## Search and list database
1. Search all data from database
- truy cập {GET} http://127.0.0.1:5505/bazaar_data , http://127.0.0.1:5505/otx_data, http://127.0.0.1:5505/vt_data
- kết quả trả về là 1 json chứa tất cả thông tin được crawl từ malwarebazaar, otx, virustotal

- tìm kiếm theo type , có thể dùng : {POST} http://127.0.0.1:5505/bazaar_data/type ,
{POST} http://127.0.0.1:5505/otx_data/type 
- trong phần body gồm json:
```
{
    "type":"SHA256"
}
```
- kết quả trả về là:
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
- với data từ virustotal, truy cập {POST} http://127.0.0.1:5505/vt_data/type
- body:
```
{
    "type":"RAR"
}
```
- response:
``` {
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