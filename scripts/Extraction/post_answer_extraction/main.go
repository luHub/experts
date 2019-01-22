package main

import (
	"bufio"
	"encoding/xml"
	"fmt"
	"os"
)

type Answer struct {
	writer *bufio.Writer
	ids    []string
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

	// Type    string   `xml:"type,attr"`
	// Name    string   `xml:"name"`
	// Social  Social   `xml:"social"`

}

func getQuestionsID(path string) []string {
	var Ids []string
	// Open our xmlFile
	xmlFile, err := os.Open(path)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("Successfully Opened from HD test.xml")
	// defer the closing of our xmlFile so that we can parse it later on
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
			// If we just read a StartElement token
			// ...and its name is "page"
			if se.Name.Local == "row" {
				var row Row
				decoder.DecodeElement(&row, &se)
				if err != nil {
					panic(err)
				}
				Ids = append(Ids, row.Id)
			}
		}
	}
	return Ids
}

func filterByParent(parentIDs []string, postType string, row Row) bool {
	for _, element := range parentIDs {
		if element == row.ParentId && postType == "2" {
			return true
		}
		// element is the element from someSlice for where we are
	}
	return false
}

func findAnswers(answers []Answer) {
	// Open our xmlFile
	xmlFile, err := os.Open("Add path to XML dump from stackoverflow")
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
			// If we just read a StartElement token
			// ...and its name is "page"
			if se.Name.Local == "row" {
				var row Row
				decoder.DecodeElement(&row, &se)
				out, err := xml.MarshalIndent(row, "", "   ")
				if err != nil {
					panic(err)
				}

				for _, answer := range answers {
					if filterByParent(answer.ids, "2", row) {
						answer.writer.WriteString(string(out))
						answer.writer.WriteByte('\n')
					}
				}

			}
		}
	}

}

func createAnswer(questionPath string, answerPath string) Answer {
	var ids = getQuestionsID(questionPath)
	file, errWf := os.Create(answerPath)
	if errWf != nil {
		panic(errWf)
	}
	writer := bufio.NewWriter(file)
	return Answer{writer, ids}
}

func main() {

	var emberQuestionsPath = "Add question output path 1"
	var angularQuestionsPath = "Add question output path 2"
	var reactQuestionsPath = "Add question output path 3"
	var vueQuestionsPath = "Add question output path 4"

	var emberPathAnswers = "Add answers path 1"
	var angularPathAnswers = "Add answers path 2"
	var reactPathAnswers = "Add answers path 3"
	var vuePathAnswers = "Add answers path 4"

	var answers []Answer

	var ember = createAnswer(emberQuestionsPath, emberPathAnswers)
	var angular = createAnswer(angularQuestionsPath, angularPathAnswers)
	var react = createAnswer(reactQuestionsPath, reactPathAnswers)
	var vue = createAnswer(vueQuestionsPath, vuePathAnswers)
	answers = append(answers, ember)
	answers = append(answers, angular)
	answers = append(answers, react)
	answers = append(answers, vue)

	for _, answer := range answers {
		answer.writer.WriteString("<posts>")
		answer.writer.WriteByte('\n')
	}

	findAnswers(answers)

	for _, answer := range answers {
		answer.writer.WriteString("</posts>")
		answer.writer.Flush()
	}
}
