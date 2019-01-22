package main

import (
	"bufio"
	"encoding/xml"
	"fmt"
	"os"
)

type Participants struct {
	users map[string]bool
}

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

func createTrendings(path string, activity map[string]Participants) {
	// Open our xmlFile
	xmlFile, err := os.Open(path)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened from HD test.xml")
	defer xmlFile.Close()

	decoder := xml.NewDecoder(xmlFile)

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
				rdate := []rune(date)
				sdate := string(rdate[0:4])

				var participant = row.OwnerUserId
				rparticipant := []rune(participant)
				sparticipant := string(rparticipant)

				if val, ok := activity[sdate]; ok {
					_, isKeyPresent := val.users[sparticipant]
					if !isKeyPresent {
						val.users[sparticipant] = true
					}
				} else {
					var par map[string]bool
					par = make(map[string]bool)
					par[sparticipant] = true
					us := Participants{users: par}
					activity[sdate] = us
				}
			}
		}
	}
}

func writeFile(path string, activity map[string]Participants) {
	file, errWf := os.Create(path)
	if errWf != nil {
		panic(errWf)
	}
	defer file.Close()
	w := bufio.NewWriter(file)
	w.WriteString("<activity>\n")
	for key, v1 := range activity {
		w.WriteString("<year date=\"" + string(key) + "\">\n")
		for key := range v1.users {
			w.WriteString("<participant>" + key + "</participant>\n")
		}
		w.WriteString("</year>\n")
	}
	w.WriteString("</activity>\n")
	w.Flush()
}

func extractParticipantsPerYear(answersPath string, savePath string) {
	//Users per year active:
	var participants map[string]Participants
	participants = make(map[string]Participants)
	createTrendings(answersPath, participants)
	writeFile(savePath, participants)

}

func main() {

	var answersPath = "Add answers path"
	var participantsTrendingPath = "Add output answers path"
	extractParticipantsPerYear(answersPath, participantsTrendingPath)
}
