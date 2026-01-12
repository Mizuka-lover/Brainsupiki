# -*- coding: utf-8 -*-

bf_to_ja = {
    '>': 'ﾑﾙｺﾞﾙﾚｼﾞ',
    '<': 'ﾎﾊﾞｷﾞ',
    '+': 'ﾁｮﾜﾖ~',
    '-': 'ｽﾝﾊﾞｺｯﾁ',
    '.': 'ｳｱｱ!',
    ',': 'ｽﾋﾟｷﾃﾞﾘｼﾞﾊﾞｾﾞﾖ!',
    '[': 'ｽﾋﾟｷﾓﾘﾁｬﾊﾞﾀﾞﾝｷﾞｼﾞﾊﾞｾﾞﾖ!',
    ']': 'ｽﾋﾟｷｦｲｼﾞﾒﾇﾝﾃﾞ...'
}

bf_to_ko = {
    '>': '물걸레질',
    '<': '호박이',
    '+': '좋아요~',
    '-': '숨바꼭질',
    '.': '흐으아악!',
    ',': '스피키 네르지 마세요!',
    '[': '스피키 머리 잡아당기지 마세요!',
    ']': '스피키 열심히 했는데...'
}

def create_reverse_map(mapping):
    return {v: k for k, v in mapping.items()}

ja_to_bf = create_reverse_map(bf_to_ja)
ko_to_bf = create_reverse_map(bf_to_ko)

def bf_to_text(code, lang='ja'):
    mapping = bf_to_ja if lang == 'ja' else bf_to_ko
    result = []
    for char in code:
        if char in mapping:
            result.append(mapping[char])
    return ' '.join(result)

def text_to_bf(text, lang='ja'):
    mapping = ja_to_bf if lang == 'ja' else ko_to_bf
    
    tokens = text.replace('\n', '').split()
    result = []
    
    for token in tokens:
        if token in mapping:
            result.append(mapping[token])
    
    return ''.join(result)

def main():
     while True:
        print("\n変換モードを選択してください / 변환 모드를 선택하세요:")
        print("1. Brainfuck → Brainsupiki(JP)")
        print("2. Brainfuck → Brainsupiki(KR)")
        print("3. Brainsupiki(JP) → Brainfuck")
        print("4. Brainsupiki(KR) → Brainfuck")
        print("5. 終了 / 종료")
        
        choice = input(">>").strip()
        
        if choice == '5':
            break
        
        if choice not in ['1', '2', '3', '4']:
            continue
        
        print("\nコードを入力してください（空行で終了） / 코드를 입력하세요 (빈 줄로 종료):")
        lines = []
        while True:
            line = input()
            if line == '':
                break
            lines.append(line)
        
        code = '\n'.join(lines)
        
        if choice == '1':
            result = bf_to_text(code, 'ja')
            print("\n変換結果/변환 결과:")
            print(result)
        elif choice == '2':
            result = bf_to_text(code, 'ko')
            print("\n変換結果/변환 결과:")
            print(result)
        elif choice == '3':
            result = text_to_bf(code, 'ja')
            print("\n変換結果/변환 결과:")
            print(result)
        elif choice == '4':
            result = text_to_bf(code, 'ko')
            print("\n変換結果/변환 결과:")
            print(result)
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
