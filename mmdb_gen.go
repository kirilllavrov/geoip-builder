package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"

	"github.com/maxmind/mmdbwriter"
	"github.com/maxmind/mmdbwriter/mmdbtype"
)

func main() {
	if len(os.Args) < 4 {
		fmt.Fprintf(os.Stderr, "Usage: %s <input.txt> <output.mmdb> <country_code>\n", os.Args[0])
		os.Exit(1)
	}

	inputFile := os.Args[1]
	outputFile := os.Args[2]
	countryCode := strings.ToUpper(os.Args[3])

	writer, err := mmdbwriter.New(mmdbwriter.Options{
		DatabaseType:            "GeoIP2-Country",
		RecordSize:              28,
		IncludeReservedNetworks: true,
	})
	if err != nil {
		fmt.Fprintf(os.Stderr, "mmdbwriter.New: %v\n", err)
		os.Exit(1)
	}

	file, err := os.Open(inputFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "os.Open: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	count := 0
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") || strings.HasPrefix(line, "//") {
			continue
		}
		_, cidr, err := net.ParseCIDR(line)
		if err != nil {
			continue
		}
		data := mmdbtype.Map{
			"country": mmdbtype.Map{
				"iso_code": mmdbtype.String(countryCode),
			},
		}
		if err := writer.Insert(cidr, data); err != nil {
			continue
		}
		count++
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "scanner.Err: %v\n", err)
		os.Exit(1)
	}

	f, err := os.Create(outputFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "os.Create: %v\n", err)
		os.Exit(1)
	}
	defer f.Close()

	if _, err := writer.WriteTo(f); err != nil {
		fmt.Fprintf(os.Stderr, "writer.WriteTo: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Generated %s with %d entries\n", outputFile, count)
}
