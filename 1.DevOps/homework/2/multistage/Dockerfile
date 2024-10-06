FROM golang:1.23 AS build
WORKDIR /src

COPY <<EOF /src/main.go
package main

import (
	"fmt"
	"os"
)

func main() {

  args := os.Args[1:]

  if len(args) < 2 {
		fmt.Println("Будь ласка, передайте 2 аргументи.")
		return
  }

  sumResult := args[0] + args[1]
  fmt.Println(sumResult)
}
EOF

RUN go build -o /bin/add ./main.go

FROM scratch
COPY --from=build /bin/add /bin/add

ENTRYPOINT ["/bin/add"]

CMD ["2", "3"]
