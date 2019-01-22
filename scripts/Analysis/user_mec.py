
import csv
from functools import reduce
import xml.etree.ElementTree as ET  

#  Stackoverflow Posts Schema
#0 'Id', 
#1 'PostTypeId'
#2 'AcceptedAnswerId'
#3 'ParentId'
#4 'CreationDate'
#5 'DeletionDate'
#6 'Score'
#7 'ViewCount'
#8 'Body'
#9 'OwnerUserId'
#10 'OwnerDisplayName'
#11 'LastEditorUserId'
#12 'LastEditorDisplayName'
#13 'LastEditDate'
#14 'LastActivityDate'
#15 'Title'
#16 'Tags'
#17 'AnswerCount'
#18 'CommentCount'
#19 'FavoriteCount'
#20 'ClosedDate'
#21 'CommunityOwnedDate'
#22 'Id'
#23 'PostTypeId'
#24 'AcceptedAnswerId'
#25 'ParentId'
#26 'CreationDate'
#27 'DeletionDate'
#28 'Score'
#29 'ViewCount'
#30 'Body'
#31 'OwnerUserId'
#32 'OwnerDisplayName'
#33 'LastEditorUserId'
#34 'LastEditorDisplayName'
#35 'LastEditDate', 'LastActivityDate', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount', 'ClosedDate', 'CommunityOwnedDate']

class User:
    def __init__(self):
        self.id = ''
        self.questions_answered = 0
        self.questions = [] #answered_questions
    
    def __str__(self):
        q = list(map(lambda x:str(x),self.questions))
        q_for = ' '.join(str(x)+' ' for x in q) 
        return 'id: '+ self.id +' #q: '+str(self.questions_answered) +' u_questions: '+ q_for
 
class Question:  
    def __init__(self):
        self.id = ''
        self.answers = []
    def __str__(self):
        return 'id: ' + self.id +' #a:'+ str(len(self.answers))+' ac'+ str(self.answer_count())+ ' answers: ' + "".join(str(x) for x in self.answers)

    def debatablenes(self):
        return len(self.answers)

    def answer_count(self):
        return len(self.answers)

    def __sort_score__(self,e):
        return e.score 
    
    def utility(self,userId):
        self.answers.sort(key= self.__sort_score__, reverse=True)
        userAnswer = list(filter(lambda x: x.userId == userId ,self.answers))
        rank = self.answers.index(userAnswer[0])+1
        return 1.0/rank


class Answer:
    def __init__(self):
        self.parentId = ''
        self.userId = ''
        self.score = 0
    
    def __str__(self):
        return '[userId: '+ str(self.userId) +' score:'+ str(self.score)+']'


def pop_questions(onwer_user_id,parent_id,score, q_topic):
    if not parent_id in q_topic and len(onwer_user_id)>0 and len(parent_id)>0:
        a = Answer()
        a.parentId = parent_id
        a.userId = onwer_user_id
        a.score = score
        q = Question()
        q.id = parent_id
        q.answers.append(a)
        q_topic[parent_id] = q
    elif len(onwer_user_id)>0 and len(parent_id)>0:
        a = Answer()
        a.score = score
        a.parentId = parent_id
        a.userId = onwer_user_id
        q_topic[parent_id].answers.append(a)

    
def pop_questions_by_user(owner_id, question_id, u_answers):
    if not owner_id in u_answers and len(owner_id)>0:
        u = User()
        u.id = owner_id
        u.questions.append(question_id)
        u.questions_answered = 1
        u_answers[owner_id] = u
    elif len(owner_id)>0:
        u_answers[owner_id].questions_answered =  u_answers[owner_id].questions_answered + 1  
        u_answers[owner_id].questions.append(question_id)

def d_avg(q_topic):
    q_total = len(q_topic) 
    sum_answers = reduce(lambda acc,item : acc + float(item.answer_count()), q_topic.values(),0)
    return sum_answers/q_total

def is_noisy_question(question):
    if len(question.answers) == 1 and int(question.answers[0].score) == 0:
        return True
    return False

def is_not_social_question(question):
    ns = reduce(lambda acc,item: acc + int(item.score),question.answers,0)
    if ns < 1:
        return True
    return False

def is_debatible(key,noise):
    if key in noise:
        return False
    return True

def remove_noisy(user,noise):
    remain = list(filter(lambda id: is_debatible(id,noise),user.questions))
    user.questions = remain
    return user

def validate_count(answers):
    invalid = list(filter(lambda x: x.questions_answered != len(x.questions),answers.values()))
    if len(invalid) > 0:
         raise AssertionError("Error counting answers")

def extract_dataset(path_answers):
    questions = dict()
    user = dict()
    tree = ET.parse(path_answers)  
    root = tree.getroot()
    for item in root.iter('row'):
            pop_questions(item.attrib['OwnerUserId'],item.attrib['ParentId'],item.attrib['Score'],questions)
            pop_questions_by_user(item.attrib['OwnerUserId'],item.attrib['ParentId'],user)

    print("#Q",len(questions))
    print("#U",len(user))    
    return questions, user

def save_owls(experts,path):
    f = open(path, "a")
    f.write("<owls>\n")
    for key, value in experts.items():
        str_list = ["<owl id=\"",str(key),"\" ","mec=\"",str(value),"\"/>\n"]
        line = ''.join(str_list)
        f.write(line)
    f.write("</owls>")
    f.flush()

path_answers = 'Add path to Answers XML (with the same schema of stackoverflow)'
path_save = 'XML file with users and their respective MEC'


print("Working...")
q_topic = {}
u_answers = {}
q_topic , u_answers = extract_dataset(path_answers)
d_avg = d_avg(q_topic)

def utility_times_dqi(userId,questionId):
    return q_topic[questionId].debatablenes()*(q_topic[questionId].utility(userId)/d_avg)

user_mec = dict(
    map(
        lambda u:  (u[0],(1.0/u[1].questions_answered)* 
        reduce(lambda acc,questionId: acc+utility_times_dqi(u[1].id,questionId),u[1].questions,0)),u_answers.items()
    )
)


owls = dict(filter(lambda kv: kv[1]>=1,user_mec.items()))
save_owls(owls,path_save)

print("user mec", len(user_mec))
print("d_avg",d_avg)
print('topic questions', len(q_topic))
print('number of users', len(u_answers))
print('number of owls: ',len(owls))
print('ratio: ',len(owls)/len(u_answers)*100)
