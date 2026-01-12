# -*- coding: utf-8 -*-

from tkinter import filedialog
from chardet.universaldetector import UniversalDetector

class BSInterpreter:
    def __init__(self, memory_size=30000):
        self.memory = [0] * memory_size
        self.pointer = 0
        self.output = []
        
        self.commands = {
            'ﾑﾙｺﾞﾙﾚｼﾞ': '>',
            '물걸레질': '>',
            'ﾎﾊﾞｷﾞ': '<',
            '호박이': '<',
            'ﾁｮﾜﾖ~': '+',
            '좋아요~': '+',
            'ｽﾝﾊﾞｺｯﾁ': '-',
            '숨바꼭질': '-',
            'ｳｱｱ!': '.',
            '흐으아악!': '.',
            'ｽﾋﾟｷﾃﾞﾘｼﾞﾊﾞｾﾞﾖ!': ',',
            '스피키 네르지 마세요!': ',',
            'ｽﾋﾟｷﾓﾘﾁｬﾊﾞﾀﾞﾝｷﾞｼﾞﾊﾞｾﾞﾖ!': '[',
            '스피키 머리 잡아당기지 마세요!': '[',
            'ｽﾋﾟｷｦｲｼﾞﾒﾇﾝﾃﾞ...': ']',
            '스피키 열심히 했는데...': ']'
        }
    
    def parse_code(self, raw_code):
        bf_code = []
        i = 0
        while i < len(raw_code):
            matched = False
            for length in range(min(25, len(raw_code) - i), 0, -1):
                substring = raw_code[i:i+length]
                if substring in self.commands:
                    bf_code.append(self.commands[substring])
                    i += length
                    matched = True
                    break
            if not matched:
                i += 1  
        return ''.join(bf_code)
        
    def run(self, code, input_data="", debug=False):
        self.output = []
        self.pointer = 0
        self.memory = [0] * len(self.memory)
        
        code = self.parse_code(code)
        
        code_pointer = 0
        input_pointer = 0
        loop_stack = []
        
        loop_map = {}
        stack = []
        for i, cmd in enumerate(code):
            if cmd == '[':
                stack.append(i)
            elif cmd == ']':
                if not stack:
                    raise ValueError(f"対応する 'ｽﾋﾟｷﾓﾘﾁｬﾊﾞﾀﾞﾝｷﾞｼﾞﾊﾞｾﾞﾖ!' がありません (位置 {i}) / 해당하는 '스피키 머리 잡아당기지 마세요!'가 없습니다 (위치 {i})")
                start = stack.pop()
                loop_map[start] = i
                loop_map[i] = start
        
        if stack:
            raise ValueError(f"対応する 'ｽﾋﾟｷｦｲｼﾞﾒﾇﾝﾃﾞ...' がありません (位置 {stack[0]}) / 해당하는 '스피키 열심히 했는데...'가 없습니다 (위치 {stack[0]})")
        
        while code_pointer < len(code):
            cmd = code[code_pointer]
            
            if debug:
                print(f"[{code_pointer}] {cmd} | ptr={self.pointer} val={self.memory[self.pointer]}")
            
            if cmd == '>':
                self.pointer += 1
                if self.pointer >= len(self.memory):
                    raise IndexError("メモリ範囲外です/메모리 범위를 벗어났습니다")
                    
            elif cmd == '<':
                self.pointer -= 1
                if self.pointer < 0:
                    raise IndexError("メモリ範囲外です/메모리 범위를 벗어났습니다")
                    
            elif cmd == '+':
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
                
            elif cmd == '-':
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
                
            elif cmd == '.':
                self.output.append(chr(self.memory[self.pointer]))
                
            elif cmd == ',':
                if input_pointer < len(input_data):
                    self.memory[self.pointer] = ord(input_data[input_pointer])
                    input_pointer += 1
                else:
                    self.memory[self.pointer] = 0
                    
            elif cmd == '[':
                if self.memory[self.pointer] == 0:
                    code_pointer = loop_map[code_pointer]
                    
            elif cmd == ']':
                if self.memory[self.pointer] != 0:
                    code_pointer = loop_map[code_pointer]
            
            code_pointer += 1
        
        return ''.join(self.output)

def menu():
    print("")
    print("--------------------------------------------------------------")
    print("番号を選択してください/번호를 선택하세요")
    print("--------------------------------------------------------------")
    print("1. .spkもしくは.txtファイルを読み込む/.spk파일 또는 .txt파일 열기")
    print("2. 情報/정보")
    print("3. 終了/종료")
    global menuanswer
    menuanswer = input(">>")
    print("")
    menuanswerinput()

def menuanswerinput():
    global menuanswer
    global run
    if menuanswer == "1":
        open_file()
        interpreter = BSInterpreter()
        
        input_data = ""
        if 'ｽﾋﾟｷﾃﾞﾘｼﾞﾊﾞｾﾞﾖ!' in SPKcode or '스피키 네르지 마세요!' in SPKcode:
            print("入力が必要です/입력이 필요합니다:")
            input_data = input(">>")
        
        result = interpreter.run(SPKcode, input_data)
        print(result)
    elif menuanswer == "2":
        print("情報/정보------------------------------------")
        print("Brainｽﾋﾟｷ/Brain스피키")
        print("Created by: Mizuka Lover")
        print("Some help:Claude")
        print("--------------------------------------------")
    elif menuanswer == "3":
        exit()

def open_file():
    global SPKcode
    SPKcode = ""
    typ = [('Brainsupiki Program File','.spk .txt')] 
    
    try:
        Wee = filedialog.askopenfilename(title='Choose your program file...', filetypes = typ)
    except FileNotFoundError:
        pass
    else:
        with open(Wee, 'rb') as f:  
            detector = UniversalDetector()
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            result = detector.result
        
        enc = result['encoding']
        
        if result['encoding'] == 'SHIFT_JIS':
            encoding = 'CP932'
        elif result['encoding'] in ['EUC-KR', 'UHC', 'ISO-2022-KR']:
            encoding = 'CP949'
        else:
            encoding = result['encoding']
        
        with open(Wee, encoding=encoding) as file:
            SPKcode = file.read()

print("Brainsupiki 1.1.0")
print("Created by: Mizuka Lover")

while True:
    menu()
