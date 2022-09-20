package main

import (
	"log"
	"github.com/Danny-Dasilva/CycleTLS/cycletls"
)

func main() {

	client := cycletls.Init()
    cookies := []cycletls.Cookie{
        {
            Name:  "Hm_lvt_337e99a01a907a08d00bed4a1a52e35d",
            Value: "1663047488",
        },
        {
            Name:  "sessionid",
            Value: "7ob42ha5l0tcdooceclp7olimcgii254",
        },
        {
            Name:  "Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d",
            Value: "1663139345",
        },
        {
            Name:  "__yr_token__",
            Value: "b301cDCJbc1B0QC59XmcpaQM4eWptdG5kBUEoUzhnV1VoGTUGT1cSTShddFdzTCEeSGgnB0I6M2xKW2kIAgt3AGZzaB8bG0NSXyh2EjsIUk08cCgjHgZWKlIUWAZYF3ZrXAZPABUMG3kJWQNBYRY=",
        },
    }
	response, err := client.Do("https://www.python-spider.com/api/challenge22", cycletls.Options{
		Body : "page=1",
		Ja3: "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
		UserAgent: "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
		Cookies: cookies,
	  }, "POST");
	if err != nil {
		log.Print("Request Failed: " + err.Error())
	}
	log.Println(response)
}