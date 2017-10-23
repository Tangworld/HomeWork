package main

import (
	"fmt"
	"net"
	//"os"
	//"bufio"
	"math/rand"
	"crypto/md5"
	"encoding/hex"
	"strings"
	"os"
)

func sender(conn net.Conn) {
	//r := bufio.NewReader(os.Stdin) /*使用bufio缓冲器*/
	buffer := make([]byte, 2048)
	//for{
		//获取一个口令
		req := authority()
		//rawLine, _, _ := r.ReadLine()
		//line := string(rawLine)
		//发送口令
		conn.Write([]byte(req))
		ack, err := conn.Read(buffer)
		ackString := string(ack)
		if err != nil{
			fmt.Printf("failed!")
			return
		}
		if strings.EqualFold(ackString, "ok"){
			conn.Write([]byte("GET"))
			currentTime, err := conn.Read(buffer)
			if err != nil{
				fmt.Printf("failed!")
				return
			}
			fmt.Println("cunrrent time:")
			fmt.Println(currentTime)
		}





		//fmt.Printf(string(buffer[:n])+"\n")
	//}
}

func main() {
	tcpAddr, err := net.ResolveTCPAddr("tcp4", "172.28.40.3:8086")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}

	fmt.Println("connect success")
	sender(conn)
}

func authority() string{
	rawInt := rand.Intn(100)
	password := md5.New()
	password.Write([]byte(string(rawInt)))
	result := hex.EncodeToString(password.Sum(nil))
	fmt.Printf("%s\n", result) // 输出加密结果
	return string(rawInt)+" "+result
}