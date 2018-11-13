from app.gp import Trie
from flask import Flask, jsonify, request, Response
import tkinter.filedialog
from app.stream import *
Suggested = []

trie = Trie()
trie.initialize("Dictionary.txt")

app = Flask(__name__)

class StreamHandler:
    def __init__(self):
        self.svm = pickle.load(open('svm.sav', 'rb'))
        self.SimulationSignal = "AutoSimTest(SC).txt"
        self.SignalLimit = 0
        self.Signals = []
        self.HSignal = []
        self.VSignal = []
        self.result = []

    def data_iterator(self):
        with open('MySimOutput.txt', 'r') as f:
            return list([i.strip() for i in f.readlines()])

    def create_stream(self):
        with open(self.SimulationSignal) as FileObj:  # Reading File
            signal = []
            for value in FileObj:
                self.SignalLimit += 1
                if self.SignalLimit == 251:
                    self.HSignal = list(signal)
                    signal = []
                elif self.SignalLimit == 502:
                    self.VSignal = list(signal)
                    self.HSignal = ProcessSignal(self.HSignal)
                    self.VSignal = ProcessSignal(self.VSignal)
                    signal = ExtractFeatures(Concatenate_Signal_Channels(self.HSignal, self.VSignal))
                    AX_Test = np.array(signal)
                    NX_Test = AX_Test.reshape(1, 100)
                    self.result.append(Classify(self.svm.predict(NX_Test)))
                    signal = []
                    self.SignalLimit = 0
                signal.append(int(value))

        with open('MySimOutput.txt', 'w') as f:
             for s in self.result:
                 f.write(s+'\n')

streamer = StreamHandler()
streamer.create_stream()

@app.route('/predict/', methods=['POST'])
def browser_predict():
    word = request.form.get("word")
    if word == " ":
        words = ["","","","",""]
    else :
        if word[0].isupper() :
            word = word[0].lower() + word[1:]
            words = trie.predict(word)
            for i in range(0,len(words)):
                words[i] = words[i][0].upper() + words[i][1:]
        else:
            words = trie.predict(word)
        words.sort(key=lambda s: len(s))
        return jsonify({'predicted': words}), 200

@app.route('/simulation/', methods=['POST'])
def simulation_stream():
    word = request.form.get("word")
    data = streamer.data_iterator()
    return jsonify({'Moves': data}), 200

if __name__ == "__main__":
    app.run('0.0.0.0')
