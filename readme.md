# Crawl data, search and list database
- Sử dụng Python, VScode để viết, kiểm tra bằng Postman

## Crawl dữ liệu
- Crawl dữ liệu từ nguồn [malwarebazaar](https://bazaar.abuse.ch/browse/), [otx alientvault](https://otx.alienvault.com/dashboard/new), [virustotal](https://www.virustotal.com/gui/home/search), [virusshare](https://virusshare.com/apiv2_reference)
- truy cập {POST} http://127.0.0.1:5505/api/v1 để crawl data từ malwarebazaar và gửi lên db, sau khi hoàn thành thông báo (inserted successful!)
- Với nguồn malwarebazaar, lấy danh sách các file đọc hại có đuôi exe, zip, ace, 7z, elf, js, rar được người dùng gửi lên
- Với nguồn otx, lấy danh sách các bài viết có tên chứa 1 trong số các từ (IOCs, malware, IP addresses, Domains, URLs, File hashes, Email addresses)
- Với nguồn virustotal, tìm files thông tin bằng cách sử dụng file id đã mã hóa sha256 của chúng, các file id này được lấy từ mongodb, được crawl về từ malwarebazaar
- Với nguồn viusshare, crawl các tên md5 của [trang](https://virusshare.com/hashes),tìm thông tin các files bằng cách sử dụng file id đã mã hóa md5 của chúng, các file id này được lấy từ mongodb, được crawl về từ virusshare

- body:
```
{
    "source":"bazaar"  # co the thay bang otx, virustotal, virusshare voi cac du lieu tuong ung
}
```
- tiêu chí
* [x] Thu thập các files có định dạng theo yêu cầu
* [x] Data thu thập không bị duplicate

## Search and list database
1. Search all data from database
- truy cập {POST} http://127.0.0.1:5505/api/v2

- Nếu body gồm 1 cặp key-value("source":".."), trả về tất cả data của collection

- example:
+ body:
```
{
    "source":"virustotal"  # can be replaced with bazaar, otx, virusshare
}
```
+ response:
```
 {
    {   "timestamp": 1679304728,
        "type": "SHA256",
        "data": [
            "0d668847ca2c3d1f086781a07ddab94dfb5129a4ec18db97123daa2aa18cf460",
            "2b7dd6b0cf1fdb9808219bcf5c9fc2ddeddf08da4ae1dc4c9b75cb90062d34e1",
            "4fc37b100e8dbdea27042487dd94e37cf6a79f2182884231eb1e6e6c2d4a1955",
            "1ef14f23c1c3fad652b81376340e8882a942b27052f85e96040067fc0ac4cd5a",
            "f7f2e73a832d09d4ccda0e3d584eb40af695ed21726be42850f9ad0f4a4ed7dd",
            "29f24efe9e0ff0f013a992cabb6dd15dd0923a5541807d1e4fc541c6e1b02592",
            ....
        ]
    }
    { 
        "timestamp": 1679304728,
        "type": "SHA1",
        "data": [
            "f345177886eaa2835674c62f711b49fca5355d66",
            "2f0d69caaed1e5a77ff933780f33094295d7a113",
            "7dd8d3337f0ed24488b9d1912f4c2fbd90c27ab5",
            "8ef76ad1aaac59cc082a94dd1fa65338c7d59111",
            .......
        ]
    }
 }
```

- Nếu body chứa 2 cặp key-value("source":"..", "type":"..."), trả về tất cả data có type là ...

- example:
+ body:
```
{
    "source":"bazaar", # can be replace by otx, virustotal, virusshare
    "type":"SHA256"  # type of data query, can be sha1 or md5
}
```
+ response:
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

- Nếu body chứa 3 cặp key-value("source":"..", "type":"...","timestamp":...), trả về tất cả data có type là ..., với timestamp là ....

- example:
+ body:
```
{
    "source":"bazaar", # # can be replace by otx, virustotal, virusshare
    "type":"SHA256",  # type of data query, can be sha1 or md5
    "timestamp":1679469975  # timestamp that match data
}
```
+ response:
```
 {
        "timestamp": 1679469975,
        "type": "MD5",
        "data": [
            "361fae4aa3f862f912e2fc6642e36298",
            "a896f1696e17908b35191251050dcbf5",
            "99c144042b4cdea7181c4e082f7172c8",
            "75d45ac139ac9630ef44d1952e574633",
            "ab64460cd667c1964fc0ee034ec60d15",
            "ec7747b1553a2a538fcba76a35349ac0",
            "5072c7564e49e382eb887b70bbcc6a51",
            "ff6b172be4941c011db0b7d474ae3a28",
            "442116bf76b22c85d2c232e28f364ee7",
            "1af0a886d082f1b1917f76937973890d",
            "de4ca12df2e6fddf8e937a160f401e30",
            "0b02eb8c341484e612cb8b2872f51c0b",
            "dcfe7be66afb58806186046e432de88c",
            "569d86839920600f3e27d9060891b9f2",
            "a31bc094279bd65f568076d2aece6c99",
            "e0453eb56d974bb704e7f537dac5853c",
            "342c4798be16aedfa2a452d3b1b57a00",
            ....
        ]
 }
```
