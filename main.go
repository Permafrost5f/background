package main

import (
	"crypto/sha256"
	"encoding/hex"
	"github.com/joho/godotenv"
	"github.com/reujab/wallpaper"
	"io"
	"log"
	"math"
	"os"
	"strconv"
	"time"
)

var hasher = sha256.New()

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	hash := os.Getenv("CHECKSUM")
	t := os.Getenv("TIMER")

	i, err := strconv.Atoi(t)
	if err != nil {
		log.Fatalln(err.Error())
	}

	i = int(math.Min(float64(i), 3600))

	for {
		log.Println("Checked")
		get, err := wallpaper.Get()
		if err != nil {
			log.Fatal(err.Error())
		}

		if checksum(&get) != hash {
			err = wallpaper.SetFromURL("https://i.imgur.com/4rJR98e.png")
			if err != nil {
				log.Fatal(err.Error())
			}
		}

		time.Sleep(time.Duration(i) * time.Second)
	}
}

func checksum(wallpaper *string) string {
	f, err := os.Open(*wallpaper)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	if _, err := io.Copy(hasher, f); err != nil {
		log.Fatal(err)
	}
	return hex.EncodeToString(hasher.Sum(nil))
}
