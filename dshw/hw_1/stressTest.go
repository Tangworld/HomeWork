package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"time"
	"crypto/md5"
	"encoding/hex"
	"math/rand"
	"strconv"
)

func stressSender(conn net.Conn) {
	for {
		buffer := make([]byte, 2048)
		//获取一个口令
		req := stressAuthority()
		//fmt.Printf(req)
		//发送口令
		conn.Write([]byte(req))
		//获取服务器端返回的同意信息，若返回ok则正常进行后续逻辑，否则连接中断
		n, err := conn.Read(buffer)
		ackString := string(buffer[:n])
		if err != nil {
			fmt.Printf("failed111!")
			continue
		}
		if strings.EqualFold(ackString, "ok") {
			//发送获取时间请求
			conn.Write([]byte("GET"))
			//计时，记录从发出请求到获得时间的时间差
			start := time.Now().UnixNano()
			//fmt.Println(start)
			cn, err := conn.Read(buffer)
			//从服务器获得的时间戳
			currentTime := string(buffer[:cn])
			intTime, err := strconv.ParseInt(currentTime, 10, 64)
			end := time.Now().UnixNano()
			//fmt.Println(end)
			//粗略计算得到的时延值
			delay := (end - start) / 2
			//fmt.Println(delay)

			//校正后的时间值
			rTime := intTime + delay
			if err != nil {
				fmt.Println(err)
				fmt.Printf("failed222!")
				continue
			}
			result := time.Unix(0, rTime).Format("2006-01-02 15:04:05")
			fmt.Println("cunrrent time:")
			fmt.Println(result)
		} else {
			fmt.Printf("connect denied!\n")
			continue
		}
	}
}

func main() {
	tcpAddr, err := net.ResolveTCPAddr("tcp4", "172.28.42.162:8086")
	if err != nil {
		fmt.Printf(err.Error())
		os.Exit(1)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		fmt.Printf(err.Error())
		os.Exit(1)
	}

	fmt.Println("ready to get time!")
	stressSender(conn)
}

//产生一个随机数，然后使用md5算法对这个随机数进行加密，将随机数和加密值传送给
//服务器进行验证，若通过验证则认为是可信任客户端，可提供后续服务
func stressAuthority() string{
	rawInt := rand.Intn(100)
	//fmt.Printf("raw_int:::"+string(rawInt)+"\n")
	password := md5.New()
	password.Write([]byte(string(rawInt)))
	result := hex.EncodeToString(password.Sum(nil))
	//fmt.Printf("%s\n", result) // 输出加密结果
	return string(rawInt)+" "+result
}