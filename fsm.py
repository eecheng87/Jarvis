from transitions.extensions import GraphMachine
from transitions import Machine
from utils import*
from ptt import*
from util_wea import*
from util_train import*
ptt_img_index = 0
ptt_post_index = 0
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_active(self, event):
        text = event.message.text
        # send_text_message(event.reply_token, "state1")
        return text.lower() == "jarvis"
    def on_enter_active(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,"Good morning sir, may I help you?")
    def is_going_to_show_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"
    def on_enter_show_fsm(self,event):
        reply_token = event.reply_token
        send_image_message(reply_token, "https://i.imgur.com/MGDr537.png")
        self.go_back()
    def is_going_to_ptt(self, event):
        text = event.message.text
        # send_text_message(event.reply_token, "state2")
        return text.lower() == "ptt"

    def on_enter_ptt(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Which board you want to enter?")

    #def on_exit_ptt(self):
     #   print("Leaving state2")
    def is_going_to_baseball(self, event):
        text = event.message.text
        return text.lower() == "baseball"

    def on_enter_baseball(self, event):
        reply_token = event.reply_token
        #rec_url = link(2)
        send_text_message(reply_token, get_recommend_title('https://www.ptt.cc/bbs/baseball/search',80))
        # self.go_back()
    def is_going_to_bchoose(self,event):
        text = event.message.text
        return text.isdigit()
    def on_enter_bchoose(self,event):
        reply_token = event.reply_token
        rank = int(event.message.text)
        if rank < 20:
            send_text_message(reply_token,get_recommend_link('https://www.ptt.cc/bbs/baseball/search',rank))
        else:
            send_text_message(reply_token,"request index is out of bound\n")
        print(rank)
        self.go_back()
    def on_exit_bchhose(self):
        print('leave bchoose')
    #def on_exit_baseball(self):
     #   print("Leaving state2")
    def is_going_to_weather(self,event):
        text = event.message.text
        return text.lower() == "weather"
#
    def on_enter_weather(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "What place's temperature do you want to know?")
        self.go_back()
    def is_going_to_degree(self,event):
        text = event.message.text
        return text.lower() != ""#re.match(r".*", text)
        #return text.lower() == "degree"
    def on_enter_degree(self,event):
        # later add `invalid location dectection` feature
        text = event.message.text
        #print(ID_MAP[text.lower()],AUTH_KEY)
        json_data = get_data_from_cwb(DATA_ID, AUTH_KEY, {})
        temp = parse_json_to_dataframe(json_data,ID_MAP[text.lower()])
        reply_token = event.reply_token
        send_text_message(reply_token, 'Current temperature is ' + temp + u'\N{DEGREE SIGN}' + 'C')
        self.go_back()
    def on_exit_degree(self):
        print('leave degree')
    def is_going_to_train(self,event):
        text = event.message.text
        return text.lower() == "train"
    def on_enter_train(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Please tell me your ride in following format!\n {departure} {arrival} {0~23}")

    def is_going_to_train_result(self,event):
        text = event.message.text
        return text.lower() != ""
    def on_enter_train_result(self,event):
        req = event.message.text
        word = req.split()
        if len(word) > 3:
            print('Incorrect format')
        else:
            payload['startStation'] = train_map[word[0].lower()]
            payload['endStation'] = train_map[word[1].lower()]
            if len(word) == 2:
                # need table start from now
                payload['startTime'] = current_time()
                payload['rideDate'] = current_date()
            else:
                payload['startTime'] = str(word[2])+':00'
                payload['rideDate'] = current_date()
            print(payload)
            res = requests.post("https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime",data=payload)
            out = ''
            num = 0
            parse = parse_entries(res.text)
            metadata = [parse_meta(entry) for entry in parse]
            for a in metadata:
                num = num+1
                out = out + '> ' + a['type'] + '\ndeparture time is ' + \
                a['departure'] + '\narrival time is ' + a['arrival'] + \
                '\n'
            reply_token = event.reply_token
            send_text_message(reply_token, 'You can take following '+str(num)+\
                ' ride\n'+out)
        self.go_back()
    def on_exit_train_result(self):
        print('leave train result')

    def is_going_to_beauty(self,event):
        text = event.message.text
        return text.lower() == "beauty"
    def on_enter_beauty(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Please tell me what mode do you want to enter")

    def is_going_to_popular(self,event):
        text = event.message.text
        return text.lower() == "popular" or text.lower() == "next"
    def on_enter_popular(self,event):
        global ptt_post_index
        global ptt_img_index
        #ptt_post_index = 0
        #ptt_img_index = 0
        url = get_beauty_url('https://www.ptt.cc/bbs/Beauty/search',50,ptt_post_index,ptt_img_index)
        l = url.split('/')
        link = 'https://i.imgur.com/' + l[-1] + '.png'
        print(link)
        reply_token = event.reply_token
        send_image_message(reply_token, link)
        #self.go_back()
    def is_going_to_next(self,event):
        text = event.message.text
        return text.lower() == "next"
    def on_enter_next(self,event):
        global ptt_img_index
        ptt_img_index += 1
        self.advance(event)
    def is_going_to_np(self,event):
        text = event.message.text
        return text.lower() == "np"
    def on_enter_np(self,event):
        global ptt_post_index
        global ptt_img_index
        ptt_post_index += 1
        ptt_img_index = 0
        self.advance(event)
    #def on_exit_next(self):
     #   print('leave next\n')











if __name__ == '__main__':
    machine = Machine(
    states=['solid', 'liquid', 'gas', 'plasma'],

# The trigger argument defines the name of the new triggering method
    transitions = [
    {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid' },
    {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
    {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
    {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}],
    initial="solid",
    #auto_transitions=False,
    #show_conditions=True,
    )

    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    send_file("fsm.png", mimetype="image/png")







