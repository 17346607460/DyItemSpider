package main

import (
	"fmt"
// 	"strconv"
//     "regexp"
	"github.com/wangluozhe/requests"
	"github.com/wangluozhe/requests/url"
)


func main() {
//     num := 0
//     for i := 1; i < 101; i++ {
    req := url.NewRequest()
    headers := url.NewHeaders()
    data := url.NewData()
    data.Set("", "")
    data.Add("page", "2")
    headers.Add("accept", "application/json, text/javascript, */*; q=0.01")
    headers.Add("accept-language", "zh-CN,zh;q=0.9")
    headers.Add("cache-control", "no-cache")
//     headers.Add("content-length", "6")
    headers.Add("content-type", "application/x-www-form-urlencoded; charset=UTF-8")
    headers.Add("cookie", "Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1663047488; sessionid=7ob42ha5l0tcdooceclp7olimcgii254; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1663135409; __yr_token__=b301cDAFgYy8XVXQTO3ApTgQoUnADYxUrJ0F4SlgOPUteUFhDT1cSTShdKAkvTFkeUURaTg8lWnMoVDQFOkx2Hm1zaB8bG0MXMmFADFFhMlRscApsZRE4MHkEWAZYF3ZrXAZPABUMG3kJWQNBYRY=")
    headers.Add("origin", "https://www.python-spider.com")
    headers.Add("pragma", "no-cache")
    headers.Add("referer", "https://www.python-spider.com/challenge/22")
    headers.Add("sec-ch-ua-mobile", "?0")
    headers.Add("sec-ch-ua-platform", "Windows")
    headers.Add("sec-fetch-dest", "empty")
    headers.Add("sec-fetch-mode", "cors")
    headers.Add("sec-fetch-site", "same-origin")
    headers.Add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36")
//     headers.Add("x-requested-with", "XMLHttpRequest")
    req.Headers = headers
//     req.Ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0"
    req.Ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27,29-23-24,0"
    r, err := requests.Post("https://www.python-spider.com/api/challenge22", req)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Printf(r.Text)
//     reg := regexp.MustCompile(`[0-9]+`)
//     response := reg.FindAllString(r.Text, -1)
//         for i := 1; i < len(response); i++ {
//             n, err := strconv.Atoi(response[i])
//             if err!=nil {
//                 panic(err)
//             }
//             num = num + n
//             fmt.Println(num)
//         }
//     }
}


// {"ja3_hash":"b32309a26951912be7dba376398abc3b", "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}


//         listHaiCoder.PushFront(r.Text)
//         f,err := os.Create("./web" + strconv.Itoa(i) + ".txt")
//         defer f.Close()
//         if err !=nil {
//             fmt.Println(err.Error())
//         } else {
//             _,err=f.Write([]byte(listHaiCoder))
//         }