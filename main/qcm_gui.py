# FINAL FORM OF MY PROTOTYPE
import sqlite3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button 
from kivy.uix.checkbox import CheckBox  
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file('qcm_gui.kv')


# Establish a connection to the SQLite database
conn = sqlite3.connect("qcmsqlite.db")
cursor = conn.cursor()

topic_id = None
input_text = None

class WelcomeScreen(Screen):

    pass


class QuizScreen(Screen):
    pass


class ExamApp(App):
    def build(self):
        self.sm = ScreenManager()


        self.sm.add_widget(WelcomeScreen(name='welcome'))
        self.sm.add_widget(QuizScreen(name='QCM'))

        return self.sm
    

    def StartPsy(self):
        quiz_screen = self.sm.get_screen('QCM')
        welcome_screen = self.sm.get_screen('welcome')
        self.sm.current = 'QCM'
        topic = self.Quiz(1,1)
        quiz_screen.ids.my_question.text = topic
        self.GetOptions(self.QuestionID(topic))
        welcome_screen.ids.welcome.text = '1'



    def StartSyn(self):
        quiz_screen = self.sm.get_screen('QCM')
        welcome_screen = self.sm.get_screen('welcome')
        self.sm.current = 'QCM'
        topic = self.Quiz(2,1)
        quiz_screen.ids.my_question.text = topic
        self.GetOptions(self.QuestionID(topic))
        welcome_screen.ids.welcome.text = '2'

    def StartRea(self):
        quiz_screen = self.sm.get_screen('QCM')
        welcome_screen = self.sm.get_screen('welcome')
        self.sm.current = 'QCM'
        topic = self.Quiz(3,1)
        quiz_screen.ids.my_question.text = topic
        self.GetOptions(self.QuestionID(topic))
        welcome_screen.ids.welcome.text = '3'

        
    
    def getTopic(self, text):
        cursor.execute('''
                        SELECT topic_id FROM topics
                        WHERE topic_name = ?
                        ''',(text,))
        global topic_id
        topic_id = cursor.fetchone()
        return topic_id
    
    def getTopicID(self, topic):
        cursor.execute('''
                SELECT topic_id
                FROM topics
                WHERE topic_name =  ?
                ''',(topic,))
        topic_id = cursor.fetchone()
    
    def reset(self):

        welcome_screen = self.sm.get_screen('welcome')
        topic = welcome_screen.ids.welcome.text

        quiz_screen = self.sm.get_screen('QCM')
        quiz_screen.ids.my_question.text = self.Quiz(topic, 1)
        
        
        quiz_screen.ids.op1.text = ""
        quiz_screen.ids.op1.color = 1, 1, 1, 1 
        quiz_screen.ids.optionA.active = False
       # quiz_screen.ids.check1.text = ""
        
        quiz_screen.ids.op2.text = ""
        quiz_screen.ids.op2.color = 1, 1, 1, 1 
        quiz_screen.ids.optionB.active = False
       # quiz_screen.ids.check2.text = ""
        
        quiz_screen.ids.op3.text = ""
        quiz_screen.ids.op3.color = 1, 1, 1, 1 
        quiz_screen.ids.optionC.active = False
       # quiz_screen.ids.check3.text = ""
        
        quiz_screen.ids.op4.text = ""
        quiz_screen.ids.op4.color = 1, 1, 1, 1 
        quiz_screen.ids.optionD.active = False
       # quiz_screen.ids.check4.text = ""
        
        quiz_screen.ids.op5.text = ""
        quiz_screen.ids.op5.color = 1, 1, 1, 1 
        quiz_screen.ids.optionE.active = False
       # quiz_screen.ids.check5.text = ""
        
        self.GetOptions(self.QuestionID(quiz_screen.ids.my_question.text))

    def Quiz(self, topic_id, num):
        cursor.execute("""
            SELECT q.question_text
            FROM questions q
            WHERE q.topic_id = ? 
            ORDER BY RANDOM()
            LIMIT ?
        """, (topic_id, num))
        random_question = cursor.fetchall()
        for questions in random_question:
            for question in questions:
                My_question = question
        return My_question
    
    def QuestionID(self, question_text):
        cursor.execute("""
                SELECT question_id
                FROM questions
                WHERE question_text = ?
                """,(question_text,))
        question = cursor.fetchone()
        for quest_id in question:
            question_id = quest_id
        return question_id
    
    def GetOptions(self, question_id):
        cursor.execute("""
                SELECT option_text
                FROM options
                WHERE question_id = ?
                    """,(question_id,))
        options = cursor.fetchall()
        option_gui = []
        for option_tuple in options:
            for option in option_tuple:
                option_gui.append(option)

        quiz_screen = self.sm.get_screen('QCM')

        quiz_screen.ids.op1.text = option_gui[0]
        quiz_screen.ids.op2.text = option_gui[1]
        quiz_screen.ids.op3.text = option_gui[2]
        quiz_screen.ids.op4.text = option_gui[3]
        quiz_screen.ids.op5.text = option_gui[4]

        return option_gui
    
    def GetOptionsAnswers(self, question_id):
        cursor.execute("""
                SELECT is_correct
                FROM options
                WHERE question_id = ?
                    """,(question_id,))
        options = cursor.fetchall()
        option_correctness = []
        for option_tuple in options:
            for option in option_tuple:
                option_correctness.append(option)
        return option_correctness
    
    def CheckAnswers(self, options):

        quiz_screen = self.sm.get_screen('QCM')

        print(options)
        
        optionA_Box = quiz_screen.ids.optionA
       # optionA_Label = quiz_screen.ids.check1
        optionB_Box = quiz_screen.ids.optionB
       # optionB_Label = quiz_screen.ids.check2
        optionC_Box = quiz_screen.ids.optionC
       # optionC_Label = quiz_screen.ids.check3
        optionD_Box = quiz_screen.ids.optionD
       # optionD_Label = quiz_screen.ids.check4
        optionE_Box = quiz_screen.ids.optionE
       # optionE_Label = quiz_screen.ids.check5


        if optionA_Box.active and options[0] == 1:
        #    optionA_Label.text = 'CORRECT'
            quiz_screen.ids.op1.color = (0, 1, 0, 1)
        elif optionA_Box.active and options[0] == 0:
        #    optionA_Label.text = 'WRONG'
            quiz_screen.ids.op1.color = (1, 0, 0, 1)
        elif options[0] == 1:
        #    optionA_Label.text = 'WRONG'
            quiz_screen.ids.op1.color = (0, 1, 0, 1)
        elif options[0] == 0:
        #    optionA_Label.text = 'CORRECT'
            quiz_screen.ids.op1.color = (1, 0, 0, 1)

        if optionB_Box.active and options[1] == 1:
        #    optionB_Label.text = 'CORRECT'
            quiz_screen.ids.op2.color = (0, 1, 0, 1)
        elif optionB_Box.active and options[1] == 0:
        #    optionB_Label.text = 'WRONG'
            quiz_screen.ids.op2.color = (1, 0, 0, 1)
        elif options[1] == 1:
        #    optionB_Label.text = 'WRONG'
            quiz_screen.ids.op2.color = (0, 1, 0, 1)
        elif options[1] == 0:
        #    optionB_Label.text = 'CORRECT'
            quiz_screen.ids.op2.color = (1, 0, 0, 1)

        if optionC_Box.active and options[2] == 1:
        #    optionC_Label.text = 'CORRECT'
            quiz_screen.ids.op3.color = (0, 1, 0, 1)
        elif optionC_Box.active and options[2] == 0:
        #    optionC_Label.text = 'WRONG'
            quiz_screen.ids.op3.color = (1, 0, 0, 1)
        elif options[2] == 1:
        #    optionC_Label.text = 'WRONG'
            quiz_screen.ids.op3.color = (0, 1, 0, 1)
        elif options[2] == 0:
        #    optionC_Label.text = 'CORRECT'
            quiz_screen.ids.op3.color = (1, 0, 0, 1)

        if optionD_Box.active and options[3] == 1:
        #    optionD_Label.text = 'CORRECT'
            quiz_screen.ids.op4.color = (0, 1, 0, 1)
        elif optionD_Box.active and options[3] == 0:
        #    optionD_Label.text = 'WRONG'
            quiz_screen.ids.op4.color = (1, 0, 0, 1)
        elif options[3] == 1:
        #    optionD_Label.text = 'WRONG'
            quiz_screen.ids.op4.color = (0, 1, 0, 1)
        elif options[3] == 0:
        #    optionD_Label.text = 'CORRECT'
            quiz_screen.ids.op4.color = (1, 0, 0, 1)

        if optionE_Box.active and options[4] == 1:
        #    optionE_Label.text = 'CORRECT'
            quiz_screen.ids.op5.color = (0, 1, 0, 1)
        elif optionE_Box.active and options[4] == 0:
        #    optionE_Label.text = 'WRONG'
            quiz_screen.ids.op5.color = (1, 0, 0, 1)
        elif options[4] == 1:
        #    optionE_Label.text = 'WRONG'
            quiz_screen.ids.op5.color = (0, 1, 0, 1)
        elif options[4] == 0:
        #    optionE_Label.text = 'CORRECT'
            quiz_screen.ids.op5.color = (1, 0, 0, 1)
            

            
        



            



if __name__ == '__main__':
    ExamApp().run()
