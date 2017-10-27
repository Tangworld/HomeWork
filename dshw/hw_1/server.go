package main
import (
	"fmt"
	"net"
	"os"
	"strings"
	"time"
	"crypto/md5"
	"encoding/hex"
	"strconv"
)

func main() {
	//建立socket，监听端口
	cip := getCurrentIp()
	netListen, err := net.Listen("tcp", cip+":8086")
	//netListen, err := net.Listen("tcp", "127.0.0.1:8086")
	CheckError(err)
	defer netListen.Close()

	for {
		conn, err := netListen.Accept()
		if err != nil {
			continue
		}
		go handleConnection(conn)
	}

}

//处理连接
func handleConnection(conn net.Conn) {
	buffer := make([]byte, 4096)
	for {
		n, err := conn.Read(buffer)
		if err != nil {
			continue
		}
		token := string(buffer[:n])
		//fmt.Printf(token)
		tokens := strings.Split(string(token), " ")
		//fmt.Printf(string(len(tokens)))
		//fmt.Printf(string(tokens[0]))
		//fmt.Printf(string(tokens[1]))
		number := tokens[0]
		password := tokens[1]
		tool := md5.New()
		tool.Write([]byte(number))
		rPassword := hex.EncodeToString(tool.Sum(nil))
		if !strings.EqualFold(password,rPassword){
			fmt.Printf("illegal client!")
			continue
		}
		conn.Write([]byte("ok"))
		nn,err := conn.Read(buffer)
		if err != nil {
			continue
		}
		commend := string(buffer[:nn])
		fmt.Printf(commend)
		t := time.Now().UnixNano()
		strt := strconv.FormatInt(t,10)
		//fmt.Println(strt)
		//fmt.Printf(string(buffer[:n]))
		conn.Write([]byte(strt))

	}
}

func CheckError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}
}
//获取服务器在当前局域网下的ip地址
func getCurrentIp() string{
	conn, err := net.Dial("udp", "baidu.com:80")
	if err != nil {
		return err.Error()
	}
	defer conn.Close()
	return strings.Split(conn.LocalAddr().String(), ":")[0]
}