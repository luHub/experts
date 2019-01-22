package main

import (
	"bufio"
	"encoding/xml"
	"fmt"
	"os"
	"strconv"
)

// type MonthFreq struct {
// 	count int
// 	date  string
// }

// type Trending struct {
// 	monthFreq []MonthFreq
// }

// Post from stackoverflow
type Posts struct {
	XMLName xml.Name `xml:"posts"`
	Rows    []Row    `xml:"row"`
}

// the user struct, this contains our
// Type attribute, our user's name and
// a social struct which will contain all
// our social links
type Row struct {
	XMLName               xml.Name `xml:"row"`
	Id                    string   `xml:"Id,attr"`
	PostTypeId            string   `xml:"PostTypeId,attr"`
	AcceptedAnswerId      string   `xml:"AcceptedAnswerId,attr"`
	ParentId              string   `xml:"ParentId,attr"`
	CreationDate          string   `xml:"CreationDate,attr"`
	Score                 string   `xml:"Score,attr"`
	ViewCount             string   `xml:"ViewCount,attr"`
	Body                  string   `xml:"Body,attr"`
	OwnerUserId           string   `xml:"OwnerUserId,attr"`
	LastEditorUserId      string   `xml:"LastEditorUserId,attr"`
	LastEditorDisplayName string   `xml:"LastEditorDisplayName,attr"`
	LastEditDate          string   `xml:"LastEditDate,attr"`
	LastActivityDate      string   `xml:"LastActivityDate,attr"`
	Title                 string   `xml:"Title,attr"`
	Tags                  string   `xml:"Tags,attr"`
	AnswerCount           string   `xml:"AnswerCount,attr"`
	CommentCount          string   `xml:"CommentCount,attr"`
	FavoriteCount         string   `xml:"FavoriteCount,attr"`
}

func createTrendings(path string, trendingPath string) {
	// Open our xmlFile
	xmlFile, err := os.Open(path)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened from HD test.xml")
	defer xmlFile.Close()

	decoder := xml.NewDecoder(xmlFile)

	var questionByMonth map[string]int
	questionByMonth = make(map[string]int)
	for {
		// Read tokens from the XML document in a stream.
		t, _ := decoder.Token()
		if t == nil {
			break
		}
		// Inspect the type of the token just read.
		switch se := t.(type) {
		case xml.StartElement:
			if se.Name.Local == "row" {
				var row Row
				decoder.DecodeElement(&row, &se)
				if err != nil {
					panic(err)
				}

				var date = row.CreationDate
				runes := []rune(date)
				safeSubstring := string(runes[0:7])
				if val, ok := questionByMonth[safeSubstring]; ok {
					//do something here
					val = val + 1
					questionByMonth[safeSubstring] = val
				} else {
					questionByMonth[safeSubstring] = 1
				}
			}
		}
	}
	//CreationDate "2013-03-07T17:07:31.280"

	file, errWf := os.Create(trendingPath)
	if errWf != nil {
		panic(errWf)
	}
	defer file.Close()
	w := bufio.NewWriter(file)
	w.WriteString("<trending>\n")
	for key, value := range questionByMonth {
		w.WriteString("<point date=\"" + string(key) + "\">" + strconv.Itoa(value) + "</point>\n")
		//	fmt.Println("Key:", key, "Value:", value)
	}
	w.WriteString("</trending>\n")
	w.Flush()

}

func main() {

	var questionsPath = "Add questions path"
	var questionsPathTrending = "Add question output path"
	createTrendings(questionsPath, questionsPathTrending)

	var answersPath = "Add answers path"
	var answersPathTrending = "Add answers path"
	createTrendings(answersPath, answersPathTrending)

}
